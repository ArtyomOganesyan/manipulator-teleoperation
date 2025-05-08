import mujoco as mj
from mujoco.glfw import glfw

def get_jaxes():
    if glfw.joystick_present(glfw.JOYSTICK_1):
        axes = glfw.get_joystick_axes(glfw.JOYSTICK_1)
        buttons = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
    return axes

def update_control_from_joystick(model, data):
    if glfw.joystick_present(glfw.JOYSTICK_1):
        axes, _ = glfw.get_joystick_axes(glfw.JOYSTICK_1)
        buttons, _ = glfw.get_joystick_buttons(glfw.JOYSTICK_1)
        
        val = -axes[0]
        data.ctrl[0] = val

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
