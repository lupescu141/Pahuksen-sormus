#!/usr/bin/python
import pygame
from pygame.locals import *



def main():
    pygame.init()
    pygame.display.set_caption('End credits')
    screen = pygame.display.set_mode((800, 600))
    screen_r = screen.get_rect()
    font = pygame.font.SysFont("Arial", 40)
    clock = pygame.time.Clock()

    credit_list = ["KREDIITIT - PAHUKSEN SORMUS"," ","Daniel - Developer","Janne - Developer", "Henna - Developer", "Gitta - Developer"]

    texts = []
    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (10, 10, 10))
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.fill((255, 255, 255))

        for r, s in texts:
            r.move_ip(0, -1)
            screen.blit(s, r)

        if not screen_r.collidelistall([r for (r, _) in texts]):
            return

        pygame.display.flip()
        clock.tick(60)

