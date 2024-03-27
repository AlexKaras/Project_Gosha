import pygame
from gosha_consts import *

#Класс Спрайта
class SpriteClass(pygame.sprite.Sprite):
    def __init__(self, fname):
        self.image = pygame.image.load(SPRITES_DIR + '/' + fname).convert()
        self.image.set_colorkey((0, 0, 0))
        self.img_rect = self.image.get_rect()

    def draw(self, img_x, img_y, screen):
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        screen.blit(self.image, self.img_rect)

#Игрок
player_idle_sprite = [SpriteClass("player_idle.png")]
player_anim_sprite = [SpriteClass("player_anim_0.png"), SpriteClass("player_anim_1.png")]

#Курсор
cursor_sprite = [SpriteClass("cursor.png")]

#Враги
enemy_sprite = [[SpriteClass("virus_type0_0.png"), SpriteClass("virus_type0_1.png"), SpriteClass("virus_type0_2.png")]]


wall_sprite = [[SpriteClass("wall_0.png")], [SpriteClass("wall_1.png")]]
door_sprite = [SpriteClass('door.png')]


heal_sprite = [SpriteClass("heal_0.png"), SpriteClass("heal_1.png")]
key_sprite = [SpriteClass("key.png")]
bonus_sprite_group = {'key': key_sprite, 'heal': heal_sprite}

file_sprite = [SpriteClass("file0.png")]

portal_inactive_sprite = [SpriteClass("portal_bad.png")]
portal_active_sprite = [SpriteClass("portal_good.png")]

#Элементы интерфейса
#Иконка здоровья
hp_icon_sprite_0 = SpriteClass("health_icon_0.png")
hp_icon_sprite = [hp_icon_sprite_0]
#Иконка ключей
key_icon_sprite = [SpriteClass("key_icon_0.png")]


#Логотип
logo_sprite = [SpriteClass("Logo.png")]
