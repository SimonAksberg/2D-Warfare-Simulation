import pygame
import constants
from camera import Camera
from infantry import Infantry
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

         # Create and store units
        self.units = []
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
        infantry_unit = Infantry(Vector2(0,random.randint(0,constants.SCREEN_HEIGHT)))
        return infantry_unit
    
    def create_destination(self):
        unit_destination = Vector2(
            random.randint(50,constants.SCREEN_WIDTH - 50), 
            random.randint(50,constants.SCREEN_HEIGHT - 50)
            )
        return unit_destination
    
    def update(self, dt):
        for unit in self.units:
            unit.update(dt)


    def render(self):
        for unit in self.units:
            screen_position = self.camera.world_to_screen(unit.position)    
            pygame.draw.circle(
                self.screen, 
                constants.INFANTRY_COLOR, 
                (round(screen_position.x), round(screen_position.y)),
                5
                )




