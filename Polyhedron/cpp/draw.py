import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from np.rendererGL import RendererGL
from cpp.polyhedron import parse


class PolyhedronGL_widget(RendererGL):
    poly_str = None
    name = vertexes = faces = normals = areas = centers = None

    n_func, resolution, color_map = 16, 750, 13

    color_bronze = (200, 132, 102)

    scale = 0.6
    main_window = None

    needs_compile = True
    gl_compiled_list = 1

    def __init__(self, main_window, poly_str):
        super(PolyhedronGL_widget, self).__init__()

        self.main_window = main_window
        self.poly_str = poly_str

        self.setFocusPolicy(Qt.StrongFocus)  # accepts key events

        self.create_poly()

    def init(self, gl):
        self.sceneInit(gl)
        gl.glCullFace(gl.GL_FRONT)
        gl.glEnable(gl.GL_RESCALE_NORMAL)
        gl.glColor3ubv(self.color_bronze)  # for all render

    def create_poly(self):
        print('generating poly...', end='')
        self.name, self.vertexes, self.faces, self.normals, self.colors, self.areas, self.centers = parse(
            self.poly_str)  # polyhedron(self.poly_def)
        print(f'done!, # vertexes:{len(self.vertexes)}, # faces:{len(self.faces)}')

    def draw(self, gl):
        def draw_centers(gl):
            gl.glPointSize(8)
            gl.glColor3fv(self.color_bronze)

            gl.glBegin(gl.GL_POINTS)
            for ic, _ in enumerate(self.poly.faces):
                gl.glVertex3fv(self.poly.centersArray[ic])
            gl.glEnd()

        def draw_faces(gl):
            gl.glEnable(gl.GL_RESCALE_NORMAL)
            gl.glScalef(self.scale, self.scale, self.scale)
            for ic, face in enumerate(self.faces):
                gl.glBegin(gl.GL_POLYGON)
                normal = self.normals[ic]  # 1 normal per face
                gl.glColor3fv(self.colors[ic])  # face color
                for ic in face:
                    gl.glVertex3fv(self.vertexes[ic])
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

        if self.name is not None:
            draw_list(gl)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.deleteLater()
        elif event.key() == Qt.Key_Plus:
            self.create_poly()
            self.needs_compile = True
            self.update()
        event.accept()


class Main(QMainWindow):
    def __init__(self, poly_str, *args):
        super(Main, self).__init__(*args)

        self.setWindowTitle(f'Polyhedron {poly_str}')
        self.setCentralWidget(PolyhedronGL_widget(self, poly_str))
        self.show()


def main():
    app = QApplication(sys.argv)
    Main('cxdO')

    app.exec_()


if __name__ == '__main__':
    main()
