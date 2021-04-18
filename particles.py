import pygame
import random


class Particle:
    def __init__(self, position, direction, lifetime):
        self.position = list(position)
        self.direction = list(direction)
        self.lifetime = lifetime

    def update(self):
        self.position[0] += self.direction[0]

        self.position[1] += self.direction[1]

        self.lifetime -= 0.2
        self.position[1] += 0.5

    def draw(self, screen):
        pygame.draw.circle(screen,
                           (random.randint(150, 255), random.randint(150, 255), 20),
                           self.position, self.lifetime/5)
