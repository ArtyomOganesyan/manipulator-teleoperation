import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import time

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
        
        val = -(axes[0]*1.5) ** 3
        control = np.array([val, 0., 0., 0., 0., 0.])
        robot.set_ctrl(control)

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
