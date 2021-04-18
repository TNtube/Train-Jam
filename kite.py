import random
import pygame
from projection import projection, SCREEN_DIMENSION
from polygon import Polygon
import pygame.gfxdraw
from particles import Particle
from os import path


class Triangle(Polygon):
    def __init__(self, color, points):
        super().__init__(0, 0, 0, color)
        self.points = points

    def draw(self, screen: pygame.Surface, camera: pygame.Vector3, rx: int, ry: int, k_rx: int = None) -> None:
        points2d = []
        z = 0
        for p in self.points:
            vec3 = projection(p, camera, rx, ry, True, k_rx)
            if (-screen.get_width() < vec3.x < screen.get_width() * 2 and
                    -screen.get_height() < vec3.y < screen.get_height() * 2):
                z += vec3.z
                points2d.append(pygame.Vector2(*vec3.xy))
            if len(points2d) > 2:
                pygame.draw.polygon(screen, 'white', points2d, 3)
                pygame.gfxdraw.filled_polygon(screen, points2d, self.color)


class Kite:
    def __init__(self, x: float, y: float, z: float):
        self.polygons = [
            # RIGHT WING
            Triangle((255, 0, 0),
                     [pygame.Vector3(1, 1, 1),  # A
                      pygame.Vector3(1, 1, 1.5),  # B
                      pygame.Vector3(2, 1.3, 1.5)  # C
                      ]),
            # LEFT WING
            Triangle((255, 0, 0),
                     [pygame.Vector3(-1, 1.3, 1.5),  # F
                      pygame.Vector3(0, 1, 1.5),  # D
                      pygame.Vector3(0, 1, 1)  # E
                      ]),
            # BODY
            Triangle((200, 100, 0),
                     [pygame.Vector3(1, 1, 1),  # A
                      pygame.Vector3(1, 1, 1.5),  # B
                      pygame.Vector3(0, 1, 1.5),  # D
                      pygame.Vector3(0, 1, 1)  # E
                      ]),
            # HEAD
            Triangle((200, 0, 100),
                     [pygame.Vector3(1, 1, 1.5),  # B
                      pygame.Vector3(0.7, 1, 2),  # H
                      pygame.Vector3(0.3, 1, 2),  # G
                      pygame.Vector3(0, 1, 1.5)  # D
                      ]),
        ]
        for triangle in self.polygons:
            for p in triangle.points:
                p.z = -p.z + 2
                p.x += x
                p.y += y
                p.z += z
        self.particles = []
        self.life = 100
        self.life_bar = pygame.transform.scale(pygame.image.load("PNG/lifebar.png"), (240, 180))
        self.explosions = [
            pygame.transform.scale(pygame.image.load(path.join("PNG", f"frame00{i:02d}.png")), (400, 400))
            for i in range(71)
        ]
        self.index = 0
        self.up_bar = pygame.image.load("PNG/up_bar.png")
        self.up_bar.set_colorkey((255, 255, 255))
        self.max_height = 6.5

    def rope_particles(self, screen: pygame.Surface, camera: pygame.Vector3, rx: int, ry: int, k_rx, x1: int, x2: int):
        left = projection(self.polygons[1].points[0], camera, rx, ry, True, k_rx)
        right = projection(self.polygons[0].points[2], camera, rx, ry, True, k_rx)
        pygame.draw.line(screen, "grey", (x1, SCREEN_DIMENSION[1]), left.xy, 2)
        pygame.draw.line(screen, "grey", (x2, SCREEN_DIMENSION[1]), right.xy, 2)
        body_left = projection(self.polygons[0].points[0], camera, rx, ry, True, k_rx)
        body_right = projection(self.polygons[1].points[2], camera, rx, ry, True, k_rx)
        self.particles.append(Particle((body_left.x - random.randint(0, abs(int(body_right.x - body_left.x))),
                                        body_left.y + 10),
                                       (0, 10),
                                       random.randint(10, 30)))
        self.particles.append(Particle((body_right.x + random.randint(0, abs(int(body_right.x - body_left.x))),
                                        body_right.y + 10),
                                       (0, 10),
                                       random.randint(10, 30)))

        for particle in self.particles:
            particle.update()
            particle.draw(screen)

    def collision(self, polygon):
        body_min = min_vec3(self.polygons[2])
        body_max = max_vec3(self.polygons[2])
        body_min.x += -0.2
        body_max.x += 0.2

        body_min.y += 0.5
        body_max.y += 0.5
        poly_min = min_vec3(polygon)
        poly_max = max_vec3(polygon)
        return (((body_min.x <= poly_max.x and body_max.x >= poly_min.x) and
                (body_min.y <= poly_max.y and body_max.y >= poly_min.y) and
                (body_min.z <= poly_max.z and body_max.z >= poly_min.z)) or
                body_min.y <= 0 or body_max.y >= self.max_height)

    def draw_explosion(self, screen):
        if self.life <= 0 and self.index <= 70:
            screen.blit(self.explosions[self.index], (340, 320))
            self.index += 1

    def draw_life(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() - self.life_bar.get_width() + 5,
                                               50, int(190 * self.life / 100), 25))
        screen.blit(self.life_bar, (screen.get_width() - self.life_bar.get_width() - 20, -20))

    def draw_height(self, screen):
        y = self.polygons[0].points[0].y
        y = min(6, y)
        cross = y * (self.up_bar.get_height() - 10) / self.max_height
        screen.blit(self.up_bar, (screen.get_width() - self.up_bar.get_width() - 20, 400))
        pygame.draw.circle(screen, (255, 0, 0), (screen.get_width() - self.up_bar.get_width() + 24, 660 - cross), 15)


def min_vec3(polygon):
    vec3 = pygame.Vector3()
    vec3.x = min(p.x for p in polygon.points)
    vec3.y = min(p.y for p in polygon.points)
    vec3.z = min(p.z for p in polygon.points)
    return vec3


def max_vec3(polygon):
    vec3 = pygame.Vector3()
    vec3.x = max(p.x for p in polygon.points)
    vec3.y = max(p.y for p in polygon.points)
    vec3.z = max(p.z for p in polygon.points)
    return vec3
