import socket
import pickle
import pygame
import numpy
import time
from player import Player

pygame.init()

window = pygame.display.set_mode((1000,400))
pygame.display.set_caption("Koldahogg")

Player1 = Player(50, 250, 72, 115, 1)
Player2 = Player(950-72, 250, 72, 115, -1)

host = 'localhost'
port = 8888

def draw(self, window, count):
        if not (self.dead) and self.moves:
                if self.f == 1:
                        window.blit(cropped[count % 7 + 1], (self.x, self.y))
                else:
                        window.blit(pygame.transform.flip(cropped[count % 7 + 1], True, False), (self.x, self.y))
        elif not (self.moves):
                if self.f == 1:
                        window.blit(cropped[0], (self.x, self.y))
                else:
                        window.blit(pygame.transform.flip(cropped[0], True, False), (self.x, self.y))

        else:
                window.blit(cropped[8], (self.x, self.y))

        self.moves = False

Warrior = pygame.image.load('warrior.jpg')
cropped = [pygame.Surface((72,115)), pygame.Surface((72,115)), pygame.Surface((72,115)),pygame.Surface((72,115)),pygame.Surface((72,115)),pygame.Surface((72,115)),pygame.Surface((72,115)),pygame.Surface((72,115)),pygame.Surface((72,115)), pygame.Surface((72,115))]
cropped[0].blit(Warrior,  (0,0), (904, 212, 72,115))
for i in range (1,8):
    cropped[i].blit(Warrior, (0,0), (220+72*i, 490, 72, 115))
cropped[8].blit(Warrior,  (0,0), (904+4*72+10, 212, 72,115))

Win = pygame.image.load('win.jpg')
clock = pygame.time.Clock()
animCount = 0
run = True
fps = 30

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected")
        while run :
                clock.tick(fps)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                run = False

                keys = pygame.key.get_pressed()

                flags = [keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_RETURN], keys[pygame.K_UP], keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE], keys[pygame.K_w]]

                s.sendall(bytes(flags))

                news = pickle.loads(s.recv(2048))
                print(news)
                Player1.set_status(news[0])
                Player2.set_status(news[1])
                window.fill((249, 245, 233))

                if animCount + 1 >= fps:
                        animCount = 0

                if not (Player1.is_dead()):
                        draw(Player1, window, animCount)
                else:
                        window.blit(Win, (700, 25))
                        window.blit(pygame.transform.rotate(cropped[8], 90), (Player1.getx(), Player1.gety() + 150))

                if not (Player2.is_dead()):
                        draw(Player2, window, animCount)
                else:
                        window.blit(Win, (25, 25))
                        window.blit(pygame.transform.rotate(cropped[8], 270), (Player2.getx(), Player2.gety() + 150))


                animCount += 1

                pygame.display.update()

pygame.quit()
s.close()