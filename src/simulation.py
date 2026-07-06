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

        for _ in range(constants.NUMBER_OF_UNITS):
            self.units.append(self.create_unit())
        
        for i in range(constants.NUMBER_OF_UNITS):
            self.destinations.append(self.create_destination())

    def run(self):
        for unit,destination in zip(self.units, self.destinations):
            unit.move_to(destination)

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
    
    def create_unit(self):
        infantry_unit = Infantry(
            Vector2(0, random.randint(0,constants.SCREEN_HEIGHT)),
            constants.INFANTRY_COLOR
            )
        return infantry_unit
    
    def create_destination(self):
        destination = Vector2(
            random.randint(50,constants.SCREEN_WIDTH - 50), 
            random.randint(50,constants.SCREEN_HEIGHT - 50)
            )
        return destination
    
    def create_projectile(self, unit_position, target_position, owner):
        projectile = Projectile(unit_position, target_position, owner, constants.PROJECTILE_COLOR)
        return projectile
    
    def update(self, dt):
        self.update_target_selection()
        self.update_units(dt)
        self.update_projectiles(dt)
        self.resolve_projectile_hits()
    
    def update_units(self, dt):
        for unit in self.units:
            unit.update_condition()

            if unit.condition == "heavily_wounded":
                unit.color = constants.HEAVILY_WOUNDED_INFANTRY_COLOR
            elif unit.condition == "wounded":
                unit.color = constants.WOUNDED_INFANTRY_COLOR
            else:
               unit.color = constants.INFANTRY_COLOR

            unit.update()

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
            

    def find_target(self,unit):
        closest_enemy = None
        closest_distance = float("inf")

        for enemy in self.units:
            if enemy is unit:
                continue
            else:
                distance = enemy.position.subtract(unit.position).length()
                if distance < unit.range:

                    if distance < closest_distance:
                        closest_enemy = enemy
                        closest_distance = distance

        return closest_enemy

    def update_target_selection(self):
        for unit in self.units:
            unit.target = self.find_target(unit)
        
    def update_projectiles(self,dt):
        for projectile in self.projectiles:
            projectile.update(dt)

    def resolve_projectile_hits(self):
        projectiles_to_remove = []
        units_to_remove = []

        for projectile in self.projectiles:
            for unit in self.units:
                if unit == projectile.owner:
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