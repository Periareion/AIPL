

class Color:

    @classmethod
    def hex(cls, hex_color):
        hex_color = hex_color.strip('#')
        return (int(hex_color[0:2], 16)/255, int(hex_color[2:4], 16)/255, int(hex_color[4:6], 16)/255)
    
    @classmethod
    def rgb(cls, rgb_color):
        return (rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)