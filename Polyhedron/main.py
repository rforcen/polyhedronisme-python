import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from rendererGL import RendererGL

from seeds import prism, antiprism, tetrahedron, cube, icosahedron, octahedron, dodecahedron, johnson_poly, cupola, \
    anticupola
from transform import transform
from color import color
import polyhedron
import parser


class PolyhedronGL_widget(RendererGL):
    poly = None

    n_func, resolution, color_map = 16, 750, 13

    color_bronze = (200, 132, 102)

    scale = 0.3
    main_window = None

    needs_compile = True
    gl_compiled_list = 1

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
            gl.glScalef(self.scale, self.scale, self.scale)
            for ic, face in enumerate(self.poly.faces):
                gl.glBegin(gl.GL_POLYGON)
                normal = self.poly.normals[ic]  # 1 normal per face
                gl.glColor3fv(self.poly.colors[ic])  # face color
                for ic in face:
                    gl.glVertex3fv(self.poly.vertices[ic])
                    gl.glNormal3fv(normal)
                gl.glEnd()

        def compile(gl):
            if self.needs_compile:
                gl.glNewList(self.gl_compiled_list, gl.GL_COMPILE)

                draw_faces(gl)

                gl.glEndList()
                self.needs_compile = False

        def draw_list(gl):
            compile(gl)
            gl.glCallList(self.gl_compiled_list)

        draw_list(gl)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.deleteLater()
        elif event.key() == Qt.Key_Plus:
            color.set_random()
            self.poly.update_colors()
            self.needs_compile = True
            self.update()
        event.accept()


class Main(QMainWindow):
    def __init__(self, poly, *args):
        super(Main, self).__init__(*args)

        self.setWindowTitle(f'Polyhedron {poly.name}')
        self.setCentralWidget(PolyhedronGL_widget(self, poly))
        self.show()


def test():  # fixed transformation
    app = QApplication(sys.argv)

    p = transform.scale(transform.hollow(transform.quinto(transform.quinto(transform.quinto((johnson_poly(89)))))))
    # p=dodecahedron()
    # p = transform.scale(transform.chamfer(dodecahedron()))
    Main(p)

    app.exec_()


def main(poly_def: str) -> polyhedron:
    p = parser.parse(poly_def)

    if p is None:
        print(f'syntax error in {poly_def}')
    else:

        app = QApplication(sys.argv)
        Main(p)

        app.exec_()


if __name__ == '__main__':
    main('wpD')
