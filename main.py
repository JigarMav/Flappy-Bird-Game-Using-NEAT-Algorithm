import pygame
import neat
import os
import time
import random

WIN_HEIGHT = 800
WIN_WIDTH = 600
BIRD_IMAGES  = []
for i in range(1,4):
    BIRD_IMAGES.append(pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(i) + str(".png")))))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
# print(BIRD_IMAGES)

class Bird:
    IMGS = BIRD_IMAGES
    # MAX BIRD TILT IS 25 degrees.
    MAX_ROTATION = 25
    # Rotation on each frame
    ROT_VELOCITY = 20
    # animation of our bird flapp.
    ANIMATION_TIME = 5

    def __int__(self,x,y):
        # intitial co-ordinates of our bird.
        self.x = x
        self.y = y
        # set initial tilt to 0
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        # starting height
        self.height = self.y
        # image count for animation
        self.img_count =0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        # height from where we need to jump
        self.height = self.y



