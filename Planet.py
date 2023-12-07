import math

import pygame

import Settings


class Planet:
    AU = 149.6e6 * 1000  # Astronomical Unit -> distance from the Sun to the Earth
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU
    TIMESTEP = 86400  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass, y_velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.font = pygame.font.SysFont("Roboto", 32)

        self.x_velocity = 0
        self.y_velocity = y_velocity
        self.orbit = list()
        self.is_sun = False
        self.distance_to_sun = 0

    def calculate_force_of_attraction(self, planet) -> tuple:
        difference_x = planet.x - self.x
        difference_y = planet.y - self.y
        difference = math.sqrt(difference_x**2 + difference_y**2)

        if planet.is_sun:
            self.distance_to_sun = difference

        # Force of attraction formula -> F = G*ma*mb/d^2
        force = self.G * ((self.mass * planet.mass) / difference**2)
        # Theta angle -> tan(theta) = y / x -> tan^-1(y / x) = theta
        theta = math.atan2(difference_y, difference_x)
        # Force X -> Force X = cos(theta) * Force
        force_x = math.cos(theta) * force
        # Force Y -> Force Y = sin(theta) * Force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_force_x = 0
        total_force_y = 0
        for planet in planets:
            if self is planet:
                continue

            force_x, force_y = self.calculate_force_of_attraction(planet)
            total_force_x += force_x
            total_force_y += force_y

        # Formula for accelaration -> a = f / m
        self.x_velocity += total_force_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def render(self, screen):
        drawn_x = self.x * self.SCALE + Settings.SCREEN_WIDTH / 2
        drawn_y = self.y * self.SCALE + Settings.SCREEN_HEGHT / 2

        # Can't use pygame.draw.lines() unless the list's length is > 2
        if len(self.orbit) > 2:
            new_points = list()
            for point in self.orbit:
                point_x, point_y = point
                point_x = point_x * self.SCALE + Settings.SCREEN_WIDTH / 2
                point_y = point_y * self.SCALE + Settings.SCREEN_HEGHT / 2
                new_points.append((point_x, point_y))
            pygame.draw.lines(screen, self.color, False, new_points, 2)

        pygame.draw.circle(screen, self.color, (drawn_x, drawn_y), self.radius)

        if self.is_sun is False:
            distance_to_sun_text = self.font.render(
                f"{round(self.distance_to_sun / 1000, 2)} km", 1, (255, 255, 255)
            )
            screen.blit(
                distance_to_sun_text,
                (
                    drawn_x - distance_to_sun_text.get_width() / 2,
                    drawn_y - distance_to_sun_text.get_height() / 2,
                ),
            )
