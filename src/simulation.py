import pygame
import constants
from infantry import Infantry
import random


class Simulation():
    def __init__(self):
        # Setup
        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Warfare Simulation")

        self.clock = pygame.time.Clock()
        self.running = True

         # Create and store units
        self.units = []

        for _ in range(constants.NUMBER_OF_UNITS):
            self.units.append(self.create_unit())
        

    def run(self):
        # Simulation loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            # Fill screen with background color to wipe away anything from previous frame
            self.screen.fill(constants.BACKGROUND_COLOR)

            # This is where the actual simulation should take place
            self.update()

            self.render()


            # Updates window based on what has happened in game loop
            pygame.display.flip()

            self.clock.tick(constants.FPS) #Limits simulation a certain fps

        pygame.quit()
    
    def create_unit(self):
        infantry_unit = Infantry(
            random.randint(0, constants.SCREEN_WIDTH),
            random.randint(0, constants.SCREEN_HEIGHT),
            random.randint(0,1),
            random.randint(0,1)
            )
        return infantry_unit
    
    def update(self):
        for unit in self.units:
            unit.update()


    def render(self):
        for unit in self.units:
            pygame.draw.circle(
                self.screen, 
                constants.INFANTRY_COLOR, 
                (unit.x, unit.y),
                5 
                )




