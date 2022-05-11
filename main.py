from json.encoder import ESCAPE
from pydoc import plain
from turtle import right
import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()

Colors ={
    "white": (255,255,255),
    "black": (0,0,0),
    "red": (255,0,0),
    "blue": (0,0,255),
    "yellow": (255,255,102),
    "random": (random.randint(0, 255),random.randint(0, 255),
    random.randint(0, 255))
}


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsams", 35)

direction = 1

width = 600
height = 600

def score(scr, screen):
    value = score_font.render("Score "+ str(scr), True, Colors["yellow"])
    screen.blit(value, [0, 0])


class Ball:
    def __init__(self, centerX = None, centerY = None, direction = None, color = None, radius = None, speed = None):
        self.centerX = random.randint(0, 600)
        self.centerY = random.randint(0, 600)
        self.color = Colors["random"]
        self.velocityX = 1
        self.velocityY = 1
        self.radius = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.centerX, self.centerY), self.radius)

    def update(self, screen, rng, mmin):

        if self.centerX <= 20 or self.centerY <= 20:
            self.velocityX = random.randint(mmin,rng)
            self.velocityY = random.randint(mmin,rng)
        if self.centerX >= 580 or self.centerY >= 580:
            self.velocityX -= random.randint(mmin,rng)
            self.velocityY -= random.randint(mmin,rng)

        self.centerX += self.velocityX
        self.centerY += self.velocityY


class Player(Ball):
    def __init__(self, centerX=None, centerY=None, direction=None, color=None, radius=None):
        super().__init__(self,radius)
        self.centerX = round(width/2)
        self.centerY = round(height/2)
        self.color = Colors["red"]
    
    def update(self, screen, ball = Ball()):
        v1 = pygame.math.Vector2(self.centerX, self.centerY)
        v2 = pygame.math.Vector2(ball.centerX, ball.centerY)

        if v1.distance_to(v2) <= self.radius + ball.radius - 2: 

            nv = v2 - v1
            m1 = pygame.math.Vector2(self.velocityX, self.velocityY).reflect(nv)
            m2 = pygame.math.Vector2(ball.velocityX, ball.velocityY).reflect(nv)

            self.centerX += round(m1.x)
            self.centerY += round(m1.y)

            ball.centerX += round(m2.x)
            ball.centerY += round(m2.y)

            print("Hit")

            return "hit"
        
        return True
        

        

def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particles")

    clock = pygame.time.Clock()

    balls = [Ball() for _ in range(2)]
    playa = Player()
    
    timer = 1
    rng = 5
    mmin = 1
    vel = 1

    
    running = True
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_q:
                    running = False
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    playa.centerX -= 10
                elif event.key == pygame.K_RIGHT:
                    playa.centerX += 10
                elif event.key == pygame.K_UP:
                    playa.centerY -= 10
                elif event.key == pygame.K_DOWN:
                    playa.centerY += 10
        
        mx, my  = pygame.mouse.get_pos()
        playa.centerX = mx
        playa.centerY = my
        
        screen.fill(Colors["black"])

        playa.draw(screen=screen)


        for ball in balls:
            if timer%365 == 0:
                rng += 1
                mmin += 1
                for b in balls:
                    b.velocityX += vel
                    b.velocityY += vel
            ball.draw(screen =screen)

            hit = playa.update(screen=screen, ball=ball)
            if hit == "hit":
                running = False
            ball.update(screen= screen, rng= rng, mmin=mmin)

        clock.tick(60)
        score(timer, screen=screen)
        pygame.display.update()
        
        timer += 1
        if timer %750 == 0:
            balls.append(Ball())

if __name__ == "__main__":
    main()
