'''
basic Qt gl renderer
'''
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtWidgets import (QOpenGLWidget)


class RendererGL(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)
    zoom = -10

    def __init__(self, parent=None):
        super(RendererGL, self).__init__(parent)

        self.object = self.xRot = self.yRot = self.zRot = 0
        self.lastPos = QPoint()

    # virtuals: implement init & draw in derived class
    def draw(self, gl):
        pass

    def init(self, gl):
        pass

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.gl.glShadeModel(self.gl.GL_FLAT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        # self.gl.glEnable(self.gl.GL_CULL_FACE)

        self.init(self.gl)  # call user init

    def paintGL(self):
        self.gl.glClear(
            self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glClearColor(0, 0, 0, 1)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(0, 0, self.zoom)
        self.gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        self.gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        self.gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        self.draw(self.gl)  # user draw

    def resizeGL(self, width, height):
        side = min(width, height)
        if side <= 0: return
        aspectRatio = width / height if height != 0 else 1

        self.gl.glViewport(0, 0, side, side)
        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()

        d=0.5
        if (width >= height): # keep aspect ratio
            self.gl.glOrtho(-d * aspectRatio, +d * aspectRatio, +d, -d, 6.0, 150.0)
        else:
            self.gl.glOrtho(-d, +d, +d, -d, 4.0 / aspectRatio, 150.0)

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def sceneInit(self, gl):
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [1.0, 1.0, 1.0, 0.0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, [1, 1, 1, 0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1, 0.5, 1, 0])
        gl.glEnable(gl.GL_LIGHT0)

        gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, [1.0, 1.0, 1.0, 0.0])
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_SPECULAR, [1, 1, 1, 0])
        gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, [-1, 0.5, -1, 0])
        gl.glEnable(gl.GL_LIGHT1)

        gl.glLightModelfv(gl.GL_LIGHT_MODEL_TWO_SIDE, [gl.GL_FALSE])
        gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, [0, 0, 0, 0])
        gl.glEnable(gl.GL_LIGHTING)

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, [0, 0, 0, 1])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, [40])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [1, 1, 1, 0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, [1, 0, 0, 0])

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glCullFace(gl.GL_FRONT)

        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
