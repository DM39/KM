import pygame
class Player():
    def __init__(self, x, y, h, w, f, dead=False, moves = False):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.f = f
        self.dead = dead
        self.moves = moves
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def get_square(self):
        return self.x,self.y
    def set_position(self,x,y):
        self.x = x
        self.y = y
    def facing(self, f):
        self.f = f
    def move(self, speed):
        self.moves = True
        self.x += self.f*speed
    def jump(self, count, isit):
        self.moves = False
        if count >= -10:
            if count < 0:
                self.y += (count ** 2) / 2
            else:
                self.y -= (count ** 2) / 2
            count -= 1
        else:
            isit = False
            count = 10

        return count, isit
    def is_dead(self):
        return self.dead
    def die(self):
        self.dead = True
    def attack (self, Player_x):
        if Player_x.gety() < self.y+30:
            if Player_x.getx() < self.x + self.h and Player_x.getx() > self.x and self.f == 1: Player_x.die()
            elif Player_x.getx() > self.x - self.h and Player_x.getx() < self.x and self.f == -1: Player_x.die()
    def analise_keys(self, enemy, keys, speed, count, jump, control):

        if control==1:
            left, right, attack, up = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_UP
        if control==2:
            left, right, attack, up = pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.K_w

        if keys[left]:
            self.facing(-1)
            self.move(speed)

        elif keys[right]:
            self.facing(1)
            self.move(speed)

        if keys[attack]:
            self.attack(enemy)

        if jump == False:
            if keys[up] and count == 10:
                jump = True

        if jump == True:
            count, jump = self.jump(count, jump)

        return count, jump
    def analise_keys_short(self, enemy, keys, speed, count, jump, control):

        if control==1:
            left, right, attack, up = 0,1,2,3,
        if control==2:
            left, right, attack, up = 4,5,6,7

        if keys[left]:
            self.facing(-1)
            self.move(speed)

        elif keys[right]:
            self.facing(1)
            self.move(speed)
        else:
            self.moves = False

        if keys[attack]:
            self.attack(enemy)

        if jump == False:
            if keys[up] and count == 10:
                jump = True

        if jump == True:
            count, jump = self.jump(count, jump)

        return count, jump
    def get_status(self):
        d = int(self.dead)
        m = int(self.moves)
        return [self.x,self.y,self.h,self.w,self.f,d,m]
    def set_status(self, status):
        self.x = status[0]
        self.y = status[1]
        self.h = status[2]
        self.w = status[3]
        self.f = status[4]
        if status[5]>0: self.dead = True
        else: self.dead = False
        if status[6]>0: self.moves = True
        else: self.moves = False