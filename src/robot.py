import mujoco as mj
import numpy as np
from numpy import pi
import time

class UR5e():
    def __init__(self, model, data, start_pos = np.array([0, -1.45, 1.67, -2.52, -1.57, 0, 0])):
        self.model = model
        self.data = data
        self.q = np.zeros((model.nu,))  # general coords [:6] and last is gripper actuator
        self.start_pos = start_pos
        self.data.qpos[:7] = start_pos
        self.start_time = time.time()

        self.site_id = self.model.site("attachment_site").id
        self.J = np.zeros((6, model.nv))


    def set_ctrl(self, control):
        self.data.ctrl[:-1] = control


    def gripper_state(self):
        return self.data.ctrl[-1]
    

    def change_gripper_state(self):
        if self.gripper_state() == 0 and time.time() - self.start_time > 0.5:
            self.data.ctrl[-1] = 255
            self.start_time = time.time()

        elif self.gripper_state() == 255 and time.time() - self.start_time > 0.5:
            self.data.ctrl[-1] = 0
            self.start_time = time.time()


    def update_jacobian(self):
        mj.mj_jacSite(self.model, self.data, self.J[:3], self.J[3:], self.site_id)
    

    def get_ee_jacobian(self):
        self.update_jacobian()
        return self.J[:, :6]
        