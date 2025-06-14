import mujoco as mj
from mujoco.glfw import glfw
import numpy as np


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

