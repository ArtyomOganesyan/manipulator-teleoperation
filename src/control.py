from abc import ABC, abstractmethod
from mujoco.glfw import glfw
import numpy as np

class RobotController(ABC):
    @abstractmethod
    def update(self, robot):
        """Compute control commands and apply them to the robot."""
        pass


class JoystickController(RobotController):
    def __init__(self, joystick_handler, window):
        self.js = joystick_handler
        self.window = window

    def update(self, robot):
        if glfw.joystick_present(glfw.JOYSTICK_1):
            v_des, omega_des = self.js.get_des_twist()  # Your existing logic
            v_des[2] += 0.015  # Gravity compensation
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
