import pygame
from projection import SCREEN_DIMENSION


def menu(screen):
    sky = pygame.transform.flip(pygame.transform.scale(pygame.image.load("PNG/sky.png"), SCREEN_DIMENSION), False, True)
    title = pygame.image.load("PNG/title.png")
    title.set_colorkey((255, 255, 255))
    play = pygame.transform.scale(pygame.image.load("PNG/play.png"), (700, 240))
    play.set_colorkey((255, 255, 255))
    play_rect = play.get_rect(x=screen.get_width() // 2 - play.get_width() // 2, y=300)
    credit = pygame.transform.scale(pygame.image.load("PNG/credits.png"), (315, 135))
    credit.set_colorkey((255, 255, 255))
    credit_rect = credit.get_rect(x=screen.get_width() // 2 - play.get_width() // 2 + credit.get_width()*0.1, y=550)
    commands = pygame.transform.scale(pygame.image.load("PNG/commands.png"), (315, 135))
    commands.set_colorkey((255, 255, 255))
    commands_rect = commands.get_rect(x=screen.get_width() // 2 + play.get_width() // 2 - commands.get_width()*1.1, y=550)
    running = True
    draw_play = False
    draw_credit = False
    draw_commands = False
    blit_credit = False
    blit_commands = False
    thanks = pygame.transform.scale(pygame.image.load("PNG/thanks.png"), SCREEN_DIMENSION)
    thanks.set_colorkey((255, 255, 255))
    keys = pygame.transform.scale(pygame.image.load("PNG/keys.png"), SCREEN_DIMENSION)
    keys.set_colorkey((255, 255, 255))
    while running:
        screen.blit(sky, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if not (blit_credit or blit_commands):
                if event.type == pygame.MOUSEMOTION:
                    if not play_rect.collidepoint(*event.pos):
                        draw_play = False
                    else:
                        draw_play = True
                    if not credit_rect.collidepoint(*event.pos):
                        draw_credit = False
                    else:
                        draw_credit = True
                    if not commands_rect.collidepoint(*event.pos):
                        draw_commands = False
                    else:
                        draw_commands = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_rect.collidepoint(*event.pos):
                        return True
                    if commands_rect.collidepoint(*event.pos):
                        blit_commands = True
                    if credit_rect.collidepoint(*event.pos):
                        blit_credit = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if blit_commands:
                    blit_commands = False
                if blit_credit:
                    blit_credit = False

        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        if draw_play:
            pygame.draw.rect(screen, (200, 200, 200), play_rect)
        if draw_commands:
            pygame.draw.rect(screen, (200, 200, 200), commands_rect)
        if draw_credit:
            pygame.draw.rect(screen, (200, 200, 200), credit_rect)
        screen.blit(play, play_rect)
        screen.blit(credit, credit_rect)
        screen.blit(commands, commands_rect)
        if blit_commands:
            screen.blit(sky, (0, 0))
            screen.blit(keys, (0, 0))
        if blit_credit:
            screen.blit(sky, (0, 0))
            screen.blit(thanks, (0, 0))

        pygame.display.flip()

