import glm
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
from components.path import Path
from OpenGL.GL import glClearColor

# handle all ui rendering and flags
class UI():

    # imgui window flags (settings for very basic use)
    WINDOW_FLAGS = ( imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_FOCUS_ON_APPEARING | imgui.WINDOW_NO_RESIZE 
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_RESIZE )

    def __init__(self, window):
            imgui.create_context()

            # create the imgui glfw renderer
            self.renderer = GlfwRenderer(window, True)
            

    # all ui rendering
    def render(self, scene):

        # imgui input
        self.renderer.process_inputs()
        

        # entire ui frame starts
        imgui.new_frame()

        imgui.set_next_window_size(200, 650)
        imgui.set_next_window_position(10,10)

        # ui style and colour variables 
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.25, 0.35, 0.40)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.36, 0.46, 0.51)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.5, 0.65, 0.7)
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.133, 0.156, 0.192, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0.223, 0.243, 0.274, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 0.323, 0.343, 0.374, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, 0.4, 0.5, 0.55, 1.0)
        imgui.push_style_color(imgui.COLOR_CHECK_MARK, 0.55, 0.65, 0.60, 1.0)
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, 0.9, 0.93, 1, 0.1)
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, 0.06, 0.63, 1, 0.2)

        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 1.0, 1.0, 1.0)

        #----------------------------------------------------------------------------
        
        # ui window starts
        imgui.begin("editor", flags=UI.WINDOW_FLAGS)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0.0, 0.0))    # window rounding (has to be after window)

        #----------------------------------------------------------------------------

        # Path section of the ui starts 
        imgui.text("Path")
        imgui.separator()
        imgui.spacing()
        imgui.spacing()

        # path draw buttons 

        if imgui.button("New Random Path"):
            scene.startTime = glfw.get_time()   # resets draw index by changing start time
            scene.path.__init__()   # generates a new random path


        imgui.spacing
        if imgui.button("Retrace Path"):
            scene.startTime = glfw.get_time()   # retraces the path by resetting the draw time/index
        

        # changes how fast the path is drawn (changes based on num segments and the time mutlipier)
        imgui.spacing
        imgui.text("Time Multipler")
        imgui.unindent(-10)
        changed, newMultipler = imgui.slider_int("", value=scene.timeMultipler, # slider for multipler
            min_value = 1, max_value = 900)
        if changed: # if the value changes , update the time multiplier in the scene
            scene.timeMultipler = newMultipler
            scene.startTime = glfw.get_time()   # reset the time for the draw index
        imgui.indent(-10)

        #----------------------------------------------------------------------------

        # path config section 

        # changes number of arcs to draw out over the entire path
        imgui.spacing
        imgui.text("Arcs (req new path)")
        imgui.unindent(-10)
        changed, newArcs = imgui.slider_int("a", value=Path.arcs,
            min_value = 1, max_value = 300)
        if changed:
            Path.arcs = newArcs
        imgui.indent(-10)


        # changes num of segments between each arc start and end points
        imgui.spacing()
        imgui.text("Segments (req new path)")
        imgui.unindent(-10)
        changed, newSegments = imgui.slider_int("as", value=Path.arcsegments,
            min_value = 2, max_value = 300)
        if changed:
            Path.arcsegments = newSegments
        imgui.indent(-10)


        # reset the path settings to some default 
        imgui.spacing()
        if imgui.button("Reset Path Settings"):
            Path.arcsegments = 80
            Path.arcs = 8


        # disables/enables showing path extras
        imgui.spacing()
        changed, scene.showControls = imgui.checkbox("Show Controls", scene.showControls)

        changed, scene.showPoints = imgui.checkbox("Show Points", scene.showPoints)

        changed, scene.showSegments = imgui.checkbox("Show Segments", scene.showSegments)


        #----------------------------------------------------------------------------

        # view settings section starts

        imgui.spacing()
        imgui.spacing()
        imgui.separator()
        imgui.text("View")
        imgui.separator()


        # changes cameras rotation
        imgui.spacing()
        imgui.text("Rotation")
        imgui.unindent(-10)
        changed, rotvalues = imgui.drag_float3(
            "r", scene.rotationCamera[0], scene.rotationCamera[1], scene.rotationCamera[2],
            format='%.2f'
        )
        if changed:
            scene.rotationCamera[0] = rotvalues[0]  # update scenes cameras stored rotation
            scene.rotationCamera[1] = rotvalues[1]
            scene.rotationCamera[2] = rotvalues[2]
        imgui.indent(-10)

        
        # changes cameras position
        imgui.spacing()
        imgui.text("Position")
        imgui.unindent(-10)
        changed, posvalues = imgui.drag_float3(
            "p", scene.positionCamera[0], scene.positionCamera[1], scene.positionCamera[2],
            format='%.2f', change_speed = 0.04
        )
        if changed:
            scene.positionCamera[0] = posvalues[0]
            scene.positionCamera[1] = posvalues[1]
            scene.positionCamera[2] = posvalues[2]
        imgui.indent(-10)


        # changes cameras zoom
        imgui.spacing()
        imgui.text("Zoom")
        imgui.unindent(-10)
        changed, scaleval = imgui.drag_float(
            "s", scene.scaleCamera, min_value = 0.1, max_value = 10.0,
            format='%.4f', change_speed = 0.002
        )
        if changed:
            scene.scaleCamera = scaleval    # update scenes stored zoom
        imgui.indent(-10)


        # reset the cameras transform to some default
        imgui.spacing
        if imgui.button("Reset View"):
            scene.positionCamera = glm.vec3(0.0, -0.6, -6)   # moves camera back 1 unit from origin
            scene.rotationCamera = glm.vec3(25, -45, 0.0)
            scene.scaleCamera = 0.85


        # some view/camera settings
        changed, scene.turn = imgui.checkbox("Turn", scene.turn)    # disable/enable camera auto turning

        changed, scene.showAxis = imgui.checkbox("Show Axis", scene.showAxis)   # show/hide the axis


        # simple background colour change (gl clear colour (ignores glviewport))
        imgui.spacing()
        imgui.text("Back Colour")
        imgui.unindent(-10)
        col = scene.clear_colour
        changed, new_clear_colour = imgui.color_edit3("Cl", *col)
        if changed:
            scene.clear_colour = new_clear_colour   # update scenes stored back colour
            glClearColor(*scene.clear_colour, 1.0)  # change gls clear color 
        imgui.indent(-10)


        #----------------------------------------------------------------------------
        
        # pop styles and colours after ui 
        imgui.pop_style_var(3)
        imgui.pop_style_color(11)

        # end of ui
        imgui.end() # window end (here only one window) 
        imgui.end_frame()   # entire ui end

        #----------------------------------------------------------------------------

        # render ui and draw
        imgui.render()
        self.renderer.render(imgui.get_draw_data())