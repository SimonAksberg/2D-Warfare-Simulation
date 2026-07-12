import pygame
from camera import Camera
import constants

class Renderer:

    def __init__(self):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.camera = Camera()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)
        )

        self.show_grid = False

        pygame.display.set_caption("Warfare Simulation")


    def draw(self, world):
        self.screen.fill(constants.BACKGROUND_COLOR)
        self.draw_units(world.units)
        self.draw_projectiles(world.projectiles)

        if self.show_grid:
            self.draw_grid(world.grid)

        
    def draw_units(self, units):
        for unit in units:
            unit_screen_position = self.camera.world_to_screen(unit.position) 

            pygame.draw.circle(
                self.screen, 
                unit.color, 
                (round(unit_screen_position.x), round(unit_screen_position.y)),
                unit.radius
                )
            
    def draw_projectiles(self, projectiles):
        for projectile in projectiles:
            projectile_screen_position = self.camera.world_to_screen(projectile.position)

            pygame.draw.circle(
                self.screen,
                projectile.color,
                (round(projectile_screen_position.x), round(projectile_screen_position.y)),
                projectile.radius
                )
            
    def draw_grid(self, grid):
        # Draw horizontal lines
        for x in range(0, constants.SCREEN_WIDTH + 1, constants.CELL_SIZE):
            screen_x = x - self.camera.position.x

            pygame.draw.line(
                self.screen,
                constants.GRID_COLOR,
                (screen_x, 0),
                (screen_x, constants.SCREEN_HEIGHT)
            )
        
        # Draw vertical lines
        for y in range(0, constants.SCREEN_HEIGHT + 1, constants.CELL_SIZE):
            screen_y = y - self.camera.position.y

            pygame.draw.line(
                self.screen,
                constants.GRID_COLOR,
                (0, screen_y),
                (constants.SCREEN_WIDTH, screen_y)
            )

        for cell, units in grid.cells.items():
            # Calculate world coordinates from cell coordinates
            screen_x = cell[0] * grid.cell_size
            screen_y = cell[1] * grid.cell_size

            text = self.my_font.render(str(len(units)), True, (255, 255, 255) )

            self.screen.blit(
                text,
                (screen_x, screen_y)
            )