import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from rendererGL import RendererGL

from seeds import prism, antiprism, tetrahedron, cube, icosahedron, octahedron, dodecahedron, johnson_poly, cupola, \
    anticupola
from transform import transform
from vector import vector
from color import color


class PolyhedronGL_widget(RendererGL):
    poly = None

    n_func, resolution, color_map = 16, 750, 13

    color_bronze = (200, 132, 102)

    scale = 0.3
    main_window = None

    def __init__(self, main_window, poly):
        super(PolyhedronGL_widget, self).__init__()

        self.main_window = main_window
        self.poly = poly

        self.setFocusPolicy(Qt.StrongFocus)  # accepts key events

    def init(self, gl):
        self.sceneInit(gl)
        gl.glCullFace(gl.GL_FRONT)
        gl.glEnable(gl.GL_RESCALE_NORMAL)
        gl.glColor3ubv(self.color_bronze)  # for all render

    def draw(self, gl):
        def draw_centers(gl):
            gl.glPointSize(8)
            gl.glColor3fv(self.color_bronze)

            gl.glBegin(gl.GL_POINTS)
            for ic, _ in enumerate(self.poly.faces):
                gl.glVertex3fv(self.poly.centersArray[ic])
            gl.glEnd()

        def draw_faces(gl):
            for ic, face in enumerate(self.poly.faces):
                gl.glBegin(gl.GL_POLYGON)
                normal = self.poly.normals[ic]  # 1 normal per face
                gl.glColor3fv(self.poly.colors[ic])  # face color
                for ic in face:
                    gl.glVertex3fv(self.poly.vertices[ic])
                    gl.glNormal3fv(normal)
                gl.glEnd()

        gl.glScalef(self.scale, self.scale, self.scale)
        draw_faces(gl)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.deleteLater()
        elif event.key() == Qt.Key_Plus:
            color.set_random()
            self.poly.update_colors()
            self.update()
        event.accept()


class Main(QMainWindow):
    def __init__(self, poly, *args):
        super(Main, self).__init__(*args)

        self.setWindowTitle(f'Polyhedron {poly.name}')
        self.setCentralWidget(PolyhedronGL_widget(self, poly))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Main(transform.propellor(transform.kisN(dodecahedron(),0,0.1)))
    app.exec_()
