import pygame
from math import sin, cos, pi, atan
from random import randint
from random import choice
import sqlite3
import os

w = 600
h = 600
bgcolor = (50, 100, 50)
pygame.init()
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Шутан")
run = True

clock = pygame.time.Clock()


game_folder = os.path.dirname(__file__)
player_img1 = pygame.image.load(os.path.join(game_folder, 'player1.png')).convert_alpha()
enemy_img1 = pygame.image.load(os.path.join(game_folder, 'enemy1.png')).convert_alpha()
# player_img2 = pygame.image.load(os.path.join(game_folder, 'player2.png')).convert_alpha()
# enemy_img2 = pygame.image.load(os.path.join(game_folder, 'enemy2.png')).convert_alpha()
# player_img3 = pygame.image.load(os.path.join(game_folder, 'player3.png')).convert_alpha()
# enemy_img3 = pygame.image.load(os.path.join(game_folder, 'enemy3.png')).convert_alpha()
bullet_img = pygame.image.load(os.path.join(game_folder, 'Bullet.png')).convert_alpha()

player_img = player_img1
enemy_img = enemy_img1

all_sprites = pygame.sprite.Group()
dif = 1
def start_game(dif=1, player_skin=player_img1,enemy_skin=enemy_img1):
    global player_img
    global enemy_img
    global player
    global all_sprites
    global player_img1
    global enemy_img1
    player_img = pygame.image.load(os.path.join(game_folder, 'player' +str(dif)+'.png')).convert_alpha()
    enemy_img = pygame.image.load(os.path.join(game_folder, 'enemy'+str(dif)+'.png')).convert_alpha()
    all_sprites = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    for i in range(dif*2):
        all_sprites.add(Enemy(randint(0,100),randint(0,100)))

def save(score):


    conn = sqlite3.connect("leaders.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard(name CHAR NOT NULL, score INT NOT NULL)")
    cursor.execute("INSERT INTO leaderboard VALUES(?,?)",['player'+str(randint(0,1000)),score])

    conn.commit()

class Player(pygame.sprite.Sprite):
    def __init__(self):

        self.score = 0
        self.direction = 0
        self.HP = 100
        self.speed = 2
        self.attack_speed = 1
        self.dmg = 10
        self.money = 0

        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (110,110)
        self.rect.x = w//2
        self.rect.y = h//2
        self.size = self.image.get_size()
        self.normal_image = pygame.transform.scale(self.image, (int(40), int(40)))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = w
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.x > w:
                self.rect.x = 0
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = h
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            if self.rect.y > h:
                self.rect.y = 0
        if keys[pygame.K_ESCAPE]:
            global play
            play = 0

        self.rot_center()

    def shoot(self):
            dx = mouse_x - self.rect.x
            dy = mouse_y - self.rect.y
            if dx == 0:
                dx = 0.000001
            angle = -atan(dy / dx) / pi * 180
            if dx < 0 and dy < 0:
                angle += 180
            if dx < 0 and dy >= 0:
                angle += 180
            all_sprites.add(Bullet(self.rect.x, self.rect.y, angle))




    def rot_center(self):
        dx = mouse_x - self.rect.x
        dy = mouse_y - self.rect.y
        if dx == 0:
            dx = 0.000001
        angle = -atan(dy / dx) / pi * 180
        angle -= 90
        if dx < 0 and dy < 0:
            angle += 180
        if dx < 0 and dy > 0:
            angle += 180

        center = (self.rect.x, self.rect.y)
        rotated_image = pygame.transform.rotate(self.normal_image, angle)
        new_rect = rotated_image.get_rect(center=center)
        win.blit(rotated_image, new_rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):

        self.direction = 0
        self.HP = 100
        self.speed = 1
        self.attack_speed = 1
        self.dmg = 10

        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (w / 2, h / 2)
        self.rect.x = x
        self.rect.y = y
        self.size = self.image.get_size()
        self.normal_image = pygame.transform.scale(self.image, (int(40), int(40)))

    def update(self):
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = w
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
            if self.rect.x > w:
                self.rect.x = 0
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = h
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
            if self.rect.y > h:
                self.rect.y = 0

        if abs(self.rect.x - player.rect.x) < 40 and abs(self.rect.y - player.rect.y) < 40:
            global play
            play = 0

        self.rot_center()

    def rot_center(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        if dx == 0:
            dx = 0.000001
        angle = -atan(dy / dx) / pi * 180 - 90
        if dx < 0 and dy < 0:
            angle += 180
        if dx < 0 and dy >= 0:
            angle += 180

        center = (self.rect.x, self.rect.y)
        rotated_image = pygame.transform.rotate(self.normal_image, angle)
        new_rect = rotated_image.get_rect(center=center)
        win.blit(rotated_image, new_rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):

        pygame.sprite.Sprite.__init__(self)

        self.image = bullet_img
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (w / 2, h / 2)
        self.rect.x = x
        self.rect.y = y
        self.size = self.image.get_size()

        self.direction = dir
        self.speed = 10

    def update(self):
        rad = -self.direction / 180 * pi
        self.rect.x += cos(rad) * self.speed
        self.rect.y += sin(rad) * self.speed

        center = (self.rect.x, self.rect.y)
        rotated_image = pygame.transform.rotate(self.image, rad)
        new_rect = rotated_image.get_rect(center=center)
        win.blit(rotated_image, new_rect)

        if self.rect.x > w or self.rect.x < 0 or self.rect.y > h or self.rect.y < 0:
            all_sprites.remove(self)

        for i in all_sprites:
            if type(i) == Enemy:
                if abs(self.rect.x - i.rect.x) < 40 and abs(self.rect.y - i.rect.y) < 40:
                    all_sprites.remove(self)
                    all_sprites.remove(i)
                    all_sprites.add(Enemy(randint(0,100),randint(0,h)))
                    player.score += 1


class Button():
    def __init__(self, x, y,  color = (255,255,255), width=300, height=100, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


player = Player()


# enemy = Enemy(200,200)
# enemy1 = Enemy(500,500)



mouse_x = 100
mouse_y = 100

play = 0




start_b = Button(x=150,y=100,text='start')
dif1 = Button(x=150,y=210, width=90,text='1')
dif2 = Button(x=255,y=210, width=90,text='2')
dif3 = Button(x=360,y=210, width=90,text='3')
save_b = Button(x=150, y=320, text='save')
leaderboard = Button(x=150, y=430, text='leaders')

buttons = [start_b,dif1,dif2,dif3,save_b,leaderboard]

score = Button(0,0,text='Score: 0')



while run:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == 1024:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
        if event.type == 1025:
            if start_b.isOver(event.pos) and not play:
                play = 'Game'
                start_game(dif=dif)
            if dif1.isOver(event.pos) and not play:
                dif = 1
            if dif2.isOver(event.pos) and not play:
                dif = 2
            if dif3.isOver(event.pos) and not play:
                dif = 3
            if save_b.isOver(event.pos) and not play:
                save(player.score)
            if leaderboard.isOver(event.pos) and not play:
                play = 'leaderboard'

            player.shoot()





    win.fill(bgcolor)

    if play == 'Game':
        all_sprites.update()
        score.text = 'Score: ' + str(player.score)
        score.draw(win)
    elif play == 'leaderboard':

        conn = sqlite3.connect("leaders.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5')
        rows = cursor.fetchall()
        conn.commit()

        for i in range(len(rows)):
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(str(rows[i][0]) + ' ' + str(rows[i][1]), 1, (0, 0, 0))
            win.blit(text,
                     (150 + (300 / 2 - text.get_width() / 2), 100*(i+1) + (100 / 2 - text.get_height() / 2)))




    else:
        for b in buttons:
            b.draw(win)

    pygame.display.update()