

class Color:
    
    def __init__(self, red=255, green=255, blue=255, alpha=255):
        self.r = int(red)
        self.g = int(green)
        self.b = int(blue)
        self.a = int(alpha)
    
    def __repr__(self):
        return f'Color({self.r}, {self.g}, {self.b}, {self.a})'
    
    __str__ = __repr__
    
    def __iter__(self):
        return iter((self.r, self.g, self.b, self.a))
    
    @classmethod
    def from_fraction(cls, red=1, green=1, blue=1, alpha=1):
        return cls(red*255, green*255, blue*255, alpha*255)

    @classmethod
    def from_hex(cls, hex_color: str) -> tuple:
        hex_color = hex_color.strip('#')
        return cls(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), 255)
    
    @classmethod
    def from_hsv(cls, hue=0, saturation=0, value=1, alpha=255):
        C = saturation * value
        X = C * (1 - abs((hue / 60) % 2 - 1))
        m = value - C
        
        sector = (hue % 360) // 60
        match sector:
            case 0: RGB_prime = (C, X, 0)
            case 1: RGB_prime = (X, C, 0)
            case 2: RGB_prime = (0, C, X)
            case 3: RGB_prime = (0, X, C)
            case 4: RGB_prime = (X, 0, C)
            case 5: RGB_prime = (C, 0, X)
        
        red, green, blue = ((x+m)*255 for x in RGB_prime)
        
        return cls(red, green, blue, alpha)

COLORS = {
    'red': Color.from_hex('#ff0000'),
    'green': Color.from_hex('#00ff00'),
    'blue': Color.from_hex('#0000ff'),
}