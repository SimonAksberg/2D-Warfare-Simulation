from vector2 import Vector2

class Projectile:

    def __init__(self, position: Vector2, destination: Vector2, owner, color):
        self.position = position
        self.destination = destination
        self.speed = 100 # m/s
        self.velocity = self.calculate_velocity()
        self.color = color
        self.owner = owner
        self.damage = 4
        self.radius = 1

    def move_to(self,destination):
        self.destination = destination
    
    def calculate_velocity(self):
        coordinate_diff = self.destination.subtract(self.position)
        normalized = coordinate_diff.normalize()
        projectile_velocity = normalized.scalar_multiplication(self.speed)
        return projectile_velocity

    def update(self,dt):
        next_movement = self.velocity.scalar_multiplication(dt)
        self.position = self.position.add(next_movement)