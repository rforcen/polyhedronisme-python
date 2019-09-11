//===================================================================================================
// Polyhedron Flagset Construct
//
// A Flag is an associative triple of a face index and two adjacent vertex vertidxs,
// listed in geometric clockwise order (staring into the normal)
//
// Face_i -> V_i -> V_j
//
// They are a useful abstraction for defining topological transformations of the polyhedral mesh, as
// one can refer to vertices and faces that don't yet exist or haven't been traversed yet in the
// transformation code.
//
// A flag is similar in concept to a directed halfedge in halfedge data structures.
//
#ifndef polyflag_hpp
#define polyflag_hpp

#include "common.hpp"

const int MAX_FACE_SIDEDNESS = 1000; //GLOBAL

class Polyflag {
    
    map<string, map<string, string>>flags;  // flags[face][vertex] = next vertex of flag; symbolic triples
    map<string, int>vertidxs; // [symbolic names] holds vertex index
    map<string, Vertex>vertices; // XYZ coordinates
    
public:
    Polyflag() {}
    
    // Add a new vertex named "name" with coordinates "xyz".
    void newV(string vertName, Vertex coordinates) {
        vertidxs[vertName] = 0;
        vertices[vertName] = coordinates;
    }
    
    void newFlag(string faceName, string vertName1, string vertName2) {
        flags[faceName][vertName1] = vertName2;
    }
    
    Polyhedron topoly() {
        Vertexes vertexes(vertidxs.size());
        Faces faces(flags.size());

        int ctr = 0; // first number the vertices
        for (auto i : vertidxs) {
            vertexes[ctr]=vertices[i.first]; // store in array
            vertidxs[i.first] = ctr++;
        }
        
        ctr = 0;
        for (auto flag : flags) {
            
            auto &face = flags[flag.first];
            string &v0 = (*face.begin()).second; // first item
            auto &is = flag.second;

            // build face out of all the edge relations in the flag assoc array
            auto v = v0; // v moves around face
            faces[ctr].push_back(vertidxs[v]); //record index
            v = is[v]; //  goto next vertex

            for (int faceCTR=0; v!=v0; faceCTR++) { // loop until back to start
                faces[ctr].push_back(vertidxs[v]);
                v = is[v];
                // necessary during development to prevent browser hangs on badly formed flagsets
                if (faceCTR > MAX_FACE_SIDEDNESS) {
                    printf("Bad flag spec, have a neverending face:%d", ctr);
                    break;
                }
            }
            ctr++;
        }
        return Polyhedron("unknown polyhedron", vertexes, faces);
    }
};


#endif // polyflag_hpp
