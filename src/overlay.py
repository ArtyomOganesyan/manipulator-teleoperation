import mujoco as mj
import time

class Overlay():
    def __init__(self, robot):
        self.model = robot.model
        self.data = robot.data
        self.robot = robot
        self.overlay = {}
        
        self.message = ''
        self.start_time = 0.0
        self.msg_duration = 1.0
    

    def add_overlay(self, gridpos, text1, text2):

        if gridpos not in self.overlay:
            self.overlay[gridpos] = ["", ""]
        self.overlay[gridpos][0] += text1 + "\n"
        self.overlay[gridpos][1] += text2 + "\n"


    def create(self):
        topleft = mj.mjtGridPos.mjGRID_TOPLEFT
        topright = mj.mjtGridPos.mjGRID_TOPRIGHT
        bottomleft = mj.mjtGridPos.mjGRID_BOTTOMLEFT
        bottomright = mj.mjtGridPos.mjGRID_BOTTOMRIGHT

        self.add_overlay(
            bottomleft,
            "Restart",'R' ,
            )
        
        self.add_overlay(
            bottomleft,
            "Quit",'Q' ,
            )
        
        self.add_overlay(
            bottomleft,
            "Camera",'C' ,
            )
        
        self.add_overlay(
            bottomleft,
            "Time",'%.2f' % self.data.time
        )


        self.add_overlay(
            topleft,
            "x", '%.2f' % self.robot.ee_pos[0]
        )
        self.add_overlay(
            topleft,
            "y", '%.2f' % self.robot.ee_pos[1]
        )
        self.add_overlay(
            topleft,
            "z", '%.2f' % self.robot.ee_pos[2]
        )



    def show_items(self, viewport, context):

        # show timed message to top center if active
        if self.message and (time.time() - self.start_time < self.msg_duration):
            mj.mjr_overlay(
                mj.mjtFontScale.mjFONTSCALE_150,
                mj.mjtGridPos.mjGRID_TOP,
                viewport,
                self.message,
                "",
                context
            )

        # overlay items
        for gridpos, [t1, t2] in self.overlay.items():

            mj.mjr_overlay(
                mj.mjtFontScale.mjFONTSCALE_150,
                gridpos,
                viewport,
                t1,
                t2,
                context)
            
    def show_temp_message(self, msg, duration=1.0):
        self.message = msg
        self.start_time = time.time()
        self.msg_duration = duration


    def clear(self):
        self.overlay.clear()