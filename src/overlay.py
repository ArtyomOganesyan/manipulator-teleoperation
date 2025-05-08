import mujoco as mj
import time

class Overlay():
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.overlay = {}
        
        self.message = ''
        self.start_time = 0.0
        self.msg_duration = 1.0
    

    def add_overlay(self, gridpos, text1, text2):

        if gridpos not in self.overlay:
            self.overlay[gridpos] = ["", ""]
        self.overlay[gridpos][0] += text1 + "\n"
        self.overlay[gridpos][1] += text2 + "\n"


    def create(self, model, data):
        topleft = mj.mjtGridPos.mjGRID_TOPLEFT
        topright = mj.mjtGridPos.mjGRID_TOPRIGHT
        bottomleft = mj.mjtGridPos.mjGRID_BOTTOMLEFT
        bottomright = mj.mjtGridPos.mjGRID_BOTTOMRIGHT

        self.add_overlay(
            bottomleft,
            "Restart",'r' ,
            )
        
        self.add_overlay(
            bottomleft,
            "Quit",'q' ,
            )
        
        self.add_overlay(
            bottomleft,
            "Time",'%.2f' % data.time
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