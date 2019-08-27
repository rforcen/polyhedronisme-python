from Poly_Data import getPolyData, get_poly
from seeds import prism, antiprism, tetrahedron, cube, icosahedron, octahedron, dodecahedron

if __name__=='__main__':
    def test_poly_data():
        for p in getPolyData():
            name, faces, coords = get_poly(p)
            print(f'name: {name:60}, #coords: {len(faces):3}, #faces: {len(coords):3}', end='')
            # traverse faces
            for face in faces:
                for ic in face:
                    c = coords[ic]
            print(' -> ok')

    # test_poly_data()
    p=prism(12)
    print('ok' if p.traverse() else 'bad poly')
    p=antiprism(20)
    print('ok' if p.traverse() else 'bad poly')

    print(p.name, p.faces, p.vertices, sep='\n\n')

