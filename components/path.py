import glm
import numpy
from OpenGL.GL import *

# path contains data for the curves/arcs/points/controls/settings
class Path():

    # number of segments between each 2 points
    arcsegments = 80    # eg. 80 lines between each arc
    
    # number of arcs to generate 
    arcs = 8    # eg. 2 points per arc (total of (8 * 80) vertices the path traces out)

    def __init__(self):
        # points holds endpoints of arcs
        self.points = []
        self.points.extend([0, 0, 0])   # always start at origin

        # generate a point to go to from origin
        self.points.extend(numpy.random.uniform(low=-5, high=5, size=3))

        self.controls = []  # holds all the control points

        # generate one initial control point for the origin and second point
        self.controls.extend(numpy.random.uniform(low=-5, high=5, size=3))

        # curve holds all arcs 
        self.curve = []


        # generate a smooth path of a number of segments between the arcs endpoints
        # (quadratic bezier part)
        for i in range(0, Path.arcsegments):
            # parameter t increasing along path
            t = (i)/(Path.arcsegments-1)

            # store start/end and control point
            p0 = [self.points[0], self.points[1], self.points[2]]   # start
            p1 = [self.controls[0], self.controls[1], self.controls[2]] # control
            p2 = [self.points[3], self.points[4], self.points[5]]   # end

            # bezier point 1 calculation
            l0 = [ ((1-t)*p0[0]) + (t*p1[0]),
                   ((1-t)*p0[1]) + (t*p1[1]),
                   ((1-t)*p0[2]) + (t*p1[2]) ]

            # bezier point 2 calculation
            l1 = [ ((1-t)*p1[0]) + (t*p2[0]),
                   ((1-t)*p1[1]) + (t*p2[1]),
                   ((1-t)*p1[2]) + (t*p2[2]) ]

            # calc the final segment vertex position that traces a bezier curve for this 't'
            vert = [ ((1-t)*l0[0]) + (t*l1[0]),
                     ((1-t)*l0[1]) + (t*l1[1]),
                     ((1-t)*l0[2]) + (t*l1[2]) ]

            # add this bezier position to the curve
            self.curve.extend(vert)

        # extend this path after initial arc to number of arcs
        for i in range(1, Path.arcs):
            self.addArc()   # same process

        # send stored lists of vertex positions for the arc endpoints, controls and segments
        # into arrays of float32s before use with opengl
        self.gcurve = glm.array(glm.float32, *self.curve)
        self.gpoints = glm.array(glm.float32, *self.points)
        self.gcontrols = glm.array(glm.float32, *self.controls)
        
        # generate vaos/vbos for path objects 
        """
        self.pathvao = glGenVertexArrays(1)
        self.pathvbo = glGenBuffers(1)
        self.pointsvao = glGenVertexArrays(1)
        self.pointsvbo = glGenBuffers(1)
        self.controlsvao = glGenVertexArrays(1)
        self.controlsvbo = glGenBuffers(1)
        """

        self.pathvao, self.pointsvao, self.controlsvao = glGenVertexArrays(3)
        self.pathvbo, self.pointsvbo, self.controlsvbo = glGenBuffers(3)


        # upload all path data to buffers and vao for them
        self.bufferObject(self.pathvao, self.pathvbo, self.gcurve)
        self.bufferObject(self.pointsvao, self.pointsvbo, self.gpoints)
        self.bufferObject(self.controlsvao, self.controlsvbo, self.gcontrols)

    # adds an arc to the curve
    def addArc(self):
        newpoint = numpy.random.uniform(low=-5, high=5, size=3) # new next random point
        newcontrol = numpy.random.uniform(low=-4, high=4, size=3)   # a new random control
        
        # calculate a new arc based on the last arc endpoint and the new one and control from above 
        newarc = self.calcNew([self.points[-3],self.points[-2], self.points[-1]],
                               newcontrol, newpoint, segments=Path.arcsegments)
        
        # add this data to the curve
        self.curve.extend(newarc)
        self.points.extend(newpoint)
        self.controls.extend(newcontrol)


    # quadratic bezier method for the arc segments
    @staticmethod
    def calcNew(p0, p1, p2, segments):
        segarcs = []
        for i in range(0, segments):
            t = (i)/(segments-1)
            l0 = [ ((1-t)*p0[0]) + (t*p1[0]),
                   ((1-t)*p0[1]) + (t*p1[1]),
                   ((1-t)*p0[2]) + (t*p1[2]) ]
            l1 = [ ((1-t)*p1[0]) + (t*p2[0]),
                   ((1-t)*p1[1]) + (t*p2[1]),
                   ((1-t)*p1[2]) + (t*p2[2]) ]
            vert = [ ((1-t)*l0[0]) + (t*l1[0]),
                     ((1-t)*l0[1]) + (t*l1[1]),
                     ((1-t)*l0[2]) + (t*l1[2]) ]
            segarcs.extend(vert)

        return segarcs

    # upload the vertex data of the path to buffers
    @staticmethod
    def bufferObject(vao, vbo, garray):
        glBindVertexArray(vao)  # bind the given vao
        
        glBindBuffer(GL_ARRAY_BUFFER, vbo)  # bind given buffer
        glBufferData(GL_ARRAY_BUFFER, glm.sizeof(garray), garray.ptr, GL_STATIC_DRAW)   # upload all data
        
        # vao attribute for position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # unbind all
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


    # delete buffer data and vao
    def __del__(self):
        glDeleteVertexArrays(3, (self.pathvao, self.pointsvao, self.controlsvao))
        glDeleteBuffers(3, (self.pathvbo, self.pointsvbo, self.controlsvbo))