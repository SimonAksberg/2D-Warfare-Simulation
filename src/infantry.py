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
        self.wounded_status = "normal"
        self.state = "ADVANCE"
        self.intent = "move"
        self.faction = faction
        self.color = color


    def set_destination(self, destination: Vector2):
        self.destination = destination

    def take_damage(self, damage):
        self.health -= damage
        self.update_wounded_status()

    def update_wounded_status(self):
        if self.health <= constants.INFANTRY_HEAVILY_WOUNDED_THRESHOLD:
            self.wounded_status = "heavily_wounded"

        elif self.health <= constants.INFANTRY_WOUNDED_THRESHOLD:
            self.wounded_status = "wounded"

        else:
            self.wounded_status = "normal"
        
        self.update_appearance()

    def update_appearance(self):
            if self.faction == "ally":
                if self.wounded_status == "heavily_wounded":
                    self.color = constants.ALLY_HEAVILY_WOUNDED_INFANTRY_COLOR
                elif self.wounded_status == "wounded":
                    self.color = constants.ALLY_WOUNDED_INFANTRY_COLOR
                else:
                    self.color = constants.ALLY_INFANTRY_COLOR
            elif self.faction == "enemy":
                if self.wounded_status == "heavily_wounded":
                    self.color = constants.ENEMY_HEAVILY_WOUNDED_INFANTRY_COLOR
                elif self.wounded_status == "wounded":
                    self.color = constants.ENEMY_WOUNDED_INFANTRY_COLOR
                else:
                    self.color = constants.ENEMY_INFANTRY_COLOR
        
    
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
    
    def reduce_reload_duration(self):
        self.remaining_reload_duration -= 1