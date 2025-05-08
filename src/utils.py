import numpy as np
from numpy import cos, sin
from mujoco.glfw import glfw
import matplotlib.pyplot as plt


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

    # Flip vertically (Matplotlib origin is bottom, GLFW uses top)
    # icon_data = np.flipud(icon_data)

    # Convert to nested list [height][width][RGBA]
    pixels_list = icon_data.tolist()

    # Set window icon
    icon = (icon_data.shape[1], icon_data.shape[0], pixels_list)
    glfw.set_window_icon(window, 1, icon)