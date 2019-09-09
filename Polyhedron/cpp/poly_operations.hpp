//
//  poly_operations.hpp
//  test_polygon
//
//  Created by asd on 05/09/2019.
//  Copyright © 2019 voicesync. All rights reserved.
//

#ifndef poly_operations_hpp
#define poly_operations_hpp

#include "common.hpp"
#include "polyhedron.hpp"
#include "polyflag.hpp"

//===================================================================================================
// Polyhedron Operators
//===================================================================================================
// for each vertex of new polyhedron:
//     call newV(Vname, xyz) with a symbolic name and coordinates
// for each flag of new polyhedron:
//     call newFlag(Fname, Vname1, Vname2) with a symbolic name for the new face
//     and the symbolic name for two vertices forming an oriented edge
// ORIENTATION -must- be dealt with properly to make a manifold (correct) mesh.
// Specifically, no edge v1->v2 can ever be crossed in the -same direction- by
// two different faces
//
// call topoly() to assemble flags into polyhedron structure by following the orbits
// of the vertex mapping stored in the flagset for each new face
//
// set name as appropriate

class PolyOperations {
public:
    
    // Kis(N)
    // ------------------------------------------------------
    // Kis (abbreviated from triakis) transforms an N-sided face into an N-pyramid rooted at the
    // same base vertices.
    // only kis n-sided faces, but n==0 means kis all.
    //
    static  Polyhedron kisN(Polyhedron poly, int n=0, float apexdist=0.1) {
        
        Polyflag flag;
        
        for (size_t i = 0; i < poly.n_vertex; i++) // each old vertex is a new vertex
            flag.newV(to_string(i), poly.vertexes[i]);
        
        auto normals = poly.get_normals();
        auto centers = poly.get_centers();
        
        bool foundAny = false;
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            string v1 = to_string(f.back()); // last item
            
            for (auto &v : f) {
                string v2 = to_string(v);
                if (f.size() == (size_t)n || n == 0) {
                    foundAny = true;
                    string apex = "apex"+to_string(i);
                    string fname = to_string(i) + v1;
                    // new vertices in centers of n-sided face
                    flag.newV(apex, centers[i] + (normals[i] * apexdist));
                    flag.newFlag(fname,   v1,   v2); // the old edge of original face
                    flag.newFlag(fname,   v2, apex); // up to apex of pyramid
                    flag.newFlag(fname, apex,   v1); // and back down again
                } else {
                    flag.newFlag(to_string(i), v1, v2);  // same old flag, if non-n
                }
                // current becomes previous
                v1 = v2;
            }
        }
        
        if (!foundAny) printf("kisN: No %d-fold components were found.\n", n);
        
        auto newpoly = flag.topoly();
        newpoly.name = "k" + (n ? to_string(n):"") + poly.name;
        return newpoly;
    };
    
    
    // Ambo
    // ------------------------------------------------------
    // The best way to think of the ambo operator is as a topological "tween" between a polyhedron
    // and its dual polyhedron.  Thus the ambo of a dual polyhedron is the same as the ambo of the
    // original. Also called "Rectify".
    //
    static Polyhedron ambo(Polyhedron poly) {
        Polyflag flag;
        
        // For each face f in the original poly
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto flen=f.size();
            
            auto v1=f[flen-2], v2=f[flen-1]; //  [v1, v2] = f.slice(-2);
            
            for (auto &v3 : f) {
                if (v1 < v2)  // vertices are the midpoints of all edges of original poly
                    flag.newV(midName(v1,v2), midpoint(poly.vertexes[v1], poly.vertexes[v2]));
                
                // two new flags:
                // One whose face corresponds to the original f:
                flag.newFlag("orig"+to_string(i),  midName(v1,v2), midName(v2,v3));
                // Another flag whose face  corresponds to (the truncated) v2:
                flag.newFlag("dual"+to_string(v2), midName(v2,v3), midName(v1,v2));
                // shift over one
                v1=v2; v2=v3;
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "a"+poly.name;
        return newpoly;
    }
    
    // Gyro
    // -------------------------------------------------------
    // This is the dual operator to "snub", i.e dual*Gyro = Snub.  It is a bit easier to implement
    // this way.
    //
    // Snub creates at each vertex a new face, expands and twists it, and adds two new triangles to
    // replace each edge.
    
    static Polyhedron gyro(Polyhedron poly) {
        Polyflag flag;
        
        for (size_t i = 0; i < poly.n_vertex; i++) // each old vertex is a new vertex
            flag.newV("v"+i2s(i), unit(poly.vertexes[i]));
        
        
        Vertexes centers = poly.get_centers(); // new vertices in center of each face
        for (size_t i = 0; i < poly.n_faces; i++)
            flag.newV("center"+i2s(i), unit(centers[i]));
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto flen=f.size();
            
            auto v1=f[flen-2], v2=f[flen-1]; //  [v1, v2] = f.slice(-2);
            
            for (size_t j = 0; j < flen; j++) {
                auto sv1=i2s(v1), sv2=i2s(v2), si=i2s(i);
                auto v = f[j];
                auto v3 = v;
                auto sv3=i2s(v3);
                
                flag.newV(sv1+"~"+sv2, oneThird(poly.vertexes[v1], poly.vertexes[v2]));  // new v in face
                
                auto fname = si+"f"+sv1;
                flag.newFlag(fname, "center"+si,      sv1+"~"+sv2); // five new flags
                flag.newFlag(fname, sv1+"~"+sv2,  sv2+"~"+sv1);
                flag.newFlag(fname, sv2+"~"+sv1,  "v"+sv2);
                flag.newFlag(fname, "v"+sv2,     sv2+"~"+sv3);
                flag.newFlag(fname, sv2+"~"+sv3,  "center"+si);
                // shift over one
                v1=v2; v2=v3;
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "g"+poly.name;
        return newpoly;
    }
    
    // Propellor
    // ------------------------------------------------------
    // builds a new 'skew face' by making new points along edges, 1/3rd the distance from v1->v2,
    // then connecting these into a new inset face.  This breaks rotational symmetry about the
    // faces, whirling them into gyres
    
    static Polyhedron propellor(Polyhedron poly) {
        
        Polyflag flag;
        
        for (size_t i = 0; i < poly.n_vertex; i++) // each old vertex is a new vertex
            flag.newV("v"+i2s(i), unit(poly.vertexes[i]));
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            
            auto &f = poly.faces[i];
            auto flen=f.size();
            auto v1=f[flen-2], v2=f[flen-1]; //  [v1, v2] = f.slice(-2);
            
            for (auto &v : f) {
                auto v3 = v;
                auto sv1=i2s(v1), sv2=i2s(v2), si=i2s(i), sv3=i2s(v3);
                
                flag.newV(sv1+"~"+sv2, oneThird(poly.vertexes[v1], poly.vertexes[v2]));  // new v in face, 1/3rd along edge
                auto fname = si+"f"+sv2;
                flag.newFlag("v"+si, sv1+"~"+sv2,  sv2+"~"+sv3); // five new flags
                flag.newFlag(fname,   sv1+"~"+sv2, sv2+"~"+sv1);
                flag.newFlag(fname,   sv2+"~"+sv1,     "v"+sv2);
                flag.newFlag(fname,      "v"+sv2,  sv2+"~"+sv3);
                flag.newFlag(fname,   sv2+"~"+sv3,  sv1+"~"+sv2);
                // shift over one
                v1=v2; v2=v3;
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "p"+poly.name;
        return newpoly;
    }
    
    // Reflection
    // ------------------------------------------------------
    // geometric reflection through origin
    static Polyhedron reflect(Polyhedron poly) {
        
        // reflect each point through origin
        for (size_t i = 0; i < poly.n_vertex; i++)
            poly.vertexes[i] = -poly.vertexes[i];
        
        // repair clockwise-ness of faces
        for (size_t i = 0; i < poly.n_faces; i++)
            reverse(poly.faces[i].begin(), poly.faces[i].end());
        
        poly.name = "r"+poly.name;
        return poly;
    }
    
    // Dual
    // ---------------------------------------------------------
    // The dual of a polyhedron is another mesh wherein:
    // - every face in the original becomes a vertex in the dual
    // - every vertex in the original becomes a face in the dual
    //
    // So N_faces, N_vertices = N_dualfaces, N_dualvertices
    //
    // The new vertex coordinates are convenient to set to the original face centroids.
    //
    static Polyhedron dual(Polyhedron poly) {
        Polyflag flag;
        map<int,map<string,string>> face;
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto v1 = f.back(); //previous vertex
            for (auto &v2 : f) {
                // THIS ASSUMES that no 2 faces that share an edge share it in the same orientation!
                // which of course never happens for proper manifold meshes, so get your meshes right.
                face[v1]["v"+i2s(v2)] = i2s(i);
                v1=v2;
            }
        } // current becomes previous
        
        auto centers = poly.get_centers();
        for (size_t i = 0; i < poly.n_faces; i++)
            flag.newV(i2s(i),centers[i]);
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto v1 = f.back(); //previous vertex
            for (auto v2 : f) {
                flag.newFlag(i2s(v1), face[v2]["v"+i2s(v1)], i2s(i));
                v1=v2;
            }
        } // current becomes previous
        
        auto dpoly = flag.topoly(); // build topological dual from flags
        
        // match F index ordering to V index ordering on dual
        Faces sortF(dpoly.n_faces);
        for (auto &f : dpoly.faces) {
            auto k = intersect(poly.faces[f[0]], poly.faces[f[1]], poly.faces[f[2]]);
            sortF[k] = f;
        }
        dpoly.faces = sortF;
        
        if (poly.name[0] != 'd')     dpoly.name = "d"+poly.name;
        else                         dpoly.name = poly.name.substr(1, string::npos);
        
        return dpoly;
    }
    
    // Chamfer
    // ----------------------------------------------------
    // A truncation along a polyhedron's edges.
    // Chamfering or edge-truncation is similar to expansion, moving faces apart and outward,
    // but also maintains the original vertices. Adds a new hexagonal face in place of each
    // original edge.
    // A polyhedron with e edges will have a chamfered form containing 2e new vertices,
    // 3e new edges, and e new hexagonal faces. -- Wikipedia
    // See also http://dmccooey.com/polyhedra/Chamfer.html
    //
    // The dist parameter could control how deeply to chamfer.
    // But I'm not sure about implementing that yet.
    //
    // Q: what is the dual operation of chamfering? I.e.
    // if cX = dxdX, and xX = dcdX, what operation is x?
    
    // We could "almost" do this in terms of already-implemented operations:
    // cC = t4daC = t4jC, cO = t3daO, cD = t5daD, cI = t3daI
    // But it doesn't work for cases like T.
    
    static Polyhedron chamfer(Polyhedron poly, float dist=0.5) {
        Polyflag flag;
        auto normals = poly.get_normals();
        
        // For each face f in the original poly
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto v1 = f.back();
            auto v1new = i2s(i) + "_" + i2s(v1);
            
            for (auto &v2 : f) {
                // TODO: figure out what distances will give us a planar hex face.
                // Move each old vertex further from the origin.
                flag.newV(i2s(v2), (1.0 + dist) * poly.vertexes[v2]);
                // Add a new vertex, moved parallel to normal.
                auto v2new = i2s(i) + "_" + i2s(v2);
                
                auto sv1=i2s(v1), sv2=i2s(v2), si=i2s(i);
                
                flag.newV(v2new, poly.vertexes[v2] + (dist*1.5 * normals[i]));
                // Four new flags:
                // One whose face corresponds to the original face:
                flag.newFlag("orig"+si, v1new, v2new);
                // And three for the edges of the new hexagon:
                auto facename = (v1<v2 ? "hex"+sv1+"_"+sv2 : "hex"+sv2+"_"+sv1);
                flag.newFlag(facename, sv2, v2new);
                flag.newFlag(facename, v2new, v1new);
                flag.newFlag(facename, v1new, sv1);
                
                v1 = v2;
                v1new = v2new;
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "c"+poly.name;
        return newpoly;
    }
    
    // Whirl
    // -------------------------------------------------------
    // Gyro followed by truncation of vertices centered on original faces.
    // This create 2 new hexagons for every original edge.
    // (https://en.wikipedia.org/wiki/Conway_polyhedron_notation#Operations_on_polyhedra)
    //
    // Possible extension: take a parameter n that means only whirl n-sided faces.
    // If we do that, the flags marked #* below will need to have their other sides
    // filled in one way or another, depending on whether the adjacent face is
    // whirled or not.
    
    static Polyhedron whirl(Polyhedron poly, int n=0) {
        
        Polyflag flag;
        
        for (size_t i = 0; i < poly.n_vertex; i++) // each old vertex is a new vertex
            flag.newV("v"+i2s(i), unit(poly.vertexes[i]));
        
        // new vertices around center of each face
        auto centers = poly.get_centers();
        //for f,i in poly.face
        //  # Whirl: use "center"+i+"~"+v1
        //  flag.newV "center"+i+"~"+v1, unit(centers[i])
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto flen=f.size();
            auto v1=f[flen-2], v2=f[flen-1]; //  [v1, v2] = f.slice(-2);
            
            for (size_t j = 0; j < flen; j++) {
                auto v = f[j];
                auto v3 = v;
                auto sv1=i2s(v1), sv2=i2s(v2), sv3=i2s(v3), si=i2s(i);
                
                // New vertex along edge
                auto v1_2 = oneThird(poly.vertexes[v1], poly.vertexes[v2]);
                flag.newV(sv1+"~"+sv2, v1_2);
                // New vertices near center of face
                auto cv1name = "center"+si+"~"+sv1;
                auto cv2name = "center"+si+"~"+sv2;
                flag.newV(cv1name, unit(oneThird(centers[i], v1_2)));
                
                auto fname = si+"f"+sv1;
                // New hexagon for each original edge
                flag.newFlag(fname, cv1name,   sv1+"~"+sv2);
                flag.newFlag(fname, sv1+"~"+sv2, sv2+"~"+sv1); //*
                flag.newFlag(fname, sv2+"~"+sv1, "v"+sv2);  //*
                flag.newFlag(fname, "v"+sv2,  sv2+"~"+sv3); //*
                flag.newFlag(fname, sv2+"~"+sv3, cv2name);
                flag.newFlag(fname, cv2name,   cv1name);
                
                // New face in center of each old face
                flag.newFlag("c"+si, cv1name, cv2name);
                v1=v2; v2=v3;
            }
        } // shift over one
        
        auto newpoly = flag.topoly();
        newpoly.name = "w"+poly.name;
        return newpoly;
    }
    
    // Quinto
    // -------------------------------------------------------
    // This creates a pentagon for every point in the original face, as well as one new inset face.
    static Polyhedron quinto(Polyhedron poly) {
        Polyflag flag;
        auto centers=poly.get_centers();
        
        // For each face f in the original poly
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto flen=f.size();
            auto centroid=centers[i];
            
            // walk over face vertex-triplets
            auto v1=f[flen-2], v2=f[flen-1]; //  [v1, v2] = f.slice(-2);
            
            for (auto v3 : f) {
                
                auto sv1=i2s(v1), sv2=i2s(v2), si=i2s(i);
                
                // for each face-corner, we make two new points:
                auto midpt = midpoint(poly.vertexes[v1], poly.vertexes[v2]);
                auto innerpt = midpoint(midpt, centroid);
                auto  fname = "f"+si+"_"+sv2,
                mn12=midName(v1, v2), mn23=midName(v2, v3),
                svn1="i"+si+"_"+mn12,
                svn2="i"+si+"_"+mn23;
                
                flag.newV(mn12, midpt);
                flag.newV(svn1, innerpt);
                
                // and add the old corner-vertex
                flag.newV(sv2, poly.vertexes[v2]);
                
                // pentagon for each vertex in original face
                flag.newFlag(fname, svn1, mn12);
                flag.newFlag(fname, mn12, sv2);
                flag.newFlag(fname, sv2,  mn23);
                flag.newFlag(fname, mn23, svn2);
                flag.newFlag(fname, svn2, svn1);
                
                // inner rotated face of same vertex-number as original
                flag.newFlag("f_in_"+si, svn1, svn2);
                
                // shift over one
                v1=v2; v2=v3;
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "q"+poly.name;
        return newpoly;
    }
    
    // inset / extrude / "Loft" operator
    // ------------------------------------------------------
    static Polyhedron insetN(Polyhedron poly, int n=0, float inset_dist=0.5, float popout_dist=-0.2) {
        
        Polyflag flag;
        
        for (size_t i = 0; i < poly.n_vertex; i++) // each old vertex is a new vertex
            flag.newV("v"+i2s(i), poly.vertexes[i]);
        
        auto normals = poly.get_normals();
        auto centers = poly.get_centers();
        
        for (size_t i = 0; i < poly.n_faces; i++) { //new inset vertex for every vert in face
            auto &f = poly.faces[i];
            if (f.size() == (size_t)n || n == 0) {
                for (auto &v : f) {
                    flag.newV("f"+i2s(i)+"v"+i2s(v), tween(poly.vertexes[v],centers[i],inset_dist) +
                              (popout_dist * normals[i]));
                }
            }
        }
        
        bool foundAny = false;    // alert if don't find any
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto f = poly.faces[i];
            auto v1 = "v"+i2s(f.back());
            for (auto &v : f) {
                auto v2 = "v"+i2s(v);
                auto si=i2s(i);
                
                if (f.size() == (size_t)n || n == 0) {
                    foundAny = true;
                    auto fname = si + v1;
                    flag.newFlag(fname,      v1,       v2);
                    flag.newFlag(fname,      v2,       "f"+si+v2);
                    flag.newFlag(fname, "f"+si+v2,  "f"+si+v1);
                    flag.newFlag(fname, "f"+si+v1,  v1);
                    //new inset, extruded face
                    flag.newFlag("ex"+si, "f"+si+v1,  "f"+si+v2);
                } else {
                    flag.newFlag(si, v1, v2);  // same old flag, if non-n
                }
                v1=v2;
            }
        }  // current becomes previous
        
        if (!foundAny)
            printf("No %d - fold components were found.", n);
        
        auto newpoly = flag.topoly();
        newpoly.name = "n" + (n ? to_string(n):"") + poly.name;
        return newpoly;
    }
    
    // extrudeN
    // ------------------------------------------------------
    // for compatibility with older operator spec
    static Polyhedron extrudeN(Polyhedron poly, int n=0){
        auto newpoly = insetN(poly, n, 0.0, 0.3);
        newpoly.name = "x" + (n ? to_string(n):"") + poly.name;
        return newpoly;
    }
    
    // loft
    // ------------------------------------------------------
    static Polyhedron loft(Polyhedron poly, int n=0, float alpha=0) {
        auto newpoly = insetN(poly, n, alpha, 0.0);
        newpoly.name = "l" + (n ? to_string(n):"") + poly.name;
        return newpoly;
    }
    
    // Hollow (skeletonize)
    // ------------------------------------------------------
    static Polyhedron hollow(Polyhedron poly, float inset_dist=0.5, float thickness=0.2) {
        auto dualnormals = PolyOperations::dual(poly).avg_normals();
        auto normals = poly.avg_normals();
        auto centers = poly.get_centers();
        
        Polyflag flag;
        for (size_t i = 0; i < poly.n_vertex; i++) { // each old vertex is a new vertex
            auto p = poly.vertexes[i];
            auto si=i2s(i);
            
            flag.newV("v"+si, p);
            flag.newV("downv"+si,  p - thickness * dualnormals[i]);
        }
        // new inset vertex for every vert in face
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto si=i2s(i);
            auto &f = poly.faces[i];
            for (auto &v : f) {
                auto sv=i2s(v);
                
                flag.newV("fin"+si+"v"+sv, tween(poly.vertexes[v], centers[i], inset_dist));
                flag.newV("findown"+si+"v"+sv, tween(poly.vertexes[v], centers[i], inset_dist) - (thickness * normals[i]));
            }
        }
        
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            string v1 = "v"+i2s(f.back());
            auto si=i2s(i);
            
            for (auto &v : f) {
                auto sv=i2s(v), v2 = "v"+sv;
                
                auto fname = si + v1, s1=si+v1, s2=si+v2;
                flag.newFlag(fname,      v1,       v2);
                flag.newFlag(fname,      v2,       "fin"+s2);
                flag.newFlag(fname, "fin"+s2,  "fin"+s1);
                flag.newFlag(fname, "fin"+s1,  v1);
                
                fname = "sides"+s1;
                flag.newFlag(fname, "fin"+s1,     "fin"+s2);
                flag.newFlag(fname, "fin"+s2,     "findown"+s2);
                flag.newFlag(fname, "findown"+s2, "findown"+s1);
                flag.newFlag(fname, "findown"+s1, "fin"+s1);
                
                fname = "bottom"+s1;
                flag.newFlag(fname,  "down"+v2,      "down"+v1);
                flag.newFlag(fname,  "down"+v1,      "findown"+s1);
                flag.newFlag(fname,  "findown"+s1, "findown"+s2);
                flag.newFlag(fname,  "findown"+s2, "down"+v2);
                
                v1 = v2; // current becomes previous
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "H"+poly.name;
        return newpoly;
    }
    
    // Perspectiva 1
    // ------------------------------------------------------------------------------------------
    // an operation reverse-engineered from Perspectiva Corporum Regularium
    static Polyhedron perspectiva1(Polyhedron poly){
        auto centers = poly.get_centers();  // calculate face centers
        
        Polyflag flag;
        for (size_t i = 0; i < poly.n_vertex; i++)  // each old vertex is a new vertex
            flag.newV("v"+i2s(i), poly.vertexes[i]);
        
        // iterate over triplets of faces v1,v2,v3
        for (size_t i = 0; i < poly.n_faces; i++) {
            auto &f = poly.faces[i];
            auto flen=f.size();
            auto v1 = "v"+i2s(f[flen-2]), v2 = "v"+i2s(f[flen-1]);
            auto vert1 = poly.vertexes[f[flen-2]], vert2 = poly.vertexes[f[flen-1]];
            auto si=i2s(i);
            
            for (auto &v : f) {
                auto v3 = "v"+i2s(v);
                auto vert3 = poly.vertexes[v];
                auto v12=v1+"~"+v2; // names for "oriented" midpoints
                auto v21=v2+"~"+v1;
                auto v23=v2+"~"+v3;
                
                // on each Nface, N new points inset from edge midpoints towards center = "stellated" points
                flag.newV(v12, midpoint( midpoint(vert1, vert2), centers[i] ));
                
                // inset Nface made of new, stellated points
                flag.newFlag("in"+si,      v12,       v23);
                
                // new tri face constituting the remainder of the stellated Nface
                auto fname="f"+si+v2;
                flag.newFlag(fname,      v23,      v12);
                flag.newFlag(fname,      v12,      v2);
                flag.newFlag(fname,      v2,       v23);
                
                // one of the two new triangles replacing old edge between v1->v2
                fname = "f"+v12;
                flag.newFlag(fname,     v1,        v21);
                flag.newFlag(fname,     v21,       v12);
                flag.newFlag(fname,     v12,       v1);
                
                v1=v2; v2=v3; //  [v1, v2] = [v2, v3];  // current becomes previous
                vert1=vert2; vert2=vert3; // [vert1, vert2] = [vert2, vert3];
            }
        }
        
        auto newpoly = flag.topoly();
        newpoly.name = "P"+poly.name;
        return newpoly;
    }
    //===================================================================================================
    // Goldberg-Coxeter Operators  (in progress...)
    //===================================================================================================
    
    // Triangular Subdivision Operator
    // ----------------------------------------------------------------------------------------------
    // limited version of the Goldberg-Coxeter u_n operator for triangular meshes
    // We subdivide manually here, instead of using the usual flag machinery.
    static Polyhedron trisub(Polyhedron poly, int n=2) {
        
        for (size_t fn = 0; fn < poly.n_faces; fn++)  // No-Op for non-triangular meshes.
            if(poly.faces[fn].size() != 3)
                return poly;
        
        // Calculate redundant set of new vertices for subdivided mesh.
        Vertexes newVs;
        map<string,int>vmap;
        int pos = 0;
        
        for (size_t fn = 0; fn < poly.faces.size(); fn++) {
            auto &f = poly.faces[fn];
            auto flen = f.size();
            auto i1=f[flen-3],i2=f[flen-2],i3=f[flen-1]; // let [i1, i2, i3] = f.slice(-3);
            auto v1 = poly.vertexes[i1], v2 = poly.vertexes[i2], v3 = poly.vertexes[i3];
            auto v21 = v2 - v1;
            auto v31 = v3 - v1;
            for (int i = 0; i <= n; i++) {
                for (int j = 0; j+i <= n; j++) {
                    auto v = (v1 + (i * 1.0 / n) * v21) + (j * 1.0 / n * v31);
                    vmap["v"+i2s(fn)+"-"+i2s(i)+"-"+i2s(j)] = pos++;
                    newVs.push_back(v);
                }
            }
        }
        
        // The above vertices are redundant along original edges,
        // we need to build an index map into a uniqueified list of them.
        // We identify vertices that are closer than a certain epsilon distance.
        float EPSILON_CLOSE = 1.0e-8;
        Vertexes uniqVs;
        int newpos = 0;
        map<int,int> uniqmap;
        int i=0;
        for (auto v : newVs) {
            if (uniqmap.find(i)!=uniqmap.end())  continue;  // already mapped
            uniqmap[i] = newpos;
            uniqVs.push_back(v);
            for(size_t j = i+1; j < newVs.size(); j++) {
                auto w = newVs[j];
                if (simd_distance(v, w) < EPSILON_CLOSE)
                    uniqmap[(int)j] = newpos;
            }
            newpos++;
        }
        
        Faces faces;
        for (size_t fn = 0; fn < poly.n_faces; fn++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j+i < n; j++) {
                    faces.push_back(Face{uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i)+"-"+i2s(j)]],
                        uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i+1)+"-"+i2s(j)]],
                        uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i)+"-"+i2s(j+1)]]});
                }
            }
            for (auto i = 1; i < n; i++) {
                for (auto j = 0; j+i < n; j++) {
                    faces.push_back(Face{uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i)+"-"+i2s(j)]],
                        uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i)+"-"+i2s(j+1)]],
                        uniqmap[vmap["v"+i2s(fn)+"-"+i2s(i-1)+"-"+i2s(j+1)]]});
                }
            }
        }
        
        // Create new polygon out of faces and unique vertices.
        return Polyhedron("u"+i2s(n)+poly.name, uniqVs, faces);
    }
private:
    static inline string i2s(size_t i) { return to_string(i); }
    static inline string midName(int v1, int v2) { return v1<v2 ? to_string(v1)+"_"+to_string(v2) : to_string(v2)+"_"+to_string(v1); }
    static inline Vertex midpoint(Vertex vec1, Vertex vec2) { return (vec1+vec2)/2.; };
    static inline Vertex unit(Vertex v) { return simd::normalize(v); }
    static inline Vertex oneThird(Vertex &vec1, Vertex &vec2) { return tween(vec1, vec2, 1/3.); }
    static inline Vertex tween(Vertex &vec1, Vertex &vec2, float t) { return (1.-t)*vec1 + t*vec2; }
    static inline int intersect(Face &set1, Face &set2, Face &set3) {
        for (auto s1 : set1)
            for (auto s2 : set2)
                if (s1 == s2)
                    for (auto s3 : set3)
                        if (s1 == s3)  return s1;
        return 0; // empty intersection
    }
    static Vertex calcCentroid(Vertexes vertices) {
        // running sum of vertex coords
        Vertex centroidV=0;
        for (auto &v : vertices) centroidV += v;
        return centroidV / vertices.size();
    }
};

#endif /* poly_operations_hpp */
