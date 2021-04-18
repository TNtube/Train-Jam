import random
import noise
import pygame

from kite import Kite
from menu import menu
from polygon import Polygon
from projection import SCREEN_DIMENSION
from props import Prop
import os.path

Vec3 = pygame.Vector3


def distance(points, camera):
    return sum(p.distance_squared_to(camera) for p in points)


def perlin(poly, props=None):
    water = True
    depth_water = 0
    depth = 0
    for p in poly.points:
        v = noise.pnoise2(p.x / 8, p.z / 8, octaves=2) * 3
        if v < 0:
            depth_water -= v
            v = 0
        else:
            water = False
            depth += v
        p.y -= v * -5

    if water:
        color = (0, min(255, max(0, 150 - depth_water * 40)), min(255, max(0, 255 - depth_water * 30)))
        poly.perlin_depth = depth_water
        if poly.points[0].z % 10 == 0 and poly.points[0].x % 5 == 0 and props is not None:
            props.append(Prop(poly.points[0].x, min(depth_water * 2, 6.5), poly.points[0].z))
    else:
        color = (0, min(255, max(0, 255 - depth * 40)), 50)
    poly.color = color


def main(screen):
    running = True
    clock = pygame.time.Clock()
    speed = 7
    chunk_depth = 25
    chunk_width = 20
    bonus = 0
    coin_sound = pygame.mixer.Sound("SOUND/smw_coin.wav")
    explosion_sound = pygame.mixer.Sound("SOUND/airland.wav")
    explosion_sound.set_volume(0.2)
    best_score = 0
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as f:
            content = f.read()
            if content and content.isdigit():
                best_score = int(content)
    else:
        with open("score.txt", "w") as f:
            f.write("0")

    rx = 32
    ry = 0
    camera = pygame.Vector3(0, 5, 2)
    font = pygame.font.SysFont('arial', 30)
    sky = pygame.transform.flip(pygame.transform.scale(pygame.image.load("PNG/sky.png"), SCREEN_DIMENSION), False, True)

    pols = []
    for i in range(-chunk_width, chunk_width):
        for j in range(chunk_depth):
            pol = Polygon(i, 0, -j, (random.randint(0, 150), random.randint(200, 255), random.randint(0, 150)))
            perlin(pol)
            pols.append(pol)

    kite = Kite(-0.5, 1.5, 0)
    k_ry = 0
    while running:
        t = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pressed = pygame.key.get_pressed()
        camera.z -= speed * t
        if pressed[pygame.K_q]:
            camera.x -= speed * t
            for part in kite.polygons:
                for p in part.points:
                    p.x -= speed * t
            k_ry += 0.6
        elif pressed[pygame.K_d]:
            camera.x += speed * t
            for part in kite.polygons:
                for p in part.points:
                    p.x += speed * t
            k_ry -= 0.6
        else:
            if k_ry > 0:
                k_ry -= 1
            if k_ry < 0:
                k_ry += 1

        if k_ry > 10:
            k_ry = 10
        if k_ry < -10:
            k_ry = -10

        if pressed[pygame.K_SPACE]:
            camera.y += speed * t
            for part in kite.polygons:
                for p in part.points:
                    p.y += speed * t
        if pressed[pygame.K_LSHIFT]:
            camera.y -= speed * t
            for part in kite.polygons:
                for p in part.points:
                    p.y -= speed * t

        new_pol = []
        for pol in pols:
            if not isinstance(pol, Prop):
                if not pol.can_render_z(camera):
                    new_pol.append(Polygon(pol.x, pol.y, pol.z - chunk_depth, (random.randint(0, 150),
                                                                               random.randint(200, 255),
                                                                               random.randint(0, 150))))

                    perlin(new_pol[-1], new_pol)
                elif not pol.can_render_x_left(camera, chunk_width):
                    new_pol.append(Polygon(pol.x - chunk_width * 2, pol.y, pol.z, (random.randint(0, 150),
                                                                                   random.randint(200, 255),
                                                                                   random.randint(0, 150))))

                    perlin(new_pol[-1], new_pol)
                elif not pol.can_render_x_right(camera, chunk_width):
                    new_pol.append(Polygon(pol.x + chunk_width * 2, pol.y, pol.z, (random.randint(0, 150),
                                                                                   random.randint(200, 255),
                                                                                   random.randint(0, 150))))

                    perlin(new_pol[-1], new_pol)
                else:
                    new_pol.append(pol)
            else:
                new_pol.append(pol)

        pols = new_pol
        pols.sort(key=lambda s: distance(s.points, camera), reverse=True)

        screen.blit(sky, (0, 0))

        for pol in pols:
            pol.draw(screen, camera, rx, ry)
            if kite.collision(pol):
                kite.life -= 0.5
            if isinstance(pol, Prop):
                if pol.collide(kite):
                    bonus += 50
                    coin_sound.play()

        if kite.index < 10:
            for part in kite.polygons:
                for p in part.points:
                    p.z -= speed * t
                part.draw(screen, camera, rx, ry, k_ry)
            kite.rope_particles(screen, camera, rx, ry, k_ry, 200, 880)
        else:
            speed -= 1

        if kite.index == 1:
            explosion_sound.play()

        speed = max(speed, 0)
        s = int(-camera.z + bonus + 2)
        screen.blit(font.render(f"Score = {s}", True, (0, 0, 0)), (20, 20))
        screen.blit(font.render(f"Best score = {max(s, best_score)}", True, (0, 0, 0)), (20, 50))
        kite.draw_explosion(screen)

        kite.draw_life(screen)
        kite.draw_height(screen)

        pygame.display.flip()
        clock.tick()
        pygame.display.set_caption(f"{clock.get_fps():.2f}")
        if kite.index >= 71:
            if s > best_score:
                with open("score.txt", "w") as f:
                    f.write(str(s))
            return True


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMENSION)
    music = pygame.mixer.Sound('SOUND/music.mp3')
    music.set_volume(0.1)
    if menu(screen):
        music.play(loops=-1)
        while True:
            if not main(screen):
                break
    pygame.quit()
