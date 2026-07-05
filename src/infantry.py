from vector2 import Vector2

class Infantry:

    def __init__(self, position: Vector2):
        self.position = position
        self.destination = Vector2(position.x, position.y) 
        self.speed = 50 # speed in m/s 

    def move_to(self, destination: Vector2):
        self.destination = destination

    def update(self, dt):
        coordinate_diff = self.destination.subtract(self.position)
        normalized = coordinate_diff.normalize()
        unit_velocity = normalized.scalar_multiplication(self.speed)
        next_movement = unit_velocity.scalar_multiplication(dt)

        if next_movement.get_length()  > coordinate_diff.get_length():
            self.position = self.destination
        else:
            self.position = self.position.add(next_movement)