import sys

import pygame

import Settings
from Planet import Planet


class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Planet Orbit Simulator")
        self.screen = pygame.display.set_mode(
            (Settings.SCREEN_WIDTH, Settings.SCREEN_HEGHT)
        )
        self.clock = pygame.time.Clock()

        # Planet init
        self.Sun = Planet(0, 0, 50, (255, 255, 0), 1.98892 * 10**30, 0)
        self.Sun.is_sun = True

        self.Earth = Planet(
            -1 * Planet.AU, 0, 25, (100, 149, 237), 5.9742 * 10**24, -29.783 * 1000
        )
        self.Mars = Planet(
            -1.524 * Planet.AU, 0, 12, (80, 39, 50), 6.39 * 10**23, 24.077 * 1000
        )
        self.Mercury = Planet(
            0.387 * Planet.AU, 0, 8, (80, 78, 81), 3.30 * 10**23, -47.4 * 1000
        )
        self.Venus = Planet(
            0.723 * Planet.AU, 0, 18, (255, 255, 255), 4.8685 * 10**24, -35.02 * 1000
        )

        self.planets = [
            self.Sun,
            self.Earth,
            self.Mars,
            self.Mercury,
            self.Venus,
        ]

    def update(self):
        for planet in self.planets:
            planet.update_position(self.planets)

    def render(self):
        for planet in self.planets:
            planet.render(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")

            self.update()
            self.render()

            pygame.display.flip()
            self.clock.tick(60)
