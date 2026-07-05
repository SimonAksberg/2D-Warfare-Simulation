from vector2 import Vector2
import random

class Infantry:

    def __init__(self, position: Vector2, color):
        self.position = position
        self.destination = Vector2(position.x, position.y) 
        self.speed = 50 # speed in m/s
        self.health = 100 
        self.condition = "normal"
        self.color = color

    # Change name to set_destination when introducing the move_toward function
    def move_to(self, destination: Vector2):
        self.destination = destination

    def take_damage(self):
        self.health -= 1

    def update_condition(self):
        if self.health <= 30:
            self.condition = "heavily_wounded"
        elif self.health <= 70:
            self.condition = "wounded"
        return self.condition

    def update(self, dt):
        randint = random.randint(1,100)

        if randint <= 10:
            self.take_damage()
        else:
            coordinate_diff = self.destination.subtract(self.position)
            normalized = coordinate_diff.normalize()
            unit_velocity = normalized.scalar_multiplication(self.speed)
            next_movement = unit_velocity.scalar_multiplication(dt)

            if next_movement.get_length()  > coordinate_diff.get_length():
                self.position = self.destination
            else:
                self.position = self.position.add(next_movement)
            
        