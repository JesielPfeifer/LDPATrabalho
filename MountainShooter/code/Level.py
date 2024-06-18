import random
import sys

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Const import C_WHITE, MENU_OPTION, EVENT_ENEMY, WIN_HEIGHT, C_GREEN, C_CYAN, EVENT_TIMEOUT
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, menu_option: str, playe_score: list[int]):
        self.window: Surface = window
        self.name = name
        self.mode = menu_option  # Opção do Menu
        self.timeout = 20000
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        '''
            Para cada vez que for criado um player, será criado um score para esse jogador que será passado para a
            proxima fase, o score pertence ao Game e não ao Level porque ele tem que ser "universal" nas fases.
        '''
        player = EntityFactory.get_entity('Player1')
        player.score = playe_score[0]  # Score do player 1
        self.entity_list.append(player)
        if menu_option in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2'))
            player2 = EntityFactory.get_entity('Player2')
            player2.score = playe_score[1]  # Score do player 2
            self.entity_list.append(player)

        # Criando os eventos de geração de Enemy e validador da fase.
        pygame.time.set_timer(EVENT_ENEMY, 3000)
        pygame.time.set_timer(EVENT_TIMEOUT, 100)  # a cada 100ms sera validado se a fase foi vencida ou não

    def run(self, player_score: list[int]):
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
                if ent.name == 'Player1':
                    self.level_text(20, f'Health P1: {ent.health} | Score {ent.score}', C_GREEN, (10, 20))
                if ent.name == 'Player2':
                    self.level_text(20, f'Health P2: {ent.health} | Score {ent.score}', C_CYAN, (10, 35))
            # Desenha o FPS na tela
            self.level_text(20, f'FPS: {clock.get_fps() :.0f}', C_WHITE, (10, WIN_HEIGHT - 30))
            self.level_text(20, f'EntityList: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 15))
            self.level_text(20, f'{self.name} - Timeout {self.timeout / 1000 :.1f}s', C_WHITE, (10, 5))
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
                if event.type == EVENT_TIMEOUT:  # acontece a cada 100ms
                    self.timeout -= 100  # Timeout começa com 20.000
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True
                if not found_player:
                    return False

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lacida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
