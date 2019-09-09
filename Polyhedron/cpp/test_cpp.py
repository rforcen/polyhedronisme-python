from polyhedron import tetrahedron, cube, octahedron, icosahedron, dodecahedron, pyramid, prism, antiprism, johnson, \
    polyhedron, parse
import py.seeds
'''
[3.464101552963257, 3.464101552963257, 3.464101552963257, 3.464101552963257]
'''

name, vertexes, faces, normals, colors, areas, centers = parse('dI')  # name, n, alpha, heigth
print(name, vertexes, faces, normals, colors, areas, centers, sep='\n\n', end=f'\n{"-"*90}\n')
exit(1)


name, vertexes, faces, normals, colors, areas, centers = polyhedron(['T', 2, 0.1, 0.2])  # name, n, alpha, heigth
print(name, vertexes, faces, normals, colors, areas, centers, sep='\n\n', end=f'\n{"-"*90}\n')
exit(1)
p= py.seeds.tetrahedron()
print(p.name, p.vertices,  p.faces, p.normals, p.colors, p.areas, p.centers, sep='\n')

exit(1)

for p in [tetrahedron, cube, octahedron, icosahedron, dodecahedron, pyramid, prism, antiprism, johnson]:
    name, vertexes, faces, normals, colors, areas, centers = p()
    print(name, vertexes, faces, normals, colors, areas, centers, sep='\n\n', end=f'\n{"-"*90}\n')

for j in range(1, 92):
    name, vertexes, faces, normals, colors, areas, centers = johnson(j)
    print(name, vertexes, faces, normals, colors, areas, centers, sep='\n\n', end=f'\n{"-"*90}\n')
