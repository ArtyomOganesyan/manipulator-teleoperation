import mujoco as mj

class Overlay():
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.overlay = {}
    

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
        # overlay items
        for gridpos, [t1, t2] in self.overlay.items():

            mj.mjr_overlay(
                mj.mjtFontScale.mjFONTSCALE_150,
                gridpos,
                viewport,
                t1,
                t2,
                context)


    def clear(self):
        self.overlay.clear()