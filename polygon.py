import pygame.math
from projection import projection
import pygame.gfxdraw


class Polygon:
    def __init__(self, x: float, y: float, z: float, color):
        self.x = x
        self.y = y
        self.z = z
        self.color = list(color)
        self.points = [
            pygame.Vector3(0, 0, 0),  # BOTTOM LEFT
            pygame.Vector3(1, 0, 0),  # BOTTOM RIGHT
            pygame.Vector3(1, 0, 1),  # TOP RIGHT
            pygame.Vector3(0, 0, 1)  # TOP LEFT
        ]
        self.set_pos(x, y, z)
        self.perlin_depth = 0

    def set_pos(self, x: float, y: float, z: float) -> None:
        for p in self.points:
            p.xyz = [p.x + x, p.y + y, p.z + z]

    def can_render_z(self, camera: pygame.Vector3):
        return not all(camera.z - p.z < -3 for p in self.points)

    def can_render_x_left(self, camera: pygame.Vector3, chunk_w: int):
        return not all(camera.x - p.x < -chunk_w for p in self.points)

    def can_render_x_right(self, camera: pygame.Vector3, chunk_w: int):
        return not all(camera.x - p.x > chunk_w for p in self.points)

    def draw(self, screen: pygame.Surface, camera: pygame.Vector3, rx: int, ry: int, water: int = None) -> None:
        points2d = []
        z = 0
        vec3_cloud = None
        clouds2d = []
        zn = 0
        for p in self.points:
            if self.perlin_depth > 2:
                vec3_cloud = projection(pygame.Vector3(p.x, p.y + 7, p.z), camera, rx, ry)
            vec3 = projection(p, camera, rx, ry)
            if (-screen.get_width() < vec3.x < screen.get_width() * 2 and
                    -screen.get_height() * 1 < vec3.y < screen.get_height() * 1.5):
                z += vec3.z
                points2d.append(pygame.Vector2(*vec3.xy))
            if vec3_cloud is not None:
                if (-screen.get_width() < vec3_cloud.x < screen.get_width() * 2 and
                        -screen.get_height() * 1 < vec3_cloud.y < screen.get_height() * 1.5):
                    zn += vec3_cloud.z
                    clouds2d.append(pygame.Vector2(*vec3_cloud.xy))
        if len(points2d) > 2:
            dz = z
            c = [min(max(0, dz * 2) + self.color[0], 255),
                 min(max(0, dz * 2) + self.color[1], 255),
                 min(max(0, dz * 2) + self.color[2], 255)]
            if dz > 5:
                pygame.gfxdraw.filled_polygon(screen, points2d, c)
            if self.perlin_depth > 2 and len(clouds2d) > 2 and zn > 5:
                pygame.gfxdraw.filled_polygon(screen, clouds2d,
                                              (min(255 - 10 * self.perlin_depth, 255),
                                               min(255 - 10 * self.perlin_depth, 255),
                                               min(255 - 10 * self.perlin_depth, 255)))


def average(points):
    return sum(p.z for p in points)
