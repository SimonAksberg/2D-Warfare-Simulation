import pygame
import constants

class Simulation():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Warfare Simulation")

        self.running = True

    def run(self):
        # Simulation loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill screen with background color to wipe away anything from previous frame
            self.screen.fill(constants.BACKGROUND_COLOR)

            # This is where the actual simulation should take place


            # Updates window based on what has happened in game loop
            pygame.display.flip()

        pygame.quit()



