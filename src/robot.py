import mujoco as mj
import numpy as np
from numpy import pi
from kinematics import fkine
import time

class UR5e():
    def __init__(self, model, data, controller=None, start_pos = np.array([-1.57, -1.45, 1.67, -2.52, -1.57, 0])):
        self.model = model
        self.data = data
        self.start_pos = start_pos
        self.data.qpos[:6] = start_pos
        self.q = self.data.qpos[:6]
        self.start_time = time.time()
        self.controller = controller

        self.ee_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "end_effector")
        self.J = np.zeros((6, model.nv))

        self.DH = {
            'q_0': np.array([-pi/2, 0, 0, 0, 0, 0]),
            'a': np.array([0, -0.425, -0.3922, 0, 0, 0]),
            'd': np.array([0.1625, 0, 0, 0.1333, 0.0997, 0.0996]),
            'alpha': np.array([pi/2, 0, 0, pi/2, -pi/2, 0])
        }

        self.ee_pos, self.ee_rot = fkine(self.q, self.DH)
        self.data.qpos[:6] = start_pos

    def update(self):
        if self.controller:
            self.controller.update(self)

    def set_ee_pos(self, pos):
        self.ee_pos = pos.copy()

    def set_ee_rot(self, rot):
        self.ee_rot = rot.copy()

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
        mj.mj_jacBody(self.model, self.data, self.J[:3], self.J[3:], self.ee_id)
    
    def get_ee_jacobian(self):
        return self.J[:, :6]
    
    def forward_kinematics(self):
        self.ee_pos, self.ee_rot = fkine(self.q, self.DH)