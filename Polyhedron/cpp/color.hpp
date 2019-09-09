//
//  color.hpp
//  test_polygon
//
//  Created by asd on 03/09/2019.
//  Copyright © 2019 voicesync. All rights reserved.
//

#ifndef color_hpp
#define color_hpp

#include "common.hpp"

class Color {
public:
    static Vertex hsl2rgb(float h, float s, float l) {
        float r,g,b;
        if (s==0) r=g=b=l; // acromatic
        else {
            float q = (l < 0.5) ? l * (1. + s) : l + s - l * s;
            float p = 2. * l - q;
            r = hue2rgb(p, q, h + 1. / 3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1. / 3);
        }
        return Vertex{r, g, b};
    }
    static Vertexes random_pallete(int n=100) {
        Vertexes cols(n);
        for (auto i=0; i<n; i++) cols[i]=rnd();
        return cols;
    }
    static string  rgb2hex(float r, float g, float b) {
        char buff[8];
        sprintf(buff, "#%02x%02x%02x", (int)(r*255), (int)(g*255), (int)(b*255));
        return string(buff);
    }
    static string rgb2hex(Vertex c) {
        char buff[8];
        sprintf(buff, "#%02x%02x%02x", (int)(c.x*255), (int)(c.y*255), (int)(c.z*255));
        return string(buff);
    }
    
private:
    static float hue2rgb(float p, float q, float t) {
        if (t < 0.) t += 1;
        if (t > 1.) t -= 1;
        if (t < 1. / 6) return p + (q - p) * 6. * t;
        if (t < 1. / 2) return q;
        if (t < 2. / 3) return p + (q - p) * (2. / 3. - t) * 6.;
        return p;
    }
    static float random() { return (float)rand() / RAND_MAX;} // 0..1 random
    
    static Vertex rnd() {
        return hsl2rgb(random(), 0.5 * random() + 0.3, 0.5 * random() + 0.45);
    }
};

#endif /* color_hpp */
