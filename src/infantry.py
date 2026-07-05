from vector2 import Vector2
import random

class Infantry:

    def __init__(self, position: Vector2, color):
        self.position = position
        self.destination = Vector2(position.x, position.y) 
        self.speed = 20 # speed in m/s
        self.health = 10 
        self.max_health = 10
        self.condition = "normal"
        self.intent = "move"
        self.color = color
        self.radius = 5
        self.target = None
        self.range = 100
        self.reload_duration = 0

    # Change name to set_destination when introducing the move_toward function
    def move_to(self, destination: Vector2):
        self.destination = destination

    def take_damage(self, damage):
        self.health -= damage

    def update_condition(self):
        if self.health <= 0:
            self.health = 0
        if self.health <= 0.3 * self.max_health:
            self.condition = "heavily_wounded"
        elif self.health <= 0.7 * self.max_health:
            self.condition = "wounded"
        return self.condition
    
    def reload(self):
        self.reload_duration = 200
    
    def move_towards_destination(self,dt):
            coordinate_diff = self.destination.subtract(self.position)
            normalized = coordinate_diff.normalize()
            unit_velocity = normalized.scalar_multiplication(self.speed)
            next_movement = unit_velocity.scalar_multiplication(dt)

            if next_movement.length()  > coordinate_diff.length():
                self.position = self.destination
            else:
                self.position = self.position.add(next_movement)
            

    def update(self):
        if self.target and self.reload_duration == 0:
            self.intent = "shoot"
        else:
            self.intent = "move"
        
        if self.reload_duration > 0:
            self.reload_duration -= 1
            
