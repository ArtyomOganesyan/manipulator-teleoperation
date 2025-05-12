import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

def get_jaxes():
    if glfw.joystick_present(glfw.JOYSTICK_1):
        axes = glfw.get_joystick_axes(glfw.JOYSTICK_1)
        buttons = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
    return axes, buttons

def apply_deadzone(val, threshold=0.1):
    return 0 if abs(val) < threshold else val

def update_control_from_joystick(robot, window):
    if glfw.joystick_present(glfw.JOYSTICK_1):
        axes, _ = glfw.get_joystick_axes(glfw.JOYSTICK_1)
        buttons, _ = glfw.get_joystick_buttons(glfw.JOYSTICK_1)

        def transform(axis):
            return -(axis) ** 3
        
        lstick_hor = transform(axes[0])
        lstick_ver = transform(axes[1])
        rstick_hor = transform(axes[2])
        rstick_ver = transform(axes[3])
        l2 = -(axes[4] + 1) * 0.5
        r2 = (axes[5] + 1) * 0.5

        v_des = np.array([lstick_ver, lstick_hor, r2+l2])
        omega_des = np.array([rstick_hor, rstick_ver, 0])

        dx = np.hstack([v_des, omega_des])

        robot.update_jacobian()
        J = robot.get_ee_jacobian()

        dq = np.linalg.inv(J) @ dx

        robot.ee_pos += dq[:3] * 1.0/60
        robot.ee_rot += dq[3:] * 1.0/60

        control = np.hstack([robot.ee_pos, robot.ee_rot])
        robot.set_ctrl(dq)

        if (glfw.PRESS == buttons[0]):
            robot.change_gripper_state()

        if (glfw.PRESS == buttons[1]):
            glfw.set_window_should_close(window, 1)


class JoystickHandler:
    def __init__(self):
        self.prev_buttons = []

    def update(self):
        if glfw.joystick_present(glfw.JOYSTICK_1):
            buttons = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
            if self.prev_buttons:
                for i, (prev, curr) in enumerate(zip(self.prev_buttons, buttons)):
                    if prev == glfw.RELEASE and curr == glfw.PRESS:
                        print(f"Button {i} pressed")
            self.prev_buttons = buttons
