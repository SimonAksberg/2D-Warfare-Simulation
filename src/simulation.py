import pygame
import random
import constants
from infantry import Infantry
from projectile import Projectile
from vector2 import Vector2
from renderer import Renderer
from world import World

class Simulation():
    def __init__(self):
        # Setup
        self.clock = pygame.time.Clock()

        self.running = True
        self.paused = False
        self.world = World()
        self.renderer = Renderer()
        
        # self.units = []
        # self.allies = []
        # self.enemies = []
        # self.projectiles = []
        # self.destinations =[]
        # self.grid = SpatialGrid()

        self.create_ally_units()
        self.create_enemy_units()

        # Positions are currently created once, hence assigned before game loop
        self.assign_unit_destinations()

    def run(self):
        # Simulation loop
        while self.running:
            # Delta time
            dt = self.clock.tick(60) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

                    if event.key == pygame.K_g:
                        self.renderer.show_grid = not self.renderer.show_grid
        
            # Fill screen with background color to wipe away anything from previous frame

            # This is where the actual simulation should take place
            if not self.paused:
                self.update(dt)

            self.renderer.draw(self.world)

            # Updates window based on what has happened in game loop
            pygame.display.flip()

        pygame.quit()

    def create_ally_units(self):
        for _ in range(constants.ALLY_NUMBER_OF_UNITS):
            ally_unit = self.create_unit(constants.ALLY)
            self.world.units.append(ally_unit)
            self.world.allies.append(ally_unit)
    
    def create_enemy_units(self):
        for _ in range(constants.ENEMY_NUMBER_OF_UNITS):
            enemy_unit = self.create_unit(constants.ENEMY)
            self.world.units.append(enemy_unit)
            self.world.enemies.append(enemy_unit)        
    
    def create_unit(self,faction):
        unit_color = faction.color
        unit_spawn_point = faction.spawn_point
            
        infantry_unit = Infantry(
            unit_spawn_point,
            faction,
            unit_color
            )
        return infantry_unit

    def assign_unit_destinations(self):
        for unit in self.world.units:
            unit.destination = self.create_destination(unit.faction)

    def create_destination(self,faction):
        objective_destination = faction.objective
        destination_offset = self.create_destination_offset()
        final_destination = objective_destination.add(destination_offset)
        return final_destination
    
    def create_destination_offset(self):
        return Vector2(random.randint(-100,100),random.randint(-100,100))
    
    def update(self, dt):
        self.update_spatial_grid()
        self.update_unit_target_selection()
        self.update_unit_intent()
        self.execute_unit_intent(dt)
        self.update_projectiles(dt)
        self.resolve_projectile_hits()
    
    def update_spatial_grid(self):
        self.world.grid.clear()

        for unit in self.world.units:
            self.world.grid.insert(unit)

    def update_unit_target_selection(self):
        for unit in self.world.units:
            unit.target = self.find_target(unit)

    def find_target(self,unit):
        closest_enemy = None
        closest_distance = float("inf")

        for candidate in self.world.grid.query_radius(unit.position, unit.range):
            if candidate.faction == unit.faction:
                continue
            else:
                distance = candidate.position.subtract(unit.position).length()
                if distance < unit.range:

                    if distance < closest_distance:
                        closest_enemy = candidate
                        closest_distance = distance

        return closest_enemy
    
    def update_unit_intent(self):
        for unit in self.world.units:
            if unit.wounded_status == "heavily_wounded":
                unit.destination = unit.faction.retreat_point
                unit.intent = "move"

            elif unit.target is not None:
                if unit.remaining_reload_duration == 0:
                    unit.intent = "shoot"
                else:
                    unit.intent = "hold"

            else:
                unit.intent = "move"            

    def execute_unit_intent(self,dt):
        for unit in self.world.units:
            if unit.intent == "shoot":
                projectile = self.create_projectile(
                    unit.position, 
                    unit.target.position,
                    unit
                    )
                self.world.projectiles.append(projectile)
                unit.reload()

            elif unit.intent == "move":
                unit.move_towards_destination(dt)
            elif unit.intent == "hold":
                pass

            if unit.remaining_reload_duration > 0:
                unit.reduce_reload_duration()


    def create_projectile(self, unit_position, target_position, owner):
        projectile = Projectile(unit_position,
                                target_position,
                                owner,
                                constants.PROJECTILE_COLOR)
        return projectile
        
    def update_projectiles(self,dt):
        for projectile in self.world.projectiles:
            projectile.update(dt)

    def resolve_projectile_hits(self):
        projectiles_to_remove = []
        units_to_remove = []

        for projectile in self.world.projectiles:
            for unit in self.world.grid.query_radius(projectile.position, projectile.radius):
                if unit.faction == projectile.owner.faction:
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
            self.world.projectiles.remove(projectile) 

        for unit in units_to_remove:
            self.world.units.remove(unit)

            if unit.faction is constants.ALLY:
                self.world.allies.remove(unit)
            else:
                self.world.enemies.remove(unit)
