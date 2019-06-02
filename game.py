import pickle
import pygame
from PIL import Image
import socket
from player import Player

pygame.init()

window = pygame.display.set_mode((1000,400))
pygame.display.set_caption("Koldahogg")

Player1 = Player(50, 250, 72, 115, 1)
Player2 = Player(950-72, 250, 72, 115, -1)

isJump = [False, False]
jumpCount = [10, 10]
fps = 30
speed = 8
time = 100*fps
run = True

host = 'localhost'
port = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(2)
    conn1, addr1 = s.accept()
    conn2, addr2 = s.accept()
    with conn1:
        with conn2:

            print("Connecter by ", addr1, " and ", addr2)

            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                keys_a = conn1.recv(1024)
                keys1 = tuple(keys_a)
                keys_b = conn2.recv(1024)
                keys2 = tuple(keys_b)

                if not (Player1.is_dead()):
                        jumpCount[0], isJump[0] = Player1.analise_keys_short(Player2, keys1, speed, jumpCount[0], isJump[0], 1)
                else:
                        time -= fps

                if not (Player2.is_dead()):
                        jumpCount[1], isJump[1] = Player2.analise_keys_short(Player1, keys2, speed, jumpCount[1], isJump[1], 2)
                else:
                        time -= fps

                status = [Player1.get_status(),Player2.get_status()]
                print(status)

                conn1.sendall(pickle.dumps(status))

                conn2.sendall(pickle.dumps(status))

                if time == 0:
                    break
                #pygame.display.update()

pygame.quit()
s.close()
