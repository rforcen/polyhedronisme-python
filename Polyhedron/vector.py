from math import sqrt, floor, log10


class vector():
    x, y, z = 0, 0, 0

    def __init__(self, v: list):
        self.x, self.y, self.z = v[0], v[1], v[2]

    def __sub__(self, b):
        return vector([self.x - b.x, self.y - b.y, self.z - b.z])

    def __add__(self, b):
        return vector([self.x + b.x, self.y + b.y, self.z + b.z])

    def div(self, d):
        if d != 0:
            self.x /= d
            self.y /= d
            self.z /= d
        return self

    def mult(self, c):
        self.x *= c
        self.y *= c
        self.z *= c
        return self

    def cross(self, b):
        return vector([(self.y * b.z) - (self.z * b.y),
                       (self.z * b.x) - (self.x * b.z),
                       (self.x * b.y) - (self.y * b.x)])

    def length(self):
        def sqr(x): return x * x

        return sqrt(sqr(self.x) + sqr(self.y) + sqr(self.z))

    def normalize(self):
        self.div(self.length())
        return self

    def list(self):
        return [self.x, self.y, self.z]

    def normal(v0, v1, v2):
        return vector.cross(vector(v0) - vector(v1), vector(v2) - vector(v1)).normalize()

    def normal_vertex(v: list):
        return vector.normal(v[0], v[1], v[2])

    def dot(v0, v1):
        return v1.x * v0.x + v1.y * v0.y + v1.z * v0.z

    def mag(self):
        return sqrt(vector.dot(self, self))

    def mag2(self):
        return vector.dot(self, self)

    def sigfigs(N, nsigs=2) -> int:  # returns string w. nsigs digits ignoring magnitude
        mantissa = N / pow(10, floor(log10(N)))
        return round(mantissa * pow(10, (nsigs - 1)))


if __name__ == '__main__':
    print(vector.sigfigs(0.123123, 2))
