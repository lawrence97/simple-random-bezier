import glfw
import glm
from math import floor
from OpenGL.GL import *

from components.shader import Shader
from components.ui import UI
from components.axis import Axis
from components.path import Path


PATH_VERTEX = "shaders/path_vert.glsl"
PATH_FRAGMENT = "shaders/path_frag.glsl"
AXIS_VERTEX = "shaders/axis_vert.glsl"
AXIS_FRAGMENT = "shaders/axis_frag.glsl"


class Scene():
    WIDTH = 1000
    HEIGHT = 800

    def __init__(self):

        # init window and context
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # glfw window
        self.window = glfw.create_window(Scene.WIDTH, Scene.HEIGHT, "random-bezier", None, None)

        glfw.set_window_attrib(self.window, glfw.RESIZABLE, False)
        glfw.set_window_pos(self.window, 200, 100)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)   # vsync enabled/disabled

        # setup shader programs
        self.path_shader = Shader.gen_shader(PATH_VERTEX, PATH_FRAGMENT)
        self.axis_shader = Shader.gen_shader(AXIS_VERTEX, AXIS_FRAGMENT)

        self.clear_colour = (0.160, 0.294, 0.305)   # back colour

        # gl configure
        glClearColor(*self.clear_colour, 1.0)
        glViewport(220, 0, Scene.WIDTH - 220, Scene.HEIGHT) 
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # imgui UI object
        self.ui = UI(window=self.window)

        # store reference to shader uniforms
        self.col_uni = glGetUniformLocation(self.path_shader, "ucol")   # paths shader uniforms
        self.view_uni = glGetUniformLocation(self.path_shader, "view")
        self.proj_uni = glGetUniformLocation(self.path_shader, "proj")

        self.view_uni_axis = glGetUniformLocation(self.axis_shader, "view") # axis shader uniforms 
        self.proj_uni_axis = glGetUniformLocation(self.axis_shader, "proj")

        # default camera transform
        self.positionCamera = glm.vec3(0.0, -0.6, -6)   # move camera back origin
        self.rotationCamera = glm.vec3(25, -45, 0.0)
        self.scaleCamera = 0.92

        # create and set perspective matrix in both shader programs as uniforms (only set once)
        proj = glm.perspective(90, 1, 0.1, 200)
        glUseProgram(self.axis_shader)
        glUniformMatrix4fv(self.proj_uni_axis, 1, GL_FALSE, glm.value_ptr(proj))
        glUseProgram(self.path_shader)
        glUniformMatrix4fv(self.proj_uni, 1, GL_FALSE, glm.value_ptr(proj))

        # axis ( x y z lines )
        self.axis = Axis()

        # path is the programs entire curve (data/buffer/vao/settings)
        self.path = Path()

        # draw index of the curve (used to draw the path out over time)
        self.pathIndex = 0

        # some path/camera settings
        self.turn = True
        self.pathTime = 0
        self.startTime = 0
        self.timeMultipler = 50
        self.showControls = True
        self.showPoints = True
        self.showSegments = False
        self.showAxis = True


        self.run()

    def run(self):
  
        self.startTime = glfw.get_time()
        
        while not glfw.window_should_close(self.window):
            
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # render(and updates) enitre scene
            self.render()

            # render ui
            self.ui.render(scene=self)

            glfw.swap_buffers(self.window)


        # terminate after loop
        self.end()

    
    # main scene render/update
    def render(self):
 
        # calc how much of path to draw based on time elapsed
        self.pathTime = glfw.get_time() - self.startTime
        self.pathIndex = min(floor(self.pathTime * self.timeMultipler), len(self.path.curve)//3)

        # small camera rotate  
        if self.turn: 
            self.rotationCamera[1] += 0.006     # amount of turn
        
        # calc view matrix (from cameras transform)
        view = glm.mat4(1.0)
        view = glm.translate(view, self.positionCamera)
        view = glm.rotate(view, glm.radians(self.rotationCamera[0]), glm.vec3(1.0, 0.0, 0.0))
        view = glm.rotate(view, glm.radians(self.rotationCamera[1]), glm.vec3(0.0, 1.0, 0.0))
        view = glm.rotate(view, glm.radians(self.rotationCamera[2]), glm.vec3(0.0, 0.0, 1.0))
        view = glm.scale(view, glm.vec3(self.scaleCamera))

        
        # use axis shader       
        glUseProgram(self.axis_shader)

        # sets the view matrix uniform in the axis shader (doesnt need model matrix, as axis is constant transform)
        glUniformMatrix4fv(self.view_uni_axis, 1, GL_FALSE, glm.value_ptr(view))


        # axis draw
        glLineWidth(1)
        if self.showAxis:
            glBindVertexArray(self.axis.vao)
            glDrawArrays(GL_LINES, 0, self.axis.ngrid)


        # use path shader
        glUseProgram(self.path_shader)


        # set the view uniform (previously calcualted) now in the path shader
        glUniformMatrix4fv(self.view_uni, 1, GL_FALSE, glm.value_ptr(view))

        # set the paths colour uniform in shader
        colour = glm.vec4(1.0, 1.0, 1.0, 0.9)
        glUniform4fv(self.col_uni, 1, glm.value_ptr(colour))
        
        # bind the path vao and draw the path (curve itself - made of arcs each with segments )
        glBindVertexArray(self.path.pathvao)
        glDrawArrays(GL_LINE_STRIP, 0, self.pathIndex)

        # draw each segment of each arc of the curve (every point of the curve)
        if self.showSegments:
            # use slightly different colour for segments of curve
            colour = glm.vec4(0.8, 0.8, 0.8, 0.7)
            glUniform4fv(self.col_uni, 1, glm.value_ptr(colour))
            glPointSize(1)
            glDrawArrays(GL_POINTS, 0, len(self.path.curve)//3)
        

        # draw the points of curve (start and end points of each arc)
        if self.showPoints:
            colour = glm.vec4(1.0, 1.0, 1.0, 0.8)
            glUniform4fv(self.col_uni, 1, glm.value_ptr(colour))
            glPointSize(4)
            glBindVertexArray(self.path.pointsvao)
            glDrawArrays(GL_POINTS, 0, len(self.path.points) // 3)
 

        # draws the controls of the bezier arcs (one control point for every two arc endpoints)
        if self.showControls:
            colour = glm.vec4(1.0, 0.5, 0.2, 1.0)
            glUniform4fv(self.col_uni, 1, glm.value_ptr(colour))
            glPointSize(3)
            glBindVertexArray(self.path.controlsvao)
            glDrawArrays(GL_POINTS, 0, len(self.path.controls) // 3)



    # delete buffer/array/shaders and terminte ui/window
    def end(self):
        del self.path
        self.ui.renderer.shutdown()
        del self.axis
        Shader.del_shader(self.path_shader)
        Shader.del_shader(self.axis_shader)
        glfw.destroy_window(self.window)
        glfw.terminate()



if __name__ == "__main__":
    scene = Scene()