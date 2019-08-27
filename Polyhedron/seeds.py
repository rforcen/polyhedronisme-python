from math import pi, sin, cos, sqrt
from polyhedron import polyhedron
from johnson_solids import johnson_poly


def __range__(left, right, inclusive):
    range = []
    ascending = left < right
    end = right if not inclusive else (right + 1 if ascending else right - 1)
    i = left
    while (i < end if ascending else i > end):
        range.append(i)
        i = i + 1 if ascending else i - 1
    return range


def prism(n):
    theta = (2 * pi) / n  # pie angle
    h = sin(theta / 2)  # half-edge

    vertices = [[-cos(i * theta), -sin(i * theta), -h] for i in range(n)] + \
               [[-cos(i * theta), -sin(i * theta), h] for i in
                range(n)]  # # vertex #'s 0 to n-1 around one face, vertex #'s n to 2n-1 around other

    faces = [[i, (i + 1) % n, ((i + 1) % n) + n, i + n] for i in range(n)] + \
            [__range__(n - 1, 0, True)] + [__range__(n, 2 * n, False)]

    # poly = adjustXYZ(poly, 1)
    return polyhedron(name=f'P{n}', vertices=vertices, faces=faces)


def antiprism(n):
    theta = (2 * pi) / n  # pie angle
    h = sqrt(1 - (4 / ((4 + (2 * cos(theta / 2))) - (2 * cos(theta)))))
    r = sqrt(1 - (h * h))
    f = sqrt((h * h) + pow(r * cos(theta / 2), 2))
    # correction so edge midpoints (not vertices) on unit sphere
    r = -r / f
    h = -h / f

    vertices = [[r * cos(i * theta), r * sin(i * theta), h] for i in range(n)] + \
               [[r * cos((i + 0.5) * theta), r * sin((i + 0.5) * theta), -h] for i in range(n)]

    faces = [__range__(n - 1, 0, True)] + [__range__(n, (2 * n) - 1, True)]  # top
    for i in range(n):  # 2n triangular sides
        faces.append([i, (i + 1) % n, i + n])
        faces.append([i, i + n, ((((n + i) - 1) % n) + n)])

    # poly = adjustXYZ(poly, 1)
    return polyhedron(name=f'A{n},', vertices=vertices, faces=faces)


def pyramid(n):
    theta = (2 * pi) / n  # pie angle
    height = 1

    vertices = [[-cos(i * theta), -sin(i * theta), -0.2] for i in range(n)]
    vertices.append([0, 0, height])  # apex
    faces = [__range__(n - 1, 0, True)]  # base
    for i in range(n):  # n triangular sides
        faces.append([i, (i + 1) % n, n])

    # poly = canonicalXYZ(poly, 3)
    return polyhedron(name=f'Y{n}', vertices=vertices, faces=faces)


def tetrahedron():
    return polyhedron('T', [[1.0, 1.0, 1.0],
                            [1.0, -1.0, -1.0],
                            [-1.0, 1.0, -1.0],
                            [-1.0, -1.0, 1.0]],
                      [[0, 1, 2], [0, 2, 3],
                       [0, 3, 1], [1, 3, 2]]
                      )


def octahedron():
    return polyhedron('O', [[0, 0, 1.414], [1.414, 0, 0],
                            [0, 1.414, 0], [-1.414, 0, 0],
                            [0, -1.414, 0], [0, 0, -1.414]
                            ], [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1],
                                [1, 4, 5], [1, 5, 2], [2, 5, 3], [3, 5, 4]
                                ])


def cube():
    return polyhedron('C', [[0.707, 0.707, 0.707], [-0.707, 0.707, 0.707],
                            [-0.707, -0.707, 0.707], [0.707, -0.707, 0.707],
                            [0.707, -0.707, -0.707], [0.707, 0.707, -0.707],
                            [-0.707, 0.707, -0.707], [-0.707, -0.707, -0.707]],
                      [[3, 0, 1, 2], [3, 4, 5, 0], [0, 5, 6, 1], [1, 6, 7, 2],
                       [2, 7, 4, 3], [5, 4, 7, 6]
                       ])


def icosahedron():
    return polyhedron('I', [[0, 0, 1.176], [1.051, 0, 0.526], [0.324, 1.0, 0.525],
                            [-0.851, 0.618, 0.526], [-0.851, -0.618, 0.526], [0.325, -1.0, 0.526],
                            [0.851, 0.618, -0.526], [0.851, -0.618, -0.526], [-0.325, 1.0, -0.526],
                            [-1.051, 0, -0.526], [-0.325, -1.0, -0.526], [0, 0, -1.176]
                            ], [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 1], [1, 5, 7],
                                [1, 7, 6], [1, 6, 2], [2, 6, 8], [2, 8, 3], [3, 8, 9], [3, 9, 4],
                                [4, 9, 10], [4, 10, 5], [5, 10, 7], [6, 7, 11], [6, 11, 8], [7, 10, 11],
                                [8, 11, 9], [9, 11, 10]])


def dodecahedron():
    return polyhedron('D', [[0, 0, 1.07047], [0.713644, 0, 0.797878], [-0.356822, 0.618, 0.797878],
                            [-0.356822, -0.618, 0.797878], [0.797878, 0.618034, 0.356822], [0.797878, -0.618, 0.356822],
                            [-0.934172, 0.381966, 0.356822], [0.136294, 1.0, 0.356822], [0.136294, -1.0, 0.356822],
                            [-0.934172, -0.381966, 0.356822], [0.934172, 0.381966, -0.356822],
                            [0.934172, -0.381966, -0.356822], [-0.797878, 0.618, -0.356822],
                            [-0.136294, 1.0, -0.356822], [-0.136294, -1.0, -0.356822],
                            [-0.797878, -0.618034, -0.356822], [0.356822, 0.618, -0.797878],
                            [0.356822, -0.618, -0.797878], [-0.713644, 0, -0.797878], [0, 0, -1.07047]],
                      [[0, 1, 4, 7, 2], [0, 2, 6, 9, 3], [0, 3, 8, 5, 1],
                       [1, 5, 11, 10, 4], [2, 7, 13, 12, 6], [3, 9, 15, 14, 8],
                       [4, 10, 16, 13, 7], [5, 8, 14, 17, 11], [6, 12, 18, 15, 9],
                       [10, 11, 17, 19, 16], [12, 13, 16, 19, 18], [14, 15, 18, 19, 17]])


def cupola(n, alpha, height):
    if n is None: n = 3
    if alpha is None: alpha = 0.0

    if n < 2:
        return polyhedron()

    s = 1.0  # alternative face/height scaling
    rb = s / 2 / sin(pi / 2 / n - alpha)
    rb = s / 2 / sin(pi / 2 / n)
    rt = s / 2 / sin(pi / n)

    if height is None:
        height = (rb - rt)
        # set correct height for regularity for n=3,4,5
        if 2 <= n <= 5:
            height = s * sqrt(1 - 1 / 4 / sin(pi / n) / sin(pi / n))
    # init 3N vertices
    vertices = [[0, 0, 0]] * (n * 3)

    # fill vertices
    for i in range(n):
        vertices[i * 2] = [rb * cos(pi * (2 * i) / n + pi / 2 / n + alpha),
                           rb * sin(pi * (2 * i) / n + pi / 2 / n + alpha), 0.0]
        vertices[2 * i + 1] = [rb * cos(pi * (2 * i + 1) / n + pi / 2 / n - alpha),
                               rb * sin(pi * (2 * i + 1) / n + pi / 2 / n - alpha), 0.0]
        vertices[2 * n + i] = [rt * cos(2 * pi * i / n), rt * sin(2 * pi * i / n), height]

    faces = [__range__(2 * n - 1, 0, True)] + [__range__(2 * n, 3 * n - 1, True)]  # base, top
    for i in range(n):  # n triangular sides and n square sides
        faces.append([(2 * i + 1) % (2 * n), (2 * i + 2) % (2 * n), 2 * n + (i + 1) % n])
        faces.append([2 * i, (2 * i + 1) % (2 * n), 2 * n + (i + 1) % n, 2 * n + i])

    return polyhedron(name=f'U{n}', vertices=vertices, faces=faces)


def anticupola(n, alpha, height):
    if n is None: n = 3
    if alpha is None: alpha = 0.0

    if n < 3:
        return polyhedron()

    s = 1.0  # alternative face/height scaling
    rb = s / 2 / sin(pi / 2 / n - alpha)
    rb = s / 2 / sin(pi / 2 / n)
    rt = s / 2 / sin(pi / n)

    if height is None:
        height = (rb - rt)

    # init 3N vertices
    vertices = [[0, 0, 0]] * (n * 3)

    # fill vertices
    for i in range(n):
        vertices[2 * i] = [rb * cos(pi * (2 * i) / n + alpha), rb * sin(pi * (2 * i) / n + alpha), 0.0]
        vertices[2 * i + 1] = [rb * cos(pi * (2 * i + 1) / n - alpha), rb * sin(pi * (2 * i + 1) / n - alpha), 0.0]
        vertices[2 * n + i] = [rt * cos(2 * pi * i / n), rt * sin(2 * pi * i / n), height]

    faces = [__range__(2 * n - 1, 0, True)] + [__range__(2 * n, 3 * n - 1, True)]  # base
    for i in range(n):  # n triangular sides and n square sides
        faces.append([(2 * i) % (2 * n), (2 * i + 1) % (2 * n), 2 * n + (i) % n])
        faces.append([2 * n + (i + 1) % n, (2 * i + 1) % (2 * n), (2 * i + 2) % (2 * n)])
        faces.append([2 * n + (i + 1) % n, 2 * n + (i) % n, (2 * i + 1) % (2 * n)])

    return polyhedron(name=f'U{n}', vertices=vertices, faces=faces)
