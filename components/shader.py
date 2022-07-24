from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glDeleteProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

class Shader():

    @staticmethod
    def gen_shader(vpath, fpath):

        # read vertex shader source from file path
        with open(vpath, 'r') as fle:
            v_src = fle.read()

        # read fragment shader source from file path
        with open(fpath, 'r') as fle:
            f_src = fle.read()

        # pyopengl convient shader program function
        shader = compileProgram(
            compileShader(v_src, GL_VERTEX_SHADER), # compiles a shader of given source and type
            compileShader(f_src, GL_FRAGMENT_SHADER))

        return shader

    # delete shader program
    @staticmethod
    def del_shader(program):
        glDeleteProgram(program)