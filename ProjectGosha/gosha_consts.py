from pygame.locals import *

#Свойства экрана
SCREEN_SIZE = (1152, 784) #36X22 блока + верхняя планка
GAME_TITLE = "BUPYCOB.HET"
Y_OFFSET = 80
FRAME_COUNT_MAX = 10**6

#Директории
RESOURCES_DIR = 'resources'
SPRITES_DIR = RESOURCES_DIR + '/sprites'
SOUNDS_DIR = RESOURCES_DIR + '/sound'
MUSIC_DIR = RESOURCES_DIR + '/music'
LEVELS_DIR = "levels"
CODEX_DIR = "codex"
SAVES_DIR = "saves"

#Назначения клавиш
key_up = K_w
key_down = K_s
key_left = K_a
key_right = K_d
key_space = K_SPACE
key_esc = K_ESCAPE

debug_print_coords = K_HOME

#Константы цветов
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)

COLOR_LEVEL_BACKGROUND = (25, 51, 0)
COLOR_ERROR_BACKGROUND = (255, 0, 0)
COLOR_LEVEL_HUD = (51, 102, 0)
COLOR_MENU_BACKGROUND = (25, 51, 0)

COLOR_MESSAGE_BOX_BACKGROUND = (0, 204, 0)
#Значения по умолчанию
DEFAULT_HP = 3
MAX_HP = 6
