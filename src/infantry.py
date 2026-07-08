from vector2 import Vector2
import constants

class Infantry:

    def __init__(self, position: Vector2, faction, color ):
        self.health = constants.INFANTRY_MAX_HEALTH
        self.max_health = constants.INFANTRY_MAX_HEALTH
        self.speed = constants.INFANTRY_SPEED
        self.range = constants.INFANTRY_RANGE
        self.reload_duration = constants.INFANTRY_RELOAD_DURATION
        self.radius = constants.INFANTRY_RADIUS
        self.position = position
        self.destination = position
        self.remaining_reload_duration = 0
        self.target = None
        self.condition = "normal"
        self.intent = "move"
        self.faction = faction
        self.color = color


    def set_destination(self, destination: Vector2):
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
        self.remaining_reload_duration = self.reload_duration
    
    def move_towards_destination(self,dt):
            coordinate_diff = self.destination.subtract(self.position)
            normalized = coordinate_diff.normalize()
            unit_velocity = normalized.scalar_multiplication(self.speed)
            next_movement = unit_velocity.scalar_multiplication(dt)

            if next_movement.length()  > coordinate_diff.length():
                self.position = self.destination
            else:
                self.position = self.position.add(next_movement)
            

    def update_intent(self):
        if self.remaining_reload_duration == 0 and self.target is not None:
            self.intent = "shoot"
        else:
            self.intent = "move"
        
        if self.remaining_reload_duration > 0:
            self.remaining_reload_duration -= 1
            
