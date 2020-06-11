import pygame
import neat
import os
import time
import random

WIN_HEIGHT = 800
WIN_WIDTH = 500
# BIRD_IMAGES = []
# for i in range(1, 4):
#     BIRD_IMAGES.append(pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird" + str(i) + str(".png")))))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]

# print(BIRD_IMAGES)

class Bird:
    IMGS = BIRD_IMAGES
    # MAX BIRD TILT IS 25 degrees.
    MAX_ROTATION = 25
    # Rotation on each frame
    ROT_VELOCITY = 20
    # animation of our bird flapp.
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        # intitial co-ordinates of our bird.
        self.x = x
        self.y = y
        # set initial tilt to 0
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        # starting height
        self.height = self.y
        # image count for animation used for flappy birds. counts while loop iteration.
        self.img_count = 0
        self.img = self.IMGS[0]


    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        # height from where we need to jump
        self.height = self.y

    def move(self):
        # no of moves since the last jump.
        self.tick_count += 1

        # Displacement. No of places we move up or down.
        # tick_count is used as time. This will tell when to move down after moving to top.

        d = self.vel * self.tick_count + 1.5 * (self.tick_count) ** 2

        #       setting terminal velocity types so that we dont move waaay to up or down.
        #         if we move down or up 16 px we bottleneck it for no more acceleration
        if d >= 16:
            d = 16

        self.y = self.y + d

        # adjustment for tilting. IF our d<0 (we move UP ) or if we are above the y point where we started.
        # we keep the bird up.
        # 50 so that we come to level just before the horizontal plane.
        if(d<0 or self.y<self.height + 50):
            # check for maximum tilt while going upwards. 25 in our case.
            if(self.tilt<self.MAX_ROTATION):
                self.tilt = self.MAX_ROTATION
            else:
                # we go all the way down 90 when we move down
                if(self.tilt>-90):
                    self.tilt-=self.ROT_VELOCITY


    def draw(self,win):
        self.img_count+=1

        # Update bird image based on Animation time that we have set.
        #  Goes from 0 - 1- 2 - 1 -0.

        if(self.img_count<self.ANIMATION_TIME):
            self.img = self.IMGS[0]
        elif (self.img_count<self.ANIMATION_TIME*2):
            self.img = self.IMGS[1]
        elif (self.img_count<self.ANIMATION_TIME*3):
            self.img = self.IMGS[2]
        elif(self.img_count<self.ANIMATION_TIME*4):
            self.img = self.IMGS[1]
        elif (self.img_count < self.ANIMATION_TIME * 4 +1):
            self.img = self.IMGS[0]
        # reset after one cycle.
            self.img_count = 0

        # rotates the image about the top left hand corner .
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # modification so that it rotates about its center.
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y )).center)
        # draw the rotated image.
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)



class Pipe:

    # minimum gap between the pipes
    GAP = 200
    VEL = 5

    def __int__(self,x):
        self.x = x
        # height of our pipe
        self.height = 0

        # Top pipe which is inverted. Its postion.
        self.top = 0
        # Y of the bottom pipe.
        self.bottom = 0
        # invert the top pipe.
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        # Required for the AI training part.
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        # TOP position of top pipe.
        self.top = self.height - self.PIPE_TOP.get_height()
        # Y coordinate of the bottom pipe.
        self.bottom = self.height + self.GAP
    def move(self):
        self.x-=self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self, bird):
        '''
        uses the mask functionality of pygame to check if pixels overlap.
        :param bird: Bird object
        :return: Bool
        '''
        # bird mask
        bird_mask = bird.get_mask()
        # masks of top pipe and bottom pipe.
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # distance between bird and pipes.
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # if they collide , point of collision or returns None.
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        # if any of them collide , return true;
        if b_point or t_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        # x1 is x coordinate of 1st image . x2 is x of 2nd coordinate.
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        # images are moved at VEL speed.
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # one image after another.
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        # draw 2 bases
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# Draw a window for the game.
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird: Bird = Bird(200,200)
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    run = True
    while(run):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run = False
        draw_window(win, bird)

    pygame.quit()
    quit()



if __name__ == '__main__':
    main()