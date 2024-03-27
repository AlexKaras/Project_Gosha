import pygame.mixer
from gosha_consts import *

#Звуковые эффекты
pick_up_sound = pygame.mixer.Sound(SOUNDS_DIR + '/pick_up_effect.wav')
door_open_sound = pygame.mixer.Sound(SOUNDS_DIR + '/door_open_effect.wav')
door_block_sound = pygame.mixer.Sound(SOUNDS_DIR + '/door_block_effect.wav')
damage_sound = pygame.mixer.Sound(SOUNDS_DIR + '/damage_effect.wav')
defeat_sound = pygame.mixer.Sound(SOUNDS_DIR + '/defeat_effect.wav')
clear_sound = pygame.mixer.Sound(SOUNDS_DIR + '/stage_clear_effect.wav')