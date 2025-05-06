import mujoco as mj

class Overlay():
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self._overlay = {}
    

    def add_overlay(self, gridpos, text1, text2):

        if gridpos not in self._overlay:
            self._overlay[gridpos] = ["", ""]
        self._overlay[gridpos][0] += text1 + "\n"
        self._overlay[gridpos][1] += text2 + "\n"

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

    def clear(self):
        self._overlay.clear()

    def items(self):
        return self._overlay.items()