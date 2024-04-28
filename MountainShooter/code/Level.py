import random
import sys

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Const import COLOR_WHITE, MENU_OPTION, EVENT_ENEMY
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window, name, menu_option):
        self.window: Surface = window
        self.name = name
        self.mode = menu_option  # Opção do Menu
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Player1'))
        if menu_option in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2'))
        pygame.time.set_timer(EVENT_ENEMY, 6000)

    def run(self):
        # pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        # pygame.mixer_music.play(-1)
        # pygame.mixer_music.set_volume(0.1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            # Desenha na tela as entidades
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # Desenha o FPS na tela
            self.level_text(20, f'FPS: {clock.get_fps() :.0f}', COLOR_WHITE, (10, 10))
            self.level_text(20, f'EntityList: {len(self.entity_list)}', COLOR_WHITE, (10, 25))
            # Atualiza na tela o FPS
            pygame.display.flip()
            # Verificar relacionamento de entidades
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)
            # Confere eventos recebidos na fila
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lacida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
