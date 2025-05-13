import numpy as np
import mujoco as mj
from mujoco.glfw import glfw
from overlay import Overlay
from callbacks import Callback
import utils
import os

from tests.test_joystick import JoystickHandler
from robot import UR5e

PATH = 'models/'
TASK_NAME = 'PickAndPlace'
FILE_NAME = TASK_NAME + '.xml'
SIMTIME = 100
print_camera_config = False # this is useful for initializing view of the model)

#get the full path
current_dirname = os.getcwd()
abspath = os.path.join(current_dirname + "/" + PATH + FILE_NAME)
xml_path = abspath

# MuJoCo data structures
model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
data = mj.MjData(model)                     # MuJoCo data
cam = mj.MjvCamera()                        # Abstract camera
opt = mj.MjvOption()                        # visualization options
ee_cam_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_CAMERA, "camera_on_ee")

manipulator = UR5e(model, data)

# Init GLFW, create window, make OpenGL context current, request v-sync
glfw.init()
window = glfw.create_window(1200, 700, "Teleoperation on task " + TASK_NAME, None, None)
utils.set_icon_to(window, current_dirname + '/icon.jpg')
glfw.make_context_current(window)
glfw.swap_interval(1)

# Init overlay
overlay = Overlay(manipulator)

# initialize visualization data structures
mj.mjv_defaultCamera(cam)
mj.mjv_defaultOption(opt)
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

# install GLFW mouse and keyboard callbacks
callback = Callback(model, data, cam, scene, overlay)

glfw.set_key_callback(window, callback.keyboard)
glfw.set_cursor_pos_callback(window, callback.mouse_move)
glfw.set_mouse_button_callback(window, callback.mouse_button)
glfw.set_scroll_callback(window, callback.scroll)
glfw.set_joystick_callback(callback.joystick)

# Example on how to set camera configuration
# cam.azimuth = 90
# cam.elevation = -45
# cam.distance = 2
# cam.lookat = np.array([0.0, 0.0, 0])
cam.azimuth = 0 ; cam.elevation = -39 ; cam.distance =  2.6
cam.lookat = np.array([ 0.0, 0.0, 0.5 ])
cam.type = mj.mjtCamera.mjCAMERA_FREE

# Set camera to use the fixed camera defined in XML
cam.type = mj.mjtCamera.mjCAMERA_FIXED
cam.fixedcamid = ee_cam_id

js = JoystickHandler()

while not glfw.window_should_close(window):
    time_prev = data.time

    while (data.time - time_prev < 1.0/60.0):
        mj.mj_step(model, data)
        js.update(manipulator, window)
        manipulator.forward_kinematics()
    # get framebuffer viewport
    viewport_width, viewport_height = glfw.get_framebuffer_size(window)
    viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

    #create overlay
    overlay.create()

    #print camera configuration (help to initialize the view)
    if print_camera_config:
        print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
        print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')

    # Update scene and render
    mj.mjv_updateScene(model, data, opt, None, cam,
                       mj.mjtCatBit.mjCAT_ALL.value, scene)
    mj.mjr_render(viewport, scene, context)

    # overlay items
    overlay.show_items(viewport, context)

    # clear overlay
    overlay.clear()

    # swap OpenGL buffers (blocking call due to v-sync)
    glfw.swap_buffers(window)

    # process pending GUI events, call GLFW callbacks
    glfw.poll_events()

glfw.terminate()
