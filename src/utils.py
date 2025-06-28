import numpy as np
from numpy import cos, sin
from mujoco.glfw import glfw
import matplotlib.pyplot as plt

from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import MerweScaledSigmaPoints


def ht(q, d, a, alpha):
  R_zi = np.array([[cos(q),  -sin(q), 0],
                   [sin(q),   cos(q), 0],
                   [0,        0,      1]])

  R_xi = np.array([[1,          0,          0],
                   [0, cos(alpha),-sin(alpha)],
                   [0, sin(alpha), cos(alpha)]])

  p_di = np.array([0, 0, d]).reshape((3,1))
  p_ai = np.array([a, 0, 0]).reshape((3,1))

  T1 = np.block([
      [R_zi, np.zeros((3, 1))],
      [np.zeros(3), 1]
      ])

  T2 = np.block([
      [np.eye(3), p_di],
      [np.zeros(3), 1]
      ])

  T3 = np.block([
      [np.eye(3), p_ai],
      [np.zeros(3), 1]
      ])

  T4 = np.block([
      [R_xi, np.zeros((3, 1))],
      [np.zeros(3), 1]
      ])
  return T1 @ T2 @ T3 @ T4


def ht_inv(T):
    R = T[:3,:3]
    p = T[:3, 3].reshape(3,1)
    invT = np.block([[R.T, -R.T @ p], [np.zeros(3), 1]])
    return invT


def set_icon_to(window, icon_path):
    # Load image with matplotlib (returns floats in [0,1])
    icon_data = plt.imread(icon_path)

    # Ensure data is uint8 (0-255)
    if icon_data.dtype == np.float32 or icon_data.dtype == np.float64:
        icon_data = (icon_data * 255).astype(np.uint8)

    # Add alpha channel if missing (convert RGB to RGBA)
    if icon_data.shape[2] == 3:
        alpha = np.full((*icon_data.shape[:2], 1), 255, dtype=np.uint8)
        icon_data = np.concatenate([icon_data, alpha], axis=2)
    elif icon_data.shape[2] != 4:
        raise ValueError("Image must have 3 (RGB) or 4 (RGBA) channels")

    pixels_list = icon_data.tolist()

    # Set window icon
    icon = (icon_data.shape[1], icon_data.shape[0], pixels_list)
    glfw.set_window_icon(window, 1, icon)

class Kalman1D:
    def __init__(self):
        self.x = np.array([[0], [0]])  # state: [v, a]
        self.P = np.eye(2) * 0.1       # state covariance
        self.A = np.eye(2)            # state transition
        self.H = np.array([[0, 1]])   # we observe acceleration only
        self.Q = np.eye(2) * 0.01     # process noise
        self.R = np.array([[0.1]])    # measurement noise

    def predict(self, dt):
        self.A[0, 1] = dt
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        # z = measured acceleration
        y = np.array([[z]]) - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(2) - K @ self.H) @ self.P

    def get_velocity(self):
        return self.x[0, 0]


class UKF1D:
    def __init__(self):
        # 2D state: [velocity, acceleration]
        self.dt = 0.01
        self.points = MerweScaledSigmaPoints(n=2, alpha=0.1, beta=2., kappa=0)
        self.ukf = UKF(dim_x=2, dim_z=1, fx=self.fx, hx=self.hx, dt=self.dt, points=self.points)
        self.ukf.x = np.array([0., 0.])  # initial state: [v, a]
        self.ukf.P *= 0.1
        self.ukf.Q = np.diag([0.01, 0.01])
        self.ukf.R = np.array([[0.1]])

    def fx(self, x, dt):
        # x: [v, a]
        v = x[0] + x[1] * dt
        a = x[1]
        return np.array([v, a])

    def hx(self, x):
        return np.array([x[1]])  # Only acceleration is measured

    def predict_update(self, accel_measurement, dt):
        self.ukf.predict(dt=dt)
        self.ukf.update(np.array([accel_measurement]))

    def get_velocity(self):
        return self.ukf.x[0]