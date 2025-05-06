import mujoco as mj
from mujoco.glfw import glfw
# from teleop_demo import model, cam, scene

# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

global model
global scene
global cam

# Keyboard controls
def keyboard(window, key, scancode, act, mods):
    global quit

    # Restart
    # if (act == glfw.PRESS and key == glfw.KEY_R):
    #     mj.mj_resetData(model, data)
    #     mj.mj_forward(model, data)

    # Quit
    if (act == glfw.PRESS and key == glfw.KEY_Q):
        quit = True

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

# Window manipulation with mouse
def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    # update mouse position
    glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
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
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height,
                      dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)