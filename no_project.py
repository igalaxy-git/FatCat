# УПРАВЛЕНИЕ:
# Стрелочки на клавиатуре - движение кота по карте
# ESC в предыгровом меню - выход из игры
# ESC в игре - выход в предыгровое в меню (не сбрасывает игру)
# ENTER в игре - взаимодествие с объектами
#
# В меню можно использовать как клавиши (ENTER, ESC и стрелочки), так и мышку

import pygame
import os
import sys
import sys
from PyQt5 import uic
import sqlite3
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QAction, qApp, \
    QVBoxLayout, QScrollArea, QHBoxLayout, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from name import Ui_MainWindow

os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"  # Назначаются координаты позиции окна
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.NOFRAME)  # pygame.NOFRAME необходимо для вывода окна без рамок
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
clock = pygame.time.Clock()

WIDTH, HEIGHT, FPS = 1280, 758, 5  # Задаются размеры для поля и количество кадров в секунду
tile_height = tile_width = 100  # Задаются высота и ширина игровой клетки
player = None


punkts = [(570, 300, u'Играть', (11, 0, 77), pygame.Color('purple'), 0),  # Пункты предыгрового меню
          (570, 370, u'Выход', (11, 0, 77), pygame.Color('purple'), 1)]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        winner_name = self.lineEdit.text()
        self.edit_form = EditTable(self, winner_name, int(winner_time))
        self.edit_form.show()
        self.close()


class EditTable(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.setWindowIcon(QIcon("data/resources/cat1.png"))
        self.setWindowTitle('Table of Winners')
        self.con = sqlite3.connect("winners.db")
        self.cur = self.con.cursor()

        inf = (args[-2], args[-1])
        self.cur.execute("INSERT INTO Winners VALUES (?, ?)", inf)
        self.con.commit()
        result = self.cur.execute("SELECT * FROM Winners ORDER BY Time").fetchall()
        for i in range(len(result)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(result[i][1])))

        self.pushButton_2.clicked.connect(self.run)

    def run(self):
        main()
        self.close()


class Tile(pygame.sprite.Sprite):  # класс работы с текстурами
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def change_image(self, tile_type):
        self.image = tile_images[tile_type]

    def close(self):
        self.kill()


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y - 15)

    def step_top(self):
        self.rect.y -= tile_height
        self.image = player_image[3]

    def step_down(self):
        self.rect.y += tile_height
        self.image = player_image[2]

    def step_left(self):
        self.image = player_image[1]
        self.rect.x -= tile_width

    def step_right(self):
        self.image = player_image[0]
        self.rect.x += tile_width


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.transform.scale(enemy_image[0], (73, 100))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y - 15)

    def step_top_enemy(self):
        self.rect.y -= tile_height
        self.image = pygame.transform.scale(enemy_image[3], (73, 100))

    def step_down_enemy(self):
        self.rect.y += tile_height
        self.image = pygame.transform.scale(enemy_image[2], (80, 100))

    def step_left_enemy(self):
        self.image = pygame.transform.scale(enemy_image[1], (73, 100))
        self.rect.x -= tile_width

    def step_right_enemy(self):
        self.image = pygame.transform.scale(enemy_image[0], (73, 100))
        self.rect.x += tile_width


class NPC(pygame.sprite.Sprite):  # NPC - Non Player Character
    def __init__(self, pos_x, pos_y):
        super().__init__(new_group, all_sprites)
        self.image = new_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Menu:  # класс предыгрового меню
    def __init__(self, punkts):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for k in self.punkts:
            if num_punkt == k[5]:
                poverhnost.blit(font.render(k[2], 1, k[4]), (k[0], k[1] - 30))
            else:
                poverhnost.blit(font.render(k[2], 1, k[3]), (k[0], k[1] - 30))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('data/fonts/3572.ttf', 75)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            screen.blit(fon, (0, 0))
            mp = pygame.mouse.get_pos()
            for k in self.punkts:
                if k[0] < mp[0] < k[0] + 155 and k[1] < mp[1] < k[1] + 50:
                    punkt = k[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or \
                        (e.type == e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN):
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()
            window.blit(screen, (0, 30))
            pygame.display.flip()


class Camera:  # класс камеры за игроком
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data/resources/', name)
    image = pygame.image.load(fullname)
    if 'cat' in name:
        colorkey = -1
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/resources/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, new, new_enemy = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] == '*':
                Tile('floor', x, y)
                new = NPC(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '&':
                Tile('way', x, y)
            elif level[y][x] == 'C':
                Tile('chair', x, y)
            elif level[y][x] == 'c':
                Tile('destroyed_chair', x, y)
            elif level[y][x] == 'B':
                Tile('bed', x, y)
            elif level[y][x] == 'b':
                Tile('destroyed_bed', x, y)
            elif level[y][x] == 'D':
                Tile('wall_lower', x, y)
            elif level[y][x] == 'L':
                Tile('wall_topleft', x, y)
            elif level[y][x] == 'R':
                Tile('wall_topright', x, y)
            elif level[y][x] == 'l':
                Tile('wall_lowerleft', x, y)
            elif level[y][x] == 'r':
                Tile('wall_lowerright', x, y)
            elif level[y][x] == 'T':
                Tile('wall_top', x, y)
            elif level[y][x] == '@':
                Tile('floor', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'e':
                Tile('floor', x, y)
                new_enemy = Enemy(x, y)
    return new_player, x, y, new, new_enemy


tile_images = {'wall': load_image('house/black.png'), 'floor': load_image('house/floor.png'),
               'way': load_image('house/test.png'), 'chair': load_image('house/chair.png'),
               'destroyed_chair': load_image('house/destroyed_chair.png'), 'bed': load_image('house/bed.png'),
               'destroyed_bed': load_image('house/destroyed_bed.png'),
               'wall_topleft': load_image('house/wall_topleft.png'), 'wall_top': load_image('house/wall_top.png'),
               'wall_lower': load_image('house/wall_lower.png'), 'wall_topright': load_image('house/wall_topright.png'),
               'wall_lowerleft': load_image('house/wall_lowerleft1.png'),
               'wall_lowerright': load_image('house/wall_lowerright.png')}
player_image = load_image('cat/cat1.png'), load_image('cat/cat2.png'), \
               load_image('cat/cat3.png'), load_image('cat/cat4.png')

enemy_image = load_image('old woman/look_right.png').convert_alpha(), load_image('old woman/look_left.png'), \
               load_image('old woman/down.png'), load_image('old woman/up.png')

fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
new_image = load_image('house/new.png')

pygame.mixer.music.load('data/music/coupe.mp3')
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
new_group = pygame.sprite.Group()

winner_time = 0


def main():
    camera = Camera()
    data = load_level('map.txt')
    all_sprites.draw(screen)

    for i in range(len(data)):
        if '@' in data[i]:
            x = i
    y = data[x].index('@')
    player, level_x, level_y, NPC, enemy = generate_level(data)
    running = True
    show_menu = True
    game = Menu(punkts)
    DESTROYED_OBJECTS = 0
    CHAIR = 2
    BED = 1

    while running:
        if show_menu:
            pygame.mixer.music.stop()
            game.menu()
            show_menu = False
        pygame.mixer.music.play(loops=-1)
        screen.fill((0, 0, 0))
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # выход на ESC в предыгровое меню
                game.menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:  # движение кота
                if x > 0 and data[x - 1][y] == '.':
                    data[x] = data[x][:y] + '.' + data[x][y + 1:]
                    data[x - 1] = data[x - 1][:y] + '@' + data[x - 1][y + 1:]
                    x = x - 1
                    player.step_top()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if x < len(data[0]) and data[x + 1][y] == '.':
                    data[x] = data[x][:y] + '.' + data[x][y + 1:]
                    data[x + 1] = data[x + 1][:y] + '@' + data[x + 1][y + 1:]
                    x = x + 1
                    player.step_down()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if y < len(data[0]) - 1 and data[x][y + 1] == '.':
                    data[x] = data[x][:y] + '.' + data[x][y + 1:]
                    data[x] = data[x][:y + 1] + '@' + data[x][y + 2:]
                    y = y + 1
                    player.step_right()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if y > 0 and data[x][y - 1] == '.':
                    data[x] = data[x][:y] + '.' + data[x][y + 1:]
                    data[x] = data[x][:y - 1] + '@' + data[x][y:]
                    y = y - 1
                    player.step_left()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # взаимодествие с объектами на ENTER
                tiles_group.update()
                if CHAIR > 0:  # поверка есть ли целое кресло
                    if data[x + 1][y] == 'C':  # проверка есть ли снизу кресло
                        data[x + 1] = data[x + 1][:y] + 'c' + data[x + 1][y + 1:]
                        for obj in tiles_group:
                            if obj.pos_x == y and obj.pos_y == x + 1:
                                obj.change_image('destroyed_chair')
                        CHAIR -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x - 1][y] == 'C':  # проверка есть ли сверху кресло
                        data[x - 1] = data[x - 1][:y] + 'c' + data[x - 1][y + 1:]
                        for obj in tiles_group:
                            if obj.pos_x == y and obj.pos_y == x - 1:
                                obj.change_image('destroyed_chair')
                        CHAIR -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x][y + 1] == 'C':  # проверка есть ли справа кресло
                        data[x] = data[x][:y + 1] + 'c' + data[x][y + 2:]
                        for obj in tiles_group:
                            if obj.pos_x == y + 1 and obj.pos_y == x:
                                obj.change_image('destroyed_chair')
                        CHAIR -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x][y - 1] == 'C':  # проверка есть ли слева кресло
                        data[x] = data[x][:y - 1] + 'b' + data[x][y:]
                        for obj in tiles_group:
                            if obj.pos_x == y - 1 and obj.pos_y == x:
                                obj.change_image('destroyed_chair')
                        CHAIR -= 1
                        DESTROYED_OBJECTS += 1
                if BED > 0:  # проверка есть ли целая кровать
                    if data[x + 1][y] == 'B':  # проверка есть ли снизу кровать
                        data[x + 1] = data[x + 1][:y] + 'b' + data[x + 1][y + 1:]
                        for obj in tiles_group:
                            if obj.pos_x == y and obj.pos_y == x + 1:
                                obj.change_image('destroyed_bed')
                        BED -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x - 1][y] == 'B':  # проверка есть ли сверху кровать
                        data[x - 1] = data[x - 1][:y] + 'b' + data[x - 1][y + 1:]
                        for obj in tiles_group:
                            if obj.pos_x == y and obj.pos_y == x - 1:
                                obj.change_image('destroyed_bed')
                        BED -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x][y + 1] == 'B':  # проверка есть ли справа кровать
                        data[x] = data[x][:y + 1] + 'b' + data[x][y + 2:]
                        for obj in tiles_group:
                            if obj.pos_x == y + 1 and obj.pos_y == x:
                                obj.change_image('destroyed_bed')
                        BED -= 1
                        DESTROYED_OBJECTS += 1
                    elif data[x][y - 1] == 'B':  # проверка есть ли слева кровать
                        data[x] = data[x][:y - 1] + 'b' + data[x][y:]
                        for obj in tiles_group:
                            if obj.pos_x == y - 1 and obj.pos_y == x:
                                obj.change_image('destroyed_bed')
                        BED -= 1
                        DESTROYED_OBJECTS += 1
        # проверка есть ли рядом enemy
        if data[x + 1][y] == 'e' or data[x - 1][y] == 'e' or data[x][y + 1] == 'e' or data[x][y - 1] == 'e':
            show_menu = True
            data = load_level('map.txt')
            main()

        if DESTROYED_OBJECTS == 3:  # проверяем уничтожил ли кот все объекты
            global winner_time
            winner_time = pygame.time.get_ticks() // 1000
            app = QApplication(sys.argv)
            ex = MainWindow()
            ex.show()
            sys.exit(app.exec())

        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


main()
