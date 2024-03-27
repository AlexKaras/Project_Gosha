import os.path

from gosha_consts import *
from gosha_sprites import *
from gosha_fonts import *
import pygame

#Класс исключение
class GoshaException(Exception):
    pass
#Класс статического элемента
class StaticObject:
    def __init__(self, x, y, col_rect_w, col_rect_h, sprite, delay = 60):
        self.pos_x = x
        self.pos_y = y
        self.col_rect = pygame.Rect(10, 0 + Y_OFFSET, col_rect_w, col_rect_h)
        self.obj_sprite = sprite
        self.col_rect.center = (x + 16, y + 16)
        self.delay = delay

    def collide_get_id(self, col_list):
        res = -1
        for i in range(len(col_list)):
            if self.col_rect.colliderect(col_list[i].col_rect):
                res = i
        return res

    def change_sprite(self, sprite):
        self.obj_sprite = sprite

    def draw_anim(self, screen, frames, delay = 1):
        spr_id = frames // delay % len(self.obj_sprite)
        self.obj_sprite[spr_id].draw(self.pos_x,self.pos_y,screen)

    def draw_stat(self, screen, spr_id=0):
        self.obj_sprite[spr_id].draw(self.pos_x, self.pos_y, screen)

class DynamicObject(StaticObject):
    def __init__(self, x, y, col_rect_w, col_rect_h, sprite, speed= 1, v_x= 1, v_y= 1, delay=60):
        super().__init__(x, y, col_rect_w, col_rect_h, sprite, delay)
        self.speed = speed;
        self.v_x = v_x
        self.v_y = v_y

    def coords(self):
            return (self.pos_x, self.pos_y)

    def move_to(self, x, y):
            self.pos_x = x
            self.pos_y = y
            self.col_rect.center = (self.pos_x + 16, self.pos_y + 16)

    def move_by_vector(self):
         self.pos_x += self.speed * self.v_x
         self.pos_y += self.speed * self.v_y
         self.col_rect.center = (self.pos_x + 16, self.pos_y + 16)


class Player(DynamicObject):
    def __init__(self, x, y, col_rect_w, col_rect_h, sprite, speed = 1, delay=60):
        super().__init__(x * 32, y*32 + Y_OFFSET, col_rect_w, col_rect_h, sprite, speed, delay=60)
        self.hp = DEFAULT_HP
        self.keys = 0
        self.score = 0
        self.direction = 0
        self.hard_mode = False

    def read_controls(self, pressed):
        if (pressed[key_up] or pressed[key_down] or  pressed[key_right] or pressed[key_left]):
            self.obj_sprite = player_anim_sprite
            if pressed[key_up]:
                self.pos_y -= self.speed
                self.direction = 0
            if pressed[key_down]:
                self.pos_y += self.speed
                self.direction = 1
            if pressed[key_right]:
                self.pos_x += self.speed
                self.direction = 2
            if pressed[key_left]:
                self.pos_x -= self.speed
                self.direction = 3
            self.col_rect.center = (self.pos_x + 16, self.pos_y + 16)
        else:
            self.obj_sprite = player_idle_sprite
        if pressed[debug_print_coords]:
            print(self.coords())

    def add_hp(self, ammount):
        if (self.hp + ammount < MAX_HP) and (self.hp + ammount > 0):
            self.hp += ammount
        elif self.hp + ammount >=  MAX_HP:
            self.hp = MAX_HP
        else:
            self.hp = 0

    def add_keys(self,keys):
        self.keys += keys

    def add_score(self, val):
        self.score += val
        if self.score < 0:
            self.score = 0

    def save(self, level, stage, fname="player_save.txt"):
        with open(SAVES_DIR+"/" + fname, encoding = 'utf-8', mode = 'w') as f:
            f.write(str(level) + " " + str(stage) + "\n")
            f.write(str(self.pos_x) + " " + str(self.pos_y) + "\n")
            f.write(str(self.hp) + "\n")
            f.write(str(self.score) + "\n")

    def load(self, fname="player_save.txt"):
        if os.path.isfile(SAVES_DIR + "/" + fname):
            with open(SAVES_DIR + "/" + fname, encoding='utf-8', mode='r') as f:
                level_data = f.readline().strip().split()
                coords = f.readline().strip().split()
                self.move_to(int(coords[0]), int(coords[1]))
                self.hp = int(f.readline())
                self.score = int(f.readline())
                return level_data

class Enemy(DynamicObject):
    def __init__(self, x, y, col_rect_w, col_rect_h, sprite, speed=1, v_x=1, v_y= 1, delay=60):
        super().__init__(x, y, col_rect_w, col_rect_h, sprite, speed, v_x, v_y, delay)

class Bonus(StaticObject):
    def __init__(self,x,y,col_rect_w,col_rect_h,sprite,add_keys=0, add_hp=0, coin=False, anti=False, score=0, delay=60):
        super().__init__(x,y,col_rect_w,col_rect_h,sprite, delay)
        self.add_keys = add_keys
        self.add_hp = add_hp
        self.score = score

class CodexNote(StaticObject):
    def __init__(self, x, y, col_rect_w, col_rect_h, sprite, codex_id, delay=60):
        super(CodexNote, self).__init__(x,y,col_rect_w, col_rect_h, sprite, delay)
        self.codex_id = codex_id

class Portal(StaticObject):
    def __init__(self,x,y,col_rect_w,col_rect_h,sprite, new_lvl, new_stg, new_player_pos, delay=60, IgnoreObjectives=False):
        super().__init__(x, y, col_rect_w, col_rect_h, sprite, delay)
        self.new_lvl = new_lvl
        self.new_stg = new_stg
        self.new_player_pos = new_player_pos


class LevelStageSetup():
    def __init__(self):
        self.start_pos = [0, 0]
        self.music_path = ""
        self.walls = []
        self.enemies = []
        self.bonuses = []
        self.doors = []
        self.portals = []
        self.codex_notes = []

    def read_stage_data(self, level_name, stage_name):
        #Очищение данных
        self.walls = []
        self.enemies = []
        self.bonuses = []
        self.doors = []
        self.portals = []
        self.codex_notes = []

        #Информация об уровне
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + '/info.txt') as f:
            ss = f.readlines()
            self.start_pos = [int(ss[0].split()[0]), int(ss[0].split()[1])]
            self.music_path = MUSIC_DIR + '/' + ss[1].split()[0]
            if not os.path.exists(self.music_path):
                raise GoshaException()

        #Стены
        with open(LEVELS_DIR+'/'+level_name+'/'+stage_name+'/layout.txt') as f:
            for y, line in enumerate(f):
                line_ = line.strip("\n")
                for x, char in enumerate(line_):
                    if char != ' ':
                        if char == '@':
                            self.walls.append(StaticObject(x * 32, y * 32 + Y_OFFSET, 32, 32, wall_sprite[1]))
                        else:
                            self.walls.append(StaticObject(x * 32, y * 32 + Y_OFFSET, 32, 32, wall_sprite[0]))

        #Противники
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + '/enemies_list.txt') as f:
            ss = f.readlines()
            for s in ss:
                if s[0] != '#':
                    _ss = s.split()
                    x = int(_ss[0])
                    y = int(_ss[1])
                    v_x = float(_ss[2])
                    v_y = float(_ss[3])
                    sprite = enemy_sprite[int(_ss[4])]
                    speed = int(_ss[5])
                    delay = int(_ss[6])
                    self.enemies.append(Enemy(x*32, y*32 + Y_OFFSET, 28, 28, sprite, speed=speed, v_x=v_x, v_y=v_y, delay=delay))
        #Бонусы
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + '/bonuses_list.txt') as f:
            ss = f.readlines()
            for s in ss:
                if s[0] != '#':
                    _ss = s.split()
                    x = int(_ss[0])
                    y = int(_ss[1])
                    sprite = bonus_sprite_group[_ss[2]]
                    keys = int(_ss[3])
                    hp = int(_ss[4])
                    score = int(_ss[5])
                    delay = int(_ss[6])
                    self.bonuses.append(Bonus(x*32, y*32 + Y_OFFSET, 28, 28, sprite, add_keys=keys, add_hp=hp, score=score, delay=delay))
        #Двери
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + '/doors_list.txt') as f:
            ss = f.readlines()
            for s in ss:
                if s[0] != '#':
                    _ss = s.split()
                    x = int(_ss[0])
                    y = int(_ss[1])
                    self.doors.append(StaticObject(x*32,y*32 + Y_OFFSET,32,32, door_sprite))
        #Порталы
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + '/portals_list.txt') as f:
            ss = f.readlines()
            for s in ss:
                if s[0] != '#':
                    _ss = s.split()
                    x = int(_ss[0])
                    y = int(_ss[1])
                    level = int(_ss[2])
                    stage = int(_ss[3])
                    player_pos = [int(_ss[4]), int(_ss[5])]
                    delay = int(_ss[6])
                    self.portals.append(Portal(x*32,y*32+Y_OFFSET, 20, 20, portal_inactive_sprite,level,stage,player_pos,delay=delay))

        #Записи
        with open(LEVELS_DIR + '/' + level_name + '/' + stage_name + "/codex.txt") as f:
            ss = f.readlines()
            for s in ss:
                if s[0] != "#":
                    _ss = s.split()
                    x = int(_ss[0])
                    y = int(_ss[1])
                    id = _ss[2]
                    self.codex_notes.append(CodexNote(x*32, y*32+Y_OFFSET, 20, 20, file_sprite, id))

class image_display():
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, screen, frames=0, delay = 1):
        spr_id = frames // delay % len(self.sprite)
        self.sprite[spr_id].draw(self.x, self.y,screen)

class text_display():
    def __init__(self, x, y, font=font_standart, text="", color=COLOR_BLACK):
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.color = color

    def draw(self, screen):
        img = self.font.render(self.text, True, self.color)
        rect = img.get_rect()
        rect.x = self.x
        rect.y = self.y
        screen.blit(img, rect)

class MessageBox():
    def __init__(self, text, font, color, font_color, duration):
        self.text = text
        self.font = font
        self.color = color
        self.font_color = font_color
        self.duration = duration
        self.height = font.get_height() + 20
        self.width = len(text) * 20 + 60

    def show(self, screen):
        back_rect = pygame.Rect(500, 500, self.width, self.height)
        frame_rect = pygame.Rect(500, 500, self.width + 20, self.height + 20)
        text_img = self.font.render(self.text, True, self.font_color)
        text_rect = text_img.get_rect()
        back_rect.center = (SCREEN_SIZE[0] // 2, (SCREEN_SIZE[1] - Y_OFFSET) // 2)
        text_rect.center = back_rect.center
        frame_rect.center = back_rect.center
        pygame.draw.rect(screen, self.font_color, frame_rect)
        pygame.draw.rect(screen, self.color, back_rect)
        screen.blit(text_img, text_rect)

class MessageBoxController():
    def __init__(self):
        self.message_list = []
    def add_message_box(self, text, font=font_standart, color=COLOR_MESSAGE_BOX_BACKGROUND, font_color=COLOR_BLACK, duration=360):
        self.message_list.append(MessageBox(text, font, color, font_color, duration))
    def update_message_box(self, screen):
        if len(self.message_list) > 0:
            self.message_list[0].duration -= 1
            if self.message_list[0].duration > 0:
                self.message_list[0].show(screen)
            else:
                self.message_list.pop(0)

class MenuController():
    def __init__(self, x, y, options, names):
        self.x = x
        self.y = y
        self.options_list = options
        self.names_list = names
        self.cursor_pos = 0
        self.cooldown = 0

    def read_control(self, pressed):
        if self.cooldown == 0:
            if pressed[key_up]:
                self.cursor_pos -= 1
                self.cooldown = 20
            if pressed[key_down]:
                self.cursor_pos += 1
                self.cooldown = 20

            if self.cursor_pos <= -1:
                self.cursor_pos = len(self.names_list) - 1
            else:
                self.cursor_pos = self.cursor_pos % len(self.names_list)


    def update(self, screen):
        cursor = image_display(self.x, self.y + 10 + (self.cursor_pos * 80), cursor_sprite)
        for i in range(len(self.names_list)):
           line = text_display(self.x + 60, self.y + (i * 80), text=self.names_list[i], color=COLOR_GREEN, font=font_menu)
           line.draw(screen)
        cursor.draw(screen)
        if self.cooldown > 0:
            self.cooldown -= 1
    def get_option(self):
        if self.cooldown == 0:
            return self.options_list[self.cursor_pos]

class Codex_Entry():
    def __init__(self,fname):
        with open(CODEX_DIR + "/" + fname, encoding = 'utf-8', mode = 'r') as f_in:
            self.visible = bool(int(f_in.readline().strip()))
            self.id = f_in.readline().strip()
            self.lines = f_in.readlines()
    def unlock(self):
        self.visible = True

class Codex_Controller():
    def __init__(self):
        self.n = 0
        self.cooldown = 0
        self.entries = []
    def entry_status(self, id):
        status = False
        for entry in self.entries:
            if entry.id == id:
                status = entry.visible
        return status

    def unlock(self, id):
        for entry in self.entries:
            if entry.id == id:
                entry.unlock()

    def show_entry(self, screen):
        entry = self.entries[self.n]
        if entry.visible:
            text_display(50, 100, text="Запись  %2d"%(self.n+1), font=font_menu, color=COLOR_GREEN).draw(screen)
            text_display(50, 300, text=entry.lines[0].strip(), color=COLOR_GREEN).draw(screen)
            for i in range(1, len(entry.lines)):
                text_display(70, 320 + i * 50, text=entry.lines[i].strip(), color=COLOR_GREEN).draw(screen)
        else:
            text_display(50, 100, text="Запись  %2d"%(self.n+1), font=font_menu, color=COLOR_GREEN).draw(screen)
            text_display(50, 300, text="Запись заблокирована", color=COLOR_GREEN).draw(screen)
            text_display(50, 350, text="Найдите файл на уровне игры, чтобы её разблокировать", color=COLOR_GREEN).draw(screen)

    def read_controls(self, pressed):
        if self.cooldown == 0:
            if pressed[key_right]:
                self.n += 1
                if self.n >= len(self.entries):
                    self.n = 0
                self.cooldown = 20
            if pressed[key_left]:
                self.n -=1
                if self.n < 0:
                    self.n = len(self.entries) - 1
                self.cooldown = 20
        else:
            self.cooldown -= 1

        if pressed[key_up] and pressed[key_space]:
            for entry in self.entries:
                entry.unlock()

    def get_from_files(self):
        entry_files = os.listdir(CODEX_DIR)
        for fname in entry_files:
            self.entries.append(Codex_Entry(fname))
    def save(self, fname="codex_save.txt"):
        with open(SAVES_DIR+"/" + fname, encoding = 'utf-8', mode = 'w') as f:
            for entry in self.entries:
                f.write(entry.id.strip() + ":" + str(int(entry.visible)) + "\n")
    def load(self, fname="codex_save.txt"):
        if os.path.isfile(SAVES_DIR+"/" + fname):
            with open(SAVES_DIR+"/" + fname, encoding = 'utf-8', mode = 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    line = line.split(":")
                    if int(line[1]):
                        self.unlock(line[0])

    def debug_entry_status(self):
        for entry in self.entries:
            print(entry.id + ":" + str(entry.visible))
