import pygame
from pygame.locals import *
import math
from time import time
from sys import exit

DEFAULT_SCREEN_WIDTH = 1080
DEFAULT_SCREEN_HEIGHT = 750
RAQUETTE_HEIGHT = 76
RAQUETTE_SPEED = 6
BALL_SPEED_START = 4
ACCELERATION_BALL_SPEED = 1
FULLSCREEN = True
POINT_TO_WIN = 50

# do ont change these value

SCREEN_WIDTH = DEFAULT_SCREEN_WIDTH
SCREEN_HEIGHT = DEFAULT_SCREEN_HEIGHT


class Raquette(pygame.sprite.Sprite):
    def __init__(self, **pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, RAQUETTE_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(**pos)
        self.score = 0

    def move(self, value):
        if value < 0:
            if not self.rect.top < 0:
                self.rect.move_ip((0, value * RAQUETTE_SPEED))
        elif value > 0:
            if not self.rect.bottom > SCREEN_HEIGHT:
                self.rect.move_ip((0, value * RAQUETTE_SPEED))


class Player:
    def __init__(self, raquette: Raquette):
        self.score = 0
        self.raquette = raquette


class Ball(pygame.sprite.Sprite):
    def __init__(self, **pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(**pos)
        self.speed = self.speed_x, self.speed_y = [BALL_SPEED_START, 0]

    def move(self):
        self.rect.move_ip(self.speed)

    def collide(self, *args: Rect, player1, player2):
        for arg in args:
            if self.rect.inflate(self.speed_x*2, 0).colliderect(arg):
                if self.rect.top >= arg.bottom or self.rect.bottom <= arg.top:
                    self.speed[1] = -self.speed[1]
                else:
                    distance = self.rect.centery - arg.centery
                    if distance > 0:
                        self.speed = [-self.speed[0], math.tan(
                            math.radians((62.5 / (RAQUETTE_HEIGHT / 2)) * abs(distance))) * self.speed_x]
                    elif distance < 0:
                        self.speed = [-self.speed[0], -math.tan(
                            math.radians((62.2 / (RAQUETTE_HEIGHT / 2)) * abs(distance))) * self.speed_x]
                    else:
                        self.speed = [-self.speed[0], -self.speed[1]]
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed = [self.speed[0], -self.speed[1]]
        if self.rect.left < 0:
            player2.score += 1
            self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.speed = [-self.speed[0], 0]
        if self.rect.right > SCREEN_WIDTH:
            player1.score += 1
            self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.speed = [-self.speed[0], 0]


def main():
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global FULLSCREEN

    def wait_start():
        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        global FULLSCREEN
        win.fill((1, 1, 1))
        text = font.render("Appuyer sur n'importe quelle touche pour commencer", True, (255, 255, 255))
        text_rect = text.get_rect(center=win.get_rect().center)
        win.blit(text, text_rect)
        pygame.display.flip()
        screen = pygame.display.get_surface()
        height = screen.get_height
        width = screen.get_width
        while 1:
            broken = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if FULLSCREEN:
                            pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
                            FULLSCREEN = False
                            text_rect = text.get_rect(center=win.get_rect().center)
                            win.blit(text, text_rect)
                            pygame.display.flip()
                        else:
                            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            FULLSCREEN = True
                            text_rect = text.get_rect(center=win.get_rect().center)
                            win.blit(text, text_rect)
                            pygame.display.flip()
                        SCREEN_HEIGHT = height()
                        SCREEN_WIDTH = width()
                    else:
                        broken = True
                if event.type == pygame.VIDEORESIZE:
                    SCREEN_WIDTH = width()
                    SCREEN_HEIGHT = height()
                    text_rect = text.get_rect(center=win.get_rect().center)
                    win.blit(text, text_rect)
                    pygame.display.flip()
            if broken:
                break

    pygame.init()
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    if FULLSCREEN:
        win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        win = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
    screen = pygame.display.get_surface()
    height = screen.get_height
    width = screen.get_width
    SCREEN_HEIGHT = height()
    SCREEN_WIDTH = width()
    pygame.display.set_caption("Pong")
    wait_start()
    raquette1 = Raquette(topleft=(10, SCREEN_HEIGHT / 2))
    raquette2 = Raquette(topright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT / 2))
    raquettes = pygame.sprite.RenderPlain((raquette1, raquette2))
    player1 = Player(raquette1)
    player2 = Player(raquette2)
    ball1 = Ball(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    allsprites = pygame.sprite.RenderPlain((raquette1, raquette2, ball1))

    previous_time = time()
    while 1:
        if time() - previous_time >= 20:
            if ball1.speed[0] > 0:
                ball1.speed[0] += ACCELERATION_BALL_SPEED
            if ball1.speed[0] < 0:
                ball1.speed[0] -= ACCELERATION_BALL_SPEED
            previous_time = time()
        win.fill((1, 1, 1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.dict['w']
                SCREEN_HEIGHT = event.dict['h']
                raquette2.rect.right = SCREEN_WIDTH - 10
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if FULLSCREEN:
                        ball_pos_ratio_x = width() / ball1.rect.centerx
                        pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
                        FULLSCREEN = False
                        text_rect = text.get_rect(center=win.get_rect().center)
                        win.blit(text, text_rect)
                        ball1.rect.centerx = width() / ball_pos_ratio_x

                        raquette2.rect.right = width() - 10
                        pygame.display.flip()
                    else:
                        ball_pos_ratio_x = width() / ball1.rect.centerx
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        FULLSCREEN = True
                        ball1.rect.centerx = width() / ball_pos_ratio_x
                        text_rect = text.get_rect(center=win.get_rect().center)
                        win.blit(text, text_rect)
                        raquette2.rect.right = width() - 10
                        pygame.display.flip()
                SCREEN_HEIGHT = height()
                SCREEN_WIDTH = width()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            raquette2.move(-1)
        if keys[pygame.K_DOWN]:
            raquette2.move(1)
        if keys[pygame.K_z]:
            raquette1.move(-1)
        if keys[pygame.K_s]:
            raquette1.move(1)
        ball1.collide(raquette1.rect, raquette2.rect, player1=player1, player2=player2)
        ball1.move()
        allsprites.draw(win)
        text = font.render(f"{player1.score} - {player2.score}", True, (255, 255, 255))
        text_rect = text.get_rect(centerx=win.get_rect().centerx)
        win.blit(text, text_rect)
        pygame.display.flip()
        if player1.score >= 50 or player2.score >= 50:
            break
        clock.tick(60)

    if player1.score >= POINT_TO_WIN:
        text_win = font.render("Le joueur de gauche à gagnée", True, (255, 255, 255))
    if player2.score >= POINT_TO_WIN:
        text_win = font.render("Le joueur de droite à gagnée", True, (255, 255, 255))
    while 1:
        win.fill((1,1,1))
        text_win_rect = text.get_rect(center=win.get_rect().center)
        win.blit(text_win, text_win_rect)
        pygame.display.flip()
        screen = pygame.display.get_surface()
        height = screen.get_height
        width = screen.get_width
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if FULLSCREEN:
                        pygame.display.set_mode((width(), height()), pygame.RESIZABLE)
                        FULLSCREEN = False
                        text_rect = text.get_rect(center=win.get_rect().center)
                        win.blit(text, text_rect)
                        pygame.display.flip()
                    else:
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        FULLSCREEN = True
                    SCREEN_HEIGHT = height()
                    SCREEN_WIDTH = width()
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = width()
                SCREEN_HEIGHT = height()
                text_rect = text.get_rect(center=win.get_rect().center)
                win.blit(text, text_rect)
                pygame.display.flip()


if __name__ == '__main__':
    main()
