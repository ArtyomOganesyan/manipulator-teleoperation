from mujoco.glfw import glfw
import mujoco as mj

JCONNECTED = 262145
JDISCONNECTED = 262146

class Callback():
    def __init__(self, model, data, cam, scene, overlay):
        self.model = model
        self.data = data
        self.cam = cam
        self.scene = scene
        self.overlay = overlay

        self.button_left = False
        self.button_middle = False
        self.button_right = False
        self.lastx = 0
        self.lasty = 0

    def scroll(self, window, xoffset, yoffset):
        action = mj.mjtMouse.mjMOUSE_ZOOM
        mj.mjv_moveCamera(self.model, action, 0.0, -0.05 *
                        yoffset, self.scene, self.cam)
    
    def mouse_move(self, window, xpos, ypos):
        # compute mouse displacement, save
        dx = xpos - self.lastx
        dy = ypos - self.lasty
        self.lastx = xpos
        self.lasty = ypos

        # no buttons down: nothing to do
        if (not self.button_left) and (not self.button_middle) and (not self.button_right):
            return

        # get current window size
        width, height = glfw.get_window_size(window)

        # get shift key state
        PRESS_LEFT_SHIFT = glfw.get_key(
            window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        PRESS_RIGHT_SHIFT = glfw.get_key(
            window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
        mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

        # determine action based on mouse button
        if self.button_right:
            if mod_shift:
                action = mj.mjtMouse.mjMOUSE_MOVE_H
            else:
                action = mj.mjtMouse.mjMOUSE_MOVE_V
        elif self.button_left:
            if mod_shift:
                action = mj.mjtMouse.mjMOUSE_ROTATE_H
            else:
                action = mj.mjtMouse.mjMOUSE_ROTATE_V
        else:
            action = mj.mjtMouse.mjMOUSE_ZOOM

        mj.mjv_moveCamera(self.model, action, dx/height,
                        dy/height, self.scene, self.cam)
        
    # Window manipulation with mouse
    def mouse_button(self, window, button, act, mods):
        # update button state
        self.button_left = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        self.button_middle = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
        self.button_right = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

        # update mouse position
        glfw.get_cursor_pos(window)

    def keyboard(self, window, key, scancode, act, mods):

        # Restart
        # if (act == glfw.PRESS and key == glfw.KEY_R):
        #     mj.mj_resetData(model, data)
        #     mj.mj_forward(model, data)

        # Quit
        if (act == glfw.PRESS and key == glfw.KEY_Q):
            glfw.set_window_should_close(window, 1)

        if (act == glfw.PRESS and key == glfw.KEY_C):
            if self.cam.type == mj.mjtCamera.mjCAMERA_FREE:
                self.cam.type = mj.mjtCamera.mjCAMERA_FIXED
                # self.cam.fixedcamid = camera_id
            else:
                self.cam.type = mj.mjtCamera.mjCAMERA_FREE
            
        # # WASD control
        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_W:
        #     ee_pos[0] += 0.015

        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_A:
        #     ee_pos[1] += 0.015

        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_S:
        #     ee_pos[0] -= 0.015

        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_D:
        #     ee_pos[1] -= 0.015

        # # 
        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_DOWN:
        #     ee_pos[2] -= 0.015
        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_UP:
        #     ee_pos[2] += 0.015
        
        # # Wrist Rotate Lefr/Right
        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_LEFT:
        #     general_coords[4] += 0.015
        # if (act == glfw.REPEAT or act == glfw.PRESS) and key == glfw.KEY_RIGHT:
        #     general_coords[4] -= 0.015

        # # Gripper grab
        # if (act == glfw.PRESS and key == glfw.KEY_E):
        #     if general_coords[-1] == 0:
        #         general_coords[-1] = 255
        #     else:
        #         general_coords[-1] = 0

    def joystick(self, jid, event):
        jname = glfw.get_joystick_name(jid)

        if event == JCONNECTED:
            self.overlay.show_temp_message(f"Joystick {jid} connected")

        elif event == JDISCONNECTED:
            self.overlay.show_temp_message(f"Joystick {jid} disconnected")
        