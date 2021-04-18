import pygame
from math import cos, sin, radians

SCREEN_DIMENSION = (1080, 720)

ratio = SCREEN_DIMENSION[0] / SCREEN_DIMENSION[1]

f = 0.1
s_y = 0.15
s_x = s_y * ratio
offset_x = SCREEN_DIMENSION[0] / 2
offset_y = SCREEN_DIMENSION[1] / 2
skew = 0


def projection(vec3, camera, rot_x, rot_y, kite=False, rot_x_kite=0):
    cos_rx = cos(radians(rot_x))
    sin_rx = sin(radians(rot_x))
    cos_ry = cos(radians(rot_y))
    sin_ry = sin(radians(rot_y))
    cos_rx_k = cos(radians(rot_x_kite))
    sin_rx_k = sin(radians(rot_x_kite))
    x = vec3.x - camera.x
    y = vec3.y - camera.y
    z = vec3.z - camera.z

    x = x * cos_ry + z * sin_ry
    z = x * -sin_ry + z * cos_ry

    y = y * cos_rx + z * -sin_rx
    z = y * sin_rx + z * cos_rx

    if kite:
        x = x * cos_rx_k + z * sin_rx_k
        z = x * -sin_rx_k + z * cos_rx_k

    x = x * ((f * offset_x * 2) / (2 * s_x)) + y * skew
    y = y * ((f * offset_y * 2) / (2 * s_y))
    z = -z

    x = x/z + offset_x
    y = -y/z + offset_y
    return pygame.Vector3(x, y, z)
