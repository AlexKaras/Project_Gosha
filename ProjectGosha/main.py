#Подключение библиотек
import os.path

import pygame
from gosha_consts import * #Подключение констант


#Инициализация Pygame
pygame.init()

#Инициализация экрана
screen = pygame.display.set_mode(SCREEN_SIZE)

from gosha_classes import * #Подключение классов

pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

#Инициализация переменных
game_cycle = True
game_stage = 0
frames_count = 0

level_id = 0
level_stage_id = 0
change_stage_flag = False #Флаг переключения уровня в конце кадра
first_frame_flag = True
hard_mode = False

#Инициализация уровня
stage_data = LevelStageSetup()

#Инициализация игрока
player = Player(2, 2, 20, 20, player_idle_sprite, speed=3, delay=20)

#Загрузка ресурсов
try:
    from gosha_sprites import *

except:
    game_stage = -1

from gosha_sound import *

#Инициализация списка уровней
try:
    level_names = []
    stages = []
    f1 = open(LEVELS_DIR + '/levels.txt')
    for line in f1:
        line = line.replace("\n", "") #Убираем перенос на новую строку
        level_names.append(line)
        stages_names = []
        f2 = open(LEVELS_DIR + '/' + line + "/stages.txt")
        for _line in f2:
            _line = _line.replace("\n", "")#Убираем перенос на новую строку
            stages_names.append(_line)
        stages.append(stages_names)
        f2.close()
    f1.close()
    stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
    player.move_to(stage_data.start_pos[0] * 32, stage_data.start_pos[1] * 32 + Y_OFFSET)
except:
    game_stage = -1



#Объекты интерфейса
hud_objects = {
    'hp_icon':image_display(20,10, hp_icon_sprite), 'hp_string':text_display(96,12,text="<0>", color=COLOR_GREEN),
    'keys_icon':image_display(160,10,key_icon_sprite), 'keys_string':text_display(240,12,text="<0>", color=COLOR_GREEN),
    'score_dsiplay':text_display(500, 12, text='Счёт:000000', color=COLOR_GREEN)
}

#Инициализация контроллера сообщений
msg_controller = MessageBoxController()

#Инициализация меню
main_menu = MenuController(100,400,["start", "codex", "credits", "exit"],["Игра", "Кодекс", "Авторы", "Выход"])
static_menu_elements = [image_display(500, 10, logo_sprite)]
dynamic_menu_elements = []

#Инициализация Кодекса
Codex = Codex_Controller()
Codex.get_from_files()
Codex.load()



#Инициализация экранов меню
#Экран ошибки
error_text = [
        text_display(100, 100, text="ОШИБКА", color=COLOR_BLACK, font=font_menu),
        text_display(100, 200, text="Файлы игры повреждены", color=COLOR_BLACK, ),
        text_display(100, 250, text="Переустановите игру из источника", color=COLOR_BLACK, )
             ]
#Авторы
credits_text = [
    text_display(50, 50, text="Над игрой работали:", color=COLOR_GREEN),
    text_display(700, 50, text="esc -вернуться на главную", color=COLOR_GREEN),
    text_display(50, 220, text="Красин Александр", color=COLOR_GREEN, font=font_menu),
    text_display(70, 270, text="Тимлидер, разработчик", color=COLOR_GREEN),
    text_display(50, 340, text="Забродина Елизавета", color=COLOR_GREEN, font=font_menu),
    text_display(70, 390, text="Разработчик", color=COLOR_GREEN),
    text_display(50, 460, text="Лаврикова Елена", color=COLOR_GREEN, font=font_menu),
    text_display(70, 510, text="Художник", color=COLOR_GREEN),
    text_display(50, 580, text="Точилин Никита", color=COLOR_GREEN, font=font_menu),
    text_display(70, 630, text="Разработчик", color=COLOR_GREEN)
    ]
#Кодекс
codex_text = [text_display(700, 50, text="esc -вернуться на главную", color=COLOR_GREEN)]

#Выбор режима игры
mode_menu = MenuController(100,400,["new", "new_hard", "load", "back"], ["Новая Игра(Легко)", "Новая Игра(Сложно)", "Загрузить", "На Главную"])

#
win_text = [text_display(380,200,text="Поздравляем!", color=COLOR_GREEN, font=font_menu),
            text_display(450, 360, text="Вы прошли игру!", color=COLOR_GREEN),
            text_display(435, 420, text="Ваш счёт:<00000>", color=COLOR_GREEN),
            text_display(350, 500, text="Пробел - вернуться на главную", color=COLOR_GREEN)]
#Основной цикл игры
while game_cycle:
    clock.tick(60)
    #Оброботка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_cycle = False
    pressed = pygame.key.get_pressed()
    #Тело цикла
    player_pos = player.coords()
    match game_stage:
        case -1:#Экран ошибки
            screen.fill(COLOR_ERROR_BACKGROUND)
            for elem in error_text:
                elem.draw(screen)
            pygame.display.flip()
        case 0: #Этап главного меню
            screen.fill(COLOR_MENU_BACKGROUND)


            main_menu.read_control(pressed)
            main_menu.update(screen)

            #Команды меню
            if pressed[key_space]:
                option = main_menu.get_option()
                match option:
                    case "start": #Начало игры
                        mode_menu.cooldown = 10
                        game_stage = 3
                    case "codex":
                        game_stage = 1
                    case "credits":
                        game_stage = 2
                    case "exit":
                        game_cycle = False


            #Рендер
            for elem in static_menu_elements:
                elem.draw(screen, frames_count)
            pygame.display.flip()

        case 1: #кодекс
            screen.fill(COLOR_MENU_BACKGROUND)

            Codex.read_controls(pressed)
            Codex.show_entry(screen)

            if pressed[key_esc]:
                game_stage = 0

            for elem in codex_text:
                elem.draw(screen)

            pygame.display.flip()

        case 2: #Авторы
            screen.fill(COLOR_MENU_BACKGROUND)

            if pressed[key_esc]:
                game_stage = 0

            for elem in credits_text:
                elem.draw(screen)

            pygame.display.flip()

        case 3: #Выбор режима игры
            screen.fill(COLOR_MENU_BACKGROUND)

            mode_menu.read_control(pressed)
            mode_menu.update(screen)

            if pressed[key_space]:
                option = mode_menu.get_option()
                player.keys = 0
                player.hp = DEFAULT_HP
                match option:
                    case "new":
                        game_stage = 10
                        level_id = 0
                        level_stage_id = 0
                        stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
                        player.move_to(stage_data.start_pos[0] * 32, stage_data.start_pos[1] * 32 + Y_OFFSET)
                        msg_controller.add_message_box("Цель:Найти выход с уровня", duration=80)
                        msg_controller.add_message_box("Избегайте Вирусов, собирайте ключи и записки", duration=80)
                    case "new_hard":
                        player.hard_mode = True
                        game_stage = 10
                        level_id = 0
                        level_stage_id = 0
                        msg_controller.add_message_box("Цель:Найти выход с уровня", duration=80)
                        msg_controller.add_message_box("Избегайте Вирусов, собирайте ключи и записки", duration=80)
                        msg_controller.add_message_box("Сложный Режим: Игра начнётся с начала в случае проигрыша", duration=80)
                        stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
                        player.move_to(stage_data.start_pos[0] * 32, stage_data.start_pos[1] * 32 + Y_OFFSET)
                    case "load":
                        if os.path.isfile(SAVES_DIR+"/player_save.txt"):
                            level_data = player.load()
                            level_id = int(level_data[0])
                            level_stage_id = int(level_data[1])
                            stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
                            msg_controller.add_message_box("Сохранение загружено", duration=80)
                        else:
                            level_id = 0
                            level_stage_id = 0
                            msg_controller.add_message_box("Сохранение не найдено. Новая игра", duration=80)
                            msg_controller.add_message_box("Цель:Найти выход с уровня", duration=80)
                            msg_controller.add_message_box("Избегайте Вирусов, собирайте ключи и записки", duration=80)
                            stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
                            player.move_to(stage_data.start_pos[0] * 32, stage_data.start_pos[1] * 32 + Y_OFFSET)
                        game_stage = 10
                    case "back":
                        game_stage = 0
            if pressed[key_esc]:
                game_stage = 0


            pygame.display.flip()
        case 11: #Победа
            screen.fill(COLOR_MENU_BACKGROUND)
            win_text[2] = text_display(435, 420, text="Ваш счёт:%7d"%(player.score), color=COLOR_GREEN)
            for elem in win_text:
                elem.draw(screen)
            if pressed[key_space]:
                game_stage = 0
                main_menu.cooldown = 20
            pygame.mixer_music.stop()

            pygame.display.flip()
        case 10:#Этап уровня

            # Очистка экрана
            screen.fill(COLOR_LEVEL_BACKGROUND)

            #Первый кадр
            if first_frame_flag:
                pygame.mixer_music.load(stage_data.music_path)
                pygame.mixer_music.play(-1)
                first_frame_flag = False
                for entry in stage_data.codex_notes:
                    if Codex.entry_status(entry.codex_id):
                        stage_data.codex_notes.remove(entry)


            #Действия игрока
            player.read_controls(pressed)
            if pressed[key_esc]:
                game_stage = 0
                pygame.mixer_music.stop()
                first_frame_flag = True

            #Столкновение со стенами
            col_id = player.collide_get_id(stage_data.walls)
            if col_id != -1:
                player.move_to(player_pos[0], player_pos[1])

            #Столкновение с врагами
            col_id = player.collide_get_id(stage_data.enemies)
            if col_id != -1:
                player.add_hp(-1)
                damage_sound.play()
                stage_data.enemies.pop(col_id)

            # Столкновение с бонусами
            col_id = player.collide_get_id(stage_data.bonuses)
            if col_id != -1:
                pick_up_sound.play()
                player.add_keys(stage_data.bonuses[col_id].add_keys)
                player.add_hp(stage_data.bonuses[col_id].add_hp)
                player.add_score(stage_data.bonuses[col_id].score)
                stage_data.bonuses.pop(col_id)

            #Столкновения с записками
            col_id = player.collide_get_id(stage_data.codex_notes)
            if col_id != -1:
                pick_up_sound.play()
                Codex.unlock(stage_data.codex_notes[col_id].codex_id)
                print(stage_data.codex_notes[col_id].codex_id + "666")
                Codex.save()
                msg_controller.add_message_box("Запись Открыта. Загляните в Кодекс", duration=60)
                stage_data.codex_notes.pop(col_id)

            #Столкновение с дверями
            col_id = player.collide_get_id(stage_data.doors)
            if col_id != -1:
                if player.keys > 0:
                    stage_data.doors.pop(col_id)
                    player.keys -= 1
                    door_open_sound.play()
                else:
                    player.move_to(player_pos[0], player_pos[1])
                    door_block_sound.play()

            #Движение противников
            for obj in stage_data.enemies:
                obj.move_by_vector()
                col_id = obj.collide_get_id(stage_data.walls)
                if col_id != -1:
                    obj.v_x = -obj.v_x
                    obj.v_y = -obj.v_y

            #Проверка порталов
            col_id = player.collide_get_id(stage_data.portals)
            for i in range(len(stage_data.portals)):
                    stage_data.portals[i].change_sprite(portal_active_sprite)
                    if col_id == i:
                        change_stage_flag = True
                        level_id = stage_data.portals[i].new_lvl
                        level_stage_id = stage_data.portals[i].new_stg
                        player.start_pos = stage_data.portals[i].new_player_pos
                        clear_sound.play()


            #Проверка на проигрыш
            if player.hp <= 0:
                if player.hard_mode:
                    level_id = 0
                    level_stage_id = 0
                    player.score = 0
                    player.save(level_id, level_stage_id)
                change_stage_flag = True
                player.hp = DEFAULT_HP
                if player.score > 500:
                    player.score -= 500
                else:
                    player.score = 0
                defeat_sound.play()


            # Рендер
            #_Игровые объекты
            for obj in stage_data.walls:
                obj.draw_stat(screen)
            for obj in stage_data.enemies:
                obj.draw_anim(screen, frames_count, obj.delay)
            for obj in stage_data.bonuses:
                obj.draw_anim(screen, frames_count, obj.delay)
            for obj in stage_data.doors:
                obj.draw_stat(screen)
            for obj in stage_data.portals:
                obj.draw_stat(screen)
            for obj in stage_data.codex_notes:
                obj.draw_stat(screen)
            player.draw_anim(screen, frames_count, player.delay)

            #_Интерфейс
            pygame.draw.rect(screen, COLOR_LEVEL_HUD, pygame.Rect(0,0,SCREEN_SIZE[0],Y_OFFSET))
            #Здоровье
            hud_objects["hp_icon"].draw(screen, frames=frames_count, delay=32)
            hud_objects["hp_string"].text=str(player.hp)
            hud_objects["hp_string"].draw(screen)
            #Ключи
            hud_objects["keys_icon"].draw(screen, frames=frames_count, delay=32)
            hud_objects["keys_string"].text = str(player.keys)
            hud_objects["keys_string"].draw(screen)
            #Счёт
            hud_objects['score_dsiplay'].text = 'Счёт:' + str(player.score)
            hud_objects['score_dsiplay'].draw(screen)

            #Сообщения
            msg_controller.update_message_box(screen)

            #Переключение уровня
            if change_stage_flag:
                try:
                    if level_id == -1:
                        game_stage = 11
                    else:
                        stage_data.read_stage_data(level_names[level_id], stages[level_id][level_stage_id])
                        player.move_to(stage_data.start_pos[0] * 32, stage_data.start_pos[1] * 32 + Y_OFFSET)
                        player.save(level_id, level_stage_id)
                        player.keys = 0
                        change_stage_flag = False
                        first_frame_flag = True
                except:
                    game_stage = -1

    pygame.display.flip()
    if frames_count > FRAME_COUNT_MAX:
        frames_count = 0
    frames_count += 1


