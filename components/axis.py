import glm
from OpenGL.GL import *

class Axis():
    def __init__(self):
        
        # vertex position and colour data for axis

        self.grid = [-5,  0,  0,    # positions
                      5,  0,  0,  
                      0, -5,  0,  
                      0,  5,  0,  
                      0,  0, -5,
                      0,  0,  5,
    
                      1,  0,  0.2,  # colours
                      1,  0,  0.2,
                      0,  1,  0.5,
                      0,  1,  0.5, 
                      0,  0.7,  1,
                      0,  0.7,  1]

        # vertices from list to array of float32s (for openGL)
        self.ggrid = glm.array(glm.float32, *self.grid)
        self.ngrid = 6  # number of vertices to draw

        # gen vertex array and buffer for axis
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao) # bind vao, all further buffer operations bound to this array
        
        # bind and upload vertex data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, glm.sizeof(self.ggrid), self.ggrid.ptr, GL_STATIC_DRAW)
        
        # enable vertex attributes for buffer
        # position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # colour attribute
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(72)) 
        # *cols start 72 bytes offset from start of buffer

        # unbind
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def __del__(self):
        # delete vao and vbo
       glDeleteVertexArrays(1, (self.vao,))
       glDeleteBuffers(1, (self.vbo,))