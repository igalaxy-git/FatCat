import pygame
import os
import sys

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

WIDTH, HEIGHT, FPS = 500, 500, 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if name == 'mario.png':
        colorkey = -1
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'), 'way': load_image('test.png')}
player_image = load_image('mario.png')
new_image = load_image('new.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class NPlayer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(new_group, all_sprites)
        self.image = new_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
new_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y, new = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                new = NPlayer(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '&':
                Tile('way', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y, new


start_screen()
data = load_level('map.txt')
all_sprites.draw(screen)

for i in range(len(data)):
    if '@' in data[i]:
        x = i
y = data[x].index('@')
running = True
while running:
    player, level_x, level_y, nplayer = generate_level(data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if y > 0 and data[x][y - 1] == '.':
                data[x] = data[x][:y] + '.' + data[x][y + 1:]
                data[x] = data[x][:y - 1] + '@' + data[x][y:]
                y -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if y < len(data[0]) and data[x][y + 1] == '.':
                data[x] = data[x][:y] + '.' + data[x][y + 1:]
                data[x] = data[x][:y + 1] + '@' + data[x][y + 2:]
                y += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if x > 0 and data[x - 1][y] == '.':
                data[x] = data[x][:y] + '.' + data[x][y + 1:]
                data[x - 1] = data[x - 1][:y] + '@' + data[x - 1][y + 1:]
                x -= 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if x < len(data[0]) and data[x + 1][y] == '.':
                data[x] = data[x][:y] + '.' + data[x][y + 1:]
                data[x + 1] = data[x + 1][:y] + '@' + data[x + 1][y + 1:]
                x += 1
    all_sprites.draw(screen)
    pygame.display.flip()


