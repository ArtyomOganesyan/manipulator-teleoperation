from abc import ABC, abstractmethod
import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
from utils import Kalman1D, UKF1D

class RobotController(ABC):
    @abstractmethod
    def update(self, robot):
        """Compute control commands and apply them to the robot."""
        pass


class JoystickHandler:
    def __init__(self):
        self.prev_buttons = []

    def get_des_twist(self):
        if glfw.joystick_present(glfw.JOYSTICK_1):
            axes, _ = glfw.get_joystick_axes(glfw.JOYSTICK_1)

            def transform(axis):
                return (-(axis) ** 3)*0.5
            
            lstick_hor = transform(axes[0])
            lstick_ver = transform(axes[1])
            rstick_hor = transform(axes[2])
            rstick_ver = transform(axes[3])
            l2 = -(axes[4] + 1) * 0.2
            r2 = (axes[5] + 1) * 0.2

            v_des = np.array([lstick_ver, lstick_hor, r2+l2])
            omega_des = np.array([rstick_hor, rstick_ver, 0])
            return v_des, omega_des


class JoystickController(RobotController):
    def __init__(self, joystick_handler, window):
        self.js = joystick_handler
        self.window = window

    def update(self, robot):
        if glfw.joystick_present(glfw.JOYSTICK_1):
            v_des, omega_des = self.js.get_des_twist()
            # v_des[2] += 0.015  # Gravity compensation
            dx = np.hstack([v_des, omega_des])

            robot.update_jacobian()
            J = robot.get_ee_jacobian()

            if not abs(np.linalg.det(J)) < 0.02:
                dq = np.linalg.inv(J) @ dx
                robot.set_ctrl(dq)
            else:
                print('Singularity')

            # Handle gripper buttons
            buttons, _ = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
            if buttons[0] == glfw.PRESS:
                robot.change_gripper_state()

            if (glfw.PRESS == buttons[1]):
                glfw.set_window_should_close(self.window, 1)


class AndroidController(RobotController):
    def __init__(self):
        self.ukf_filters = [UKF1D(), UKF1D(), UKF1D()]  # x, y, z
        self.last_gyro = np.zeros(3)           # Already angular velocity
        self.pressed = False
        self.last_timestamp = None             # For dt calculation

    def update_sensor_data(self, sensor_type, values, timestamp):
        dt = 0.0
        if self.last_timestamp is not None:
            dt = (timestamp - self.last_timestamp) / 1e9

        if sensor_type == "android.sensor.linear_acceleration" and dt > 0:
            raw_accel = np.array(values)

            # Axis remapping
            accel = np.zeros(3)
            accel[2] = raw_accel[2] * 1.5
            # accel[1] = -raw_accel[0] * 2
            # accel[0] = raw_accel[1] * 2

            for i in range(3):
                self.ukf_filters[i].predict_update(accel[i], dt)

        elif sensor_type == "android.sensor.gyroscope":
            raw_gyro = np.array(values)
            raw_gyro[0], raw_gyro[1] = raw_gyro[1], -raw_gyro[0]
            self.last_gyro = raw_gyro

        self.last_timestamp = timestamp

    def update_touchscreen(self, action):
        if action == 'ACTION_DOWN':
            self.pressed = True
        if action == 'ACTION_UP':
            self.pressed = False

    def update(self, robot):
        # Map sensor data to robot commands
        v_des = np.array([f.get_velocity() for f in self.ukf_filters])
        v_des[2] += 0.015  # Gravity compensation

        omega_des = np.array(self.last_gyro.copy())
        
        dx = np.hstack([v_des, omega_des])
        robot.update_jacobian()
        J = robot.get_ee_jacobian()

        if not abs(np.linalg.det(J)) < 0.02:
            dq = np.linalg.inv(J) @ dx
            robot.set_ctrl(dq)
        else:
            print('Singularity')

        if self.pressed:
            robot.change_gripper_state()