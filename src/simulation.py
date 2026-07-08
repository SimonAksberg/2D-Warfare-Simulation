import pygame
import constants
from camera import Camera
from infantry import Infantry
from projectile import Projectile
import random
from vector2 import Vector2

class Simulation():
    def __init__(self):
        # Setup
        pygame.init()

        self.camera = Camera()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Warfare Simulation")

        self.clock = pygame.time.Clock()

        self.running = True
    
        self.units = []
        self.projectiles = []
        self.destinations =[]

        self.create_ally_units()
        self.create_enemy_units()
        self.create_unit_destinations()

    def run(self):
        # Positions are currently created once, hence assigned before game loop
        for unit,destination in zip(self.units, self.destinations):
            unit.set_destination(destination)

        # Simulation loop
        while self.running:
            # Delta time
            dt = self.clock.tick(60) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill screen with background color to wipe away anything from previous frame
            self.screen.fill(constants.BACKGROUND_COLOR)

            # This is where the actual simulation should take place
            self.update(dt)
            self.render()

            # Updates window based on what has happened in game loop
            pygame.display.flip()


        pygame.quit()

    def create_ally_units(self):
        for _ in range(constants.ALLY_NUMBER_OF_UNITS):
            self.units.append(self.create_unit("ally"))
    
    def create_enemy_units(self):
        for _ in range(constants.ENEMY_NUMBER_OF_UNITS):
             self.units.append(self.create_unit("enemy"))          
    
    def create_unit(self,faction):
        if faction == "ally":
            unit_color = constants.ALLY_INFANTRY_COLOR
            unit_spawn_point = Vector2(
                0,
                random.randint(0,constants.SCREEN_HEIGHT)
                )
        elif faction == "enemy":
            unit_color = constants.ENEMY_INFANTRY_COLOR
            unit_spawn_point = Vector2(
                constants.SCREEN_WIDTH,
                random.randint(0,constants.SCREEN_HEIGHT)
                )
            
        infantry_unit = Infantry(
            unit_spawn_point,
            faction,
            unit_color
            )
        return infantry_unit

    def create_unit_destinations(self):
        for i in range(constants.ALLY_NUMBER_OF_UNITS + constants.ENEMY_NUMBER_OF_UNITS):
            self.destinations.append(self.create_destination())

    def create_destination(self):
        destination = Vector2(
            random.randint(50,constants.SCREEN_WIDTH - 50), 
            random.randint(50,constants.SCREEN_HEIGHT - 50)
            )
        return destination
    
    def update(self, dt):
        self.update_target_selection()
        self.update_unit(dt)
        self.execute_unit_intent(dt)
        self.update_projectiles(dt)
        self.resolve_projectile_hits()
        self.update_unit_visuals()

    def update_target_selection(self):
        for unit in self.units:
            unit.target = self.find_target(unit)

    def find_target(self,current_unit):
        closest_enemy = None
        closest_distance = float("inf")

        for other_unit in self.units:
            if other_unit.faction == current_unit.faction:
                continue
            else:
                distance = other_unit.position.subtract(current_unit.position).length()
                if distance < current_unit.range:

                    if distance < closest_distance:
                        closest_enemy = other_unit
                        closest_distance = distance

        return closest_enemy
    
    def update_unit(self, dt):
        for unit in self.units:
            unit.update_condition()
            unit.update_intent()

    def execute_unit_intent(self,dt):
        for unit in self.units:
            if unit.intent == "shoot" and unit.target is not None:
                projectile = self.create_projectile(
                    unit.position, 
                    unit.target.position,
                    unit
                    )
                self.projectiles.append(projectile)
                unit.reload()

            elif unit.intent == "move":
                unit.move_towards_destination(dt)

    def create_projectile(self, unit_position, target_position, owner):
        projectile = Projectile(unit_position, target_position, owner, constants.PROJECTILE_COLOR)
        return projectile
        
    def update_projectiles(self,dt):
        for projectile in self.projectiles:
            projectile.update(dt)

    def resolve_projectile_hits(self):
        projectiles_to_remove = []
        units_to_remove = []

        for projectile in self.projectiles:
            for unit in self.units:
                # second condition decides if friendly fire is on or not
                if unit == projectile.owner or unit.faction == projectile.owner.faction:
                    continue
                if unit in units_to_remove:
                    continue

                difference = unit.position.subtract(projectile.position)
                distance = difference.length()

                if distance <=  unit.radius + projectile.radius:
                    unit.take_damage(projectile.damage)
                    projectiles_to_remove.append(projectile)
                    if unit.health <= 0:
                        units_to_remove.append(unit)
                    break

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile) 

        for unit in units_to_remove:
            self.units.remove(unit)

    def update_unit_visuals(self):
        for unit in self.units:
            if unit.faction == "ally":
                if unit.condition == "wounded":
                    unit.color = constants.ALLY_WOUNDED_INFANTRY_COLOR

                if unit.condition == "heavily_wounded":
                    unit.color = constants.ALLY_HEAVILY_WOUNDED_INFANTRY_COLOR

            elif unit.faction == "enemy":
                if unit.condition == "wounded":
                    unit.color = constants.ENEMY_WOUNDED_INFANTRY_COLOR

                if unit.condition == "heavily_wounded":
                    unit.color = constants.ENEMY_HEAVILY_WOUNDED_INFANTRY_COLOR

    def render(self):
        for unit in self.units:
            unit_screen_position = self.camera.world_to_screen(unit.position) 

            pygame.draw.circle(
                self.screen, 
                unit.color, 
                (round(unit_screen_position.x), round(unit_screen_position.y)),
                unit.radius
                )
            
        for projectile in self.projectiles:
            projectile_screen_position = self.camera.world_to_screen(projectile.position)

            pygame.draw.circle(
                self.screen,
                projectile.color,
                (round(projectile_screen_position.x), round(projectile_screen_position.y)),
                projectile.radius
                )