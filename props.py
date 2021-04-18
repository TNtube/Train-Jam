import pygame
from projection import projection


class Prop:
    def __init__(self, x, y, z):
        self.points = [pygame.Vector3(x, y, z)]
        self.color = (255, 215, 0)

    def draw(self, screen: pygame.Surface, camera: pygame.Vector3, rx: int, ry: int):
        vec3 = projection(self.points[0], camera, rx, ry)
        if (-screen.get_width() < vec3.x < screen.get_width() * 2 and
                -screen.get_height() * 1 < vec3.y < screen.get_height() * 1.5):
            c = [min(max(0, vec3.z * 2) + self.color[0], 255),
                 min(max(0, vec3.z * 2) + self.color[1], 255),
                 min(max(0, vec3.z * 2) + self.color[2], 255)]
            if vec3.z > 0:
                pygame.draw.circle(screen, c, vec3.xy, 30, 10)

    def can_render_z(self, camera: pygame.Vector3):
        return not all(camera.z - p.z < 3 for p in self.points)

    def can_render_x_left(self, camera: pygame.Vector3, chunk_w: int):
        return not all(camera.x - p.x < -chunk_w for p in self.points)

    def can_render_x_right(self, camera: pygame.Vector3, chunk_w: int):
        return not all(camera.x - p.x > chunk_w for p in self.points)

    def collide(self, kite):
        vec3 = self.points[0]
        left = kite.polygons[1].points[0]
        right = kite.polygons[0].points[2]
        top = kite.polygons[3].points[1]
        bottom = kite.polygons[1].points[2]
        if kite.polygons[0].points[0].z <= vec3.z <= kite.polygons[0].points[0].z + 0.5:
            if (left.x - 1 <= vec3.x <= right.x + 1 and
                    bottom.y - 1 <= self.points[0].y <= top.y + 2):
                return True
