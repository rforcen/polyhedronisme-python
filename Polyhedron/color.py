from random import random

# global object
color_hex_palette = None
    # ['#ff7777', '#dddddd', '#889999', '#fff0e5',
    #  '#aa3333', '#ff0000', '#ffffff', '#aaaaaa']


class color():
    @staticmethod
    def hsl2rgb(h, s, l):
        def hue2rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1 / 6: return p + (q - p) * 6 * t
            if t < 1 / 2: return q
            if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6
            return p

        if s == 0:
            r = g = b = l;  # achromatic
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue2rgb(p, q, h + 1 / 3)
            g = hue2rgb(p, q, h)
            b = hue2rgb(p, q, h - 1 / 3)
        return [r, g, b]

    @staticmethod
    def hextofloats(h):
        return [int(h[i:i + 2], 16) / 255. for i in (1, 3, 5)]  # skip '#'

    @staticmethod
    def floatstohex(rgb):
        return f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'

    @staticmethod
    def get_item(i: int):
        if color_hex_palette is None:
            color.set_random()
        return color_hex_palette[i % len(color_hex_palette)]

    @staticmethod
    def set_random():
        global color_hex_palette
        color_hex_palette = color.rndcolors()

    @staticmethod
    def rndcolors():
        return [color.floatstohex(color.hsl2rgb(random(), 0.5 * random() + 0.3, 0.5 * random() + 0.45)) for _ in
                range(100)]

    @staticmethod
    def print_pallete():
        color.set_random()
        for c in color_hex_palette:
            print(c, end=' ')
            fs = color.hextofloats(c)
            print(fs, end=' ')
            print(color.floatstohex(fs))


if __name__ == '__main__':
    color.print_pallete()
