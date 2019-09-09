//
//  seeds.hpp
//  test_polygon
//
//  Created by asd on 03/09/2019.
//  Copyright © 2019 voicesync. All rights reserved.
//

#ifndef seeds_hpp
#define seeds_hpp

#include "polyhedron.hpp"
#include "johnson.hpp"

class Seeds : public Polyhedron {
public:
    static Polyhedron tetrahedron() {
        return Polyhedron("T", {{1.0, 1.0, 1.0},  {1.0, -1.0, -1.0},  {-1.0, 1.0, -1.0}, {-1.0, -1.0, 1.0}},
        {{0, 1, 2}, {0, 2, 3}, {0, 3, 1}, {1, 3, 2}});
    }
    static Polyhedron cube() {
        return Polyhedron("C", {{0.707, 0.707, 0.707}, {-0.707, 0.707, 0.707},
            {-0.707, -0.707, 0.707}, {0.707, -0.707, 0.707},
            {0.707, -0.707, -0.707}, {0.707, 0.707, -0.707},
            {-0.707, 0.707, -0.707}, {-0.707, -0.707, -0.707}},
                          {{3, 0, 1, 2}, {3, 4, 5, 0}, {0, 5, 6, 1}, {1, 6, 7, 2},
                              {2, 7, 4, 3}, {5, 4, 7, 6}  });
    }
    static Polyhedron icosahedron(){
        return Polyhedron("I", {{0, 0, 1.176}, {1.051, 0, 0.526}, {0.324, 1.0, 0.525},
            {-0.851, 0.618, 0.526}, {-0.851, -0.618, 0.526}, {0.325, -1.0, 0.526},
            {0.851, 0.618, -0.526}, {0.851, -0.618, -0.526}, {-0.325, 1.0, -0.526},
            {-1.051, 0, -0.526}, {-0.325, -1.0, -0.526}, {0, 0, -1.176}
        }, {{0, 1, 2}, {0, 2, 3}, {0, 3, 4}, {0, 4, 5}, {0, 5, 1}, {1, 5, 7},
            {1, 7, 6}, {1, 6, 2}, {2, 6, 8}, {2, 8, 3}, {3, 8, 9}, {3, 9, 4},
            {4, 9, 10}, {4, 10, 5}, {5, 10, 7}, {6, 7, 11}, {6, 11, 8}, {7, 10, 11},
            {8, 11, 9}, {9, 11, 10}});
    }
    static Polyhedron octahedron() {
        return Polyhedron("O", {{0, 0, 1.414}, {1.414, 0, 0},
            {0, 1.414, 0}, {-1.414, 0, 0},
            {0, -1.414, 0}, {0, 0, -1.414}
        }, {{0, 1, 2}, {0, 2, 3}, {0, 3, 4}, {0, 4, 1},
            {1, 4, 5}, {1, 5, 2}, {2, 5, 3}, {3, 5, 4}
        });
    }
    static Polyhedron dodecahedron() {
        return Polyhedron("D", {{0, 0, 1.07047}, {0.713644, 0, 0.797878}, {-0.356822, 0.618, 0.797878},
            {-0.356822, -0.618, 0.797878}, {0.797878, 0.618034, 0.356822}, {0.797878, -0.618, 0.356822},
            {-0.934172, 0.381966, 0.356822}, {0.136294, 1.0, 0.356822}, {0.136294, -1.0, 0.356822},
            {-0.934172, -0.381966, 0.356822}, {0.934172, 0.381966, -0.356822},
            {0.934172, -0.381966, -0.356822}, {-0.797878, 0.618, -0.356822},
            {-0.136294, 1.0, -0.356822}, {-0.136294, -1.0, -0.356822},
            {-0.797878, -0.618034, -0.356822}, {0.356822, 0.618, -0.797878},
            {0.356822, -0.618, -0.797878}, {-0.713644, 0, -0.797878}, {0, 0, -1.07047}},
                          {{0, 1, 4, 7, 2}, {0, 2, 6, 9, 3}, {0, 3, 8, 5, 1},
                              {1, 5, 11, 10, 4}, {2, 7, 13, 12, 6}, {3, 9, 15, 14, 8},
                              {4, 10, 16, 13, 7}, {5, 8, 14, 17, 11}, {6, 12, 18, 15, 9},
                              {10, 11, 17, 19, 16}, {12, 13, 16, 19, 18}, {14, 15, 18, 19, 17}});
    }

    static Polyhedron pyramid(int n=4) {
        float theta = (2 * M_PI) / n; // pie angle
        float height = 1;
        
        Vertexes vertexes;
        Faces faces;
        
        for (int i=0; i<n; i++)
            vertexes.push_back(Vertex{-cosf(i * theta), -sinf(i * theta), -0.2});
        vertexes.push_back(Vertex{0, 0, height});  // apex

        faces.push_back(range(n - 1, 0, true));  // base
        for (auto i=0; i<n; i++)  // n triangular sides
            faces.push_back(Face{i, (i + 1) % n, n});
        
        return Polyhedron("Y"+to_string(n), vertexes, faces);
    }

    static Polyhedron prism(int n=4) {
        float   theta = (2. * M_PI) / n,  // pie angle
        h = sinf(theta / 2.);  // half-edge
        
        Vertexes vertexes;
        for (int i=0; i<n; i++) vertexes.push_back(Vertex{-cosf(i * theta), -sinf(i * theta), -h});
        for (int i=0; i<n; i++) vertexes.push_back(Vertex{-cosf(i * theta), -sinf(i * theta), h});
         // # vertex #'s 0 to n-1 around one face, vertex #'s n to 2n-1 around other
        
        Faces faces;
        faces.push_back(range(n-1, 0, true));
        faces.push_back(range(n, 2*n, false));
        for (int i=0; i<n; i++) faces.push_back(Face{i, (i + 1) % n, ((i + 1) % n) + n, i + n});

        
        return Polyhedron("P"+to_string(n), vertexes, faces);
    }

    static Polyhedron antiprism(int n=4) {
        float theta = (2. * M_PI) / n,  // pie angle
        h = sqrtf(1. - (4. / ((4. + (2. * cosf(theta / 2.))) - (2. * cosf(theta))))),
        r = sqrtf(1. - (h * h)),
        f = sqrtf((h * h) + powf(r * cosf(theta / 2), 2));
        // correction so edge midpoints (not vertexes) on unit sphere
        r = -r / f;
        h = -h / f;
        Vertexes vertexes;
        
        for (int i=0; i<n; i++)  vertexes.push_back(Vertex{ r * cosf(i * theta), r * sinf(i * theta), h});
        for (int i=0; i<n; i++)  vertexes.push_back(Vertex{ r * cosf((i + 0.5) * theta), r * sinf((i + 0.5) * theta), -h});

        Faces faces;
        faces.push_back(range(n - 1, 0, true));
        faces.push_back(range(n, (2 * n) - 1, true)); // top
        for (int i=0; i<n; i++) {  // 2n triangular sides
            faces.push_back(Face{i, (i + 1) % n, i + n});
            faces.push_back(Face{i, i + n, ((((n + i) - 1) % n) + n)});
        }
        
        return Polyhedron("A"+to_string(n), vertexes, faces);
    }
    
    static Polyhedron cupola(int n=3, float alpha=0, float height=0) {
        if (n < 2)  return Polyhedron();
        
        float s = 1.0, // alternative face/height scaling
        rb = s / 2 / sinf(M_PI / 2 / n),
        rt = s / 2 / sinf(M_PI / n);
        
        if (height == 0) height = (rb - rt);
        // set correct height for regularity for n=3,4,5
        if (n>=3 && n<=5)
            height = s * sqrtf(1 - 1 / 4 / sinf(M_PI / n) / sinf(M_PI / n));
        // init 3N vertexes
        Vertexes vertexes(n*3);
        
        // fill vertexes
        for (int i=0; i<n; i++) {
            vertexes[i * 2] = Vertex{rb * cosf(M_PI * (2 * i) / n + M_PI / 2 / n + alpha),
                rb * sinf(M_PI * (2 * i) / n + M_PI / 2 / n + alpha), 0.0};
            vertexes[2 * i + 1] = Vertex{rb * cosf(M_PI * (2 * i + 1) / n + M_PI / 2 / n - alpha),
                rb * sinf(M_PI * (2 * i + 1) / n + M_PI / 2 / n - alpha), 0.0};
            vertexes[2 * n + i] = Vertex{rt * cosf(2 * M_PI * i / n), rt * sinf(2 * M_PI * i / n), height};
        }
        
        Faces faces;
        faces.push_back(range(2 * n - 1, 0, true));
        faces.push_back(range(2 * n, 3 * n - 1, true));  // base, top
        for (int i=0; i<n; i++) { // n triangular sides and n square sides
            faces.push_back(Face{(2 * i + 1) % (2 * n), (2 * i + 2) % (2 * n), 2 * n + (i + 1) % n});
            faces.push_back(Face{2 * i, (2 * i + 1) % (2 * n), 2 * n + (i + 1) % n, 2 * n + i});
        }
        
        return Polyhedron("U"+to_string(n), vertexes, faces);
    }
    
    static Polyhedron anticupola(int n=3, float alpha=0, float height=0) {
        if (n < 3)  return Polyhedron();
        
        float s = 1.0,  // alternative face/height scaling
        rb = s / 2 / sinf(M_PI / 2 / n),
        rt = s / 2 / sinf(M_PI / n);
        
        if (height == 0) height = (rb - rt);
        
        // init 3N vertexes
        Vertexes vertexes(n * 3);
        
        // fill vertexes
        for (int i=0; i<n; i++) {
            vertexes[2 * i] = Vertex{rb * cosf(M_PI * (2 * i) / n + alpha), rb * sinf(M_PI * (2 * i) / n + alpha), 0.0};
            vertexes[2 * i + 1] = Vertex{rb * cosf(M_PI * (2 * i + 1) / n - alpha), rb * sinf(M_PI * (2 * i + 1) / n - alpha), 0.0};
            vertexes[2 * n + i] = Vertex{rt * cosf(2 * M_PI * i / n), rt * sinf(2 * M_PI * i / n), height};
        }
        // create faces
        Faces faces;
        faces.push_back(range(2 * n - 1, 0, true));
        faces.push_back(range(2 * n, 3 * n - 1, true));  // base
        for (int i=0; i<n; i++){ // n triangular sides and n square sides
            faces.push_back(Face{(2 * i) % (2 * n), (2 * i + 1) % (2 * n), 2 * n + (i) % n});
            faces.push_back(Face{2 * n + (i + 1) % n, (2 * i + 1) % (2 * n), (2 * i + 2) % (2 * n)});
            faces.push_back(Face{2 * n + (i + 1) % n, 2 * n + (i) % n, (2 * i + 1) % (2 * n)});
        }
        
        return Polyhedron("U"+to_string(n), vertexes, faces);
    }
    
    static Polyhedron johnson(int j) {
        auto ffv=johnsons.find(j);
        
        if (ffv==johnsons.end()) return Polyhedron(); // not found -> return empty poly
        
        auto fv=ffv->second; // map value {faces, vertexes}
        return Polyhedron("J"+to_string(j), fv.second, fv.first);
    }

    static Polyhedron polyhedron(char name='T', int n=0, float alpha=0, float height=0) {
        switch (name) {
        case 'T': return tetrahedron();
        case 'C': return cube();
        case 'I': return icosahedron();
        case 'O': return octahedron();
        case 'D': return dodecahedron();
        case 'P': return prism(n);
        case 'A': return antiprism(n);
        case 'U': return cupola(n, alpha, height);
        case 'X': return anticupola(n, alpha, height);
        case 'J': return johnson(n);
        default: return Polyhedron();
        }
    }
    
public: // utils
    
    static void print_all() {
        const int n=10;
        for (auto p:{tetrahedron, cube, icosahedron, octahedron, dodecahedron}) p().print();
        for (auto p:{pyramid, prism, antiprism}) p(n).print();
        for (auto p:{cupola, anticupola}) p(n,0,0).print();
        for (int i=0; i<92; i++) johnson(i+1).print();
    }
    
private:

    static Face range(int left, int right, bool inclusive) {
        Face range;
        bool ascending = left < right;
        int end = !inclusive ? right : (ascending ? right+1 : right-1);
        for (int i = left; (ascending ? i < end : i > end); ascending ? i++ : i--)
            range.push_back(i);
        return range;
    }
};

#endif /* seeds_hpp */
