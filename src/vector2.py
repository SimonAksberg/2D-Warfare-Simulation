import math

class Vector2:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def subtract (self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def normalize(self):
        length = self.get_length()

        if length == 0:
            return Vector2(0,0)
        
        return Vector2(self.x / length, self.y / length)


    def scalar_multiplication(self, k):
        return Vector2(self.x * k, self.y * k)

    def get_length(self):
        return float((math.sqrt(math.pow(self.x,2) + math.pow(self.y,2))))

