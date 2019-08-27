from vector import vector
from color import color


class polyhedron():
    name = ''
    vertices = []
    faces = []
    normals = []
    areas = []
    colors = []
    centersArray = []

    def __init__(self, name='', vertices=[], faces=[]):
        if vertices != []:
            self.name = name
            self.vertices = vertices
            # self.scale_vertices()
            self.faces = faces

            self.normals = [vector.normal(self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]]).list()
                            for
                            face in self.faces]  # face normal
            self.areas = [self.planararea(f) for f in self.faces]  # face area

            self.calc_colors()
            self.centers()

    def scale_vertices(self):
        _max = max(max(self.vertices))
        _min = min(min(self.vertices))
        diff = abs(_max - _min)
        for iv, v in enumerate(self.vertices):
            for ic, c in enumerate(v):
                self.vertices[iv][ic] = self.vertices[iv][ic] / diff

    def calc_colors(self):
        color_dict = {}  # generate color dict
        for a in self.areas:
            k = vector.sigfigs(a)
            if k not in color_dict:
                color_dict[k] = color.hextofloats(color.get_item(len(color_dict)))
        self.colors = [color_dict[vector.sigfigs(a)] for a in self.areas]

    def update_colors(self):
        self.calc_colors()

    def planararea(self, face):
        vsum = vector([0., 0., 0.])
        vertices = [self.vertices[ic] for ic in face]
        v1, v2 = vector(vertices[-2]), vector(vertices[-1])
        for v3 in vertices:
            vsum = vsum + v1.cross(v2)
            v1, v2 = v2, vector(v3)
        return abs(vector.dot(vector.normal_vertex(vertices), vsum) / 2.)

    def centers(self):
        self.centersArray = []
        for face in self.faces:
            fcenter = vector([0, 0, 0])
            for vidx in face:  # average vertex coords
                fcenter = fcenter + vector(self.vertices[vidx])
            self.centersArray.append(fcenter.mult(1.0 / len(face)).list())
        # return face - ordered array  of  centroids
        return self.centersArray

    def traverse(self):
        for face in self.faces:
            for ic in face:
                if ic < len(self.vertices):
                    c = self.vertices[ic]
                else:
                    return False
        return True


class polyflag():
    MAX_FACE_SIDEDNESS = 1000  # GLOBAL

    def __init__(self):
        self.flags = {}  # flags[face][vertex] = next vertex of flag symbolic triples
        self.vertidxs = {}  # [symbolic names] holds vertex index
        self.vertices = {}  # XYZ coordinates

    def newV(self, vertName, coordinates):  # Add a new vertex named "name" with coordinates "xyz".
        if vertName not in self.vertidxs:
            self.vertidxs[vertName] = 0
            self.vertices[vertName] = coordinates

    def newFlag(self, faceName, vertName1, vertName2):
        if faceName not in self.flags:
            self.flags[faceName] = {}
        self.flags[faceName][vertName1] = vertName2

    def topoly(self):

        vertices, faces = [], []

        for ctr, i in enumerate(self.vertidxs):
            vertices.append(self.vertices[i])  # store in array
            self.vertidxs[i] = ctr

        for ctr, i in enumerate(self.flags):
            face = self.flags[i]
            faces.append([])  # new face
            # grab _any_ vertex as starting point
            for j in face:
                v0 = face[j]
                break

            # build face out of all the edge relations in the flag assoc array
            v = v0  # v moves around face
            faces[ctr].append(self.vertidxs[v])  # record index
            v = self.flags[i][v]  # goto next vertex
            faceCTR = 0
            while v is not v0:  # loop until back to start
                faces[ctr].append(self.vertidxs[v])
                v = self.flags[i][v]
                faceCTR += 1
                # necessary during development to prevent browser hangs on badly formed flagsets
                if faceCTR > self.MAX_FACE_SIDEDNESS:
                    print("Bad flag spec, have a neverending face:", i, self.flags[i])
                    break

        return polyhedron(name='unknown polyhedron', vertices=vertices, faces=faces)


if __name__ == '__main__':
    import seeds

    p = seeds.prism(12)
    print(p.colors)
