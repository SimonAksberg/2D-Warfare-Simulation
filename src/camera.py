from vector2 import Vector2

class Camera:

    def __init__(self, position = Vector2(0.0,0.0)):
        self.position = position
        self.zoom = 1
        self.pixels_per_meter = 1

    def world_to_screen(self, unit_position: Vector2):
        return unit_position
