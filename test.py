import pygame, os
import random, sys

def terminate():
    pygame.quit()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def start_screen(listok, coord=10):
    fon = pygame.transform.scale(load_image('fon.png'), (600, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in listok:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)

intro_text = ["Это очень сырая версия", "",
             "Правила игры:",
             "Если вас заденет хоть одна пуля,",
             "то вы проиграете.",
             'Для продолжения нажмите любую клавишу']
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.mixer.music.load('data\\front.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
start_screen(intro_text)


class Player(pygame.sprite.Sprite):
    def __init__(self, im, sprites):
        super().__init__(sprites)
        self.image = pygame.transform.scale(im, (25, 25))
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, sprites):
        super().__init__(sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global k
        if k == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            k = 100
        else:
            k -= 1


class Blaster(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, sprites):
        self.flag = 0
        super().__init__(sheet, columns, rows, x, y, sprites)
        self.flip = pygame.transform.flip(self.image, 30, 0)
        self.image_rect = self.image.get_rect(center=(200, 150))
        self.image.blit(self.flip, self.image_rect)

    def update(self):
        global k2
        if k2 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            k2 = 8
            self.flag += 1
        else:
            k2 -= 1
        if self.flag == 5:
            self.kill()

    def shoot(self, x, y, pos2, pos3, screen):
        bullet = Bullet(pos2, pos3, x, y)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.pos_2 = (posx - x + 10) / 25
        self.pos_3 = (posy - y + 10) / 25

    def update(self):
        self.rect.y += self.pos_3
        self.rect.x += self.pos_2
        if self.rect.bottom < 0 and self.rect.centerx > 600:
            self.kill()


x = 250
y = 400
speed = 4
anim = True
flag = True
k = 0
k2 = 0
kol = 50
HEIGHT = 600
WIDTH = 600
poses = [[40, 450], [40, 300], [500, 450], [500, 300], [150, 180], [450, 180]]
coords = [300, 300]
spisok = ["GAME OVER"]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.mixer.music.load('data\\front_2.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

all_sprites = pygame.sprite.Group()
all_sprites_2 = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
clock = pygame.time.Clock()
heart = load_image("heart.png", -1)
heart1 = pygame.transform.scale(heart, (25, 25))
player = Player(heart, player_sprite)
player_sprite.add(player)
heads = AnimatedSprite(load_image("faces_2.png", -1), 7, 2, 260, 50, all_sprites)
torso = AnimatedSprite(load_image("tors_2.png"), 2, 1, 233, 100, all_sprites_2)

run = True
while run:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (150, 250, 290, 300), 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    all_sprites_2.draw(screen)
    all_sprites_2.update()
    all_sprites.draw(screen)
    all_sprites.update()
    player_sprite.draw(screen)
    keys = pygame.key.get_pressed()
    if keys [pygame.K_a] and x > 150:
        x -= speed
    if keys [pygame.K_d] and x < 440 - 27:
        x += speed
    if keys [pygame.K_w] and y > 252:
        y -= speed
    if keys [pygame.K_s] and y < 550 - 27:
        y += speed
    if kol == 0:
        kol = 50
        pos = random.choice(poses)
        pos2, pos3 = pos[0], pos[1]
        blast = Blaster(load_image("blasters3.png", -1), 6, 1, pos2, pos3, all_sprites)
        blast.shoot(x, y, pos2, pos3, screen)
    else:
        kol -= 1
    hits = pygame.sprite.spritecollide(player, all_sprites, True)
    if hits:
        run = False
    
    player.update(x, y)
    clock.tick(60)
    pygame.display.update()

pygame.mixer.music.load('data\\front_3.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
start_screen(spisok, 150)
terminate()

