from pydoc import plain
from turtle import right
import pygame
from pygame.locals import *
import random

clock = pygame.time.Clock()

Colors ={
    "white": (255,255,255),
    "black": (0,0,0),
    "red": (255,0,0),
    "blue": (0,0,255),
    "random": (random.randint(0, 255),random.randint(0, 255),
    random.randint(0, 255))
}


direction = 1

width = 600
height = 600


class Ball:
    def __init__(self, centerX = None, centerY = None, direction = None, color = None, radius = None, speed = None):
        self.centerX = random.randint(0, 600)
        self.centerY = random.randint(0, 600)
        self.color = Colors["red"]
        self.velocityX = 2
        self.velocityY = 2
        self.radius = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.centerX, self.centerY), self.radius)

    def update(self, screen):

        if self.centerX <= 20 or self.centerY <= 20:
            self.velocityX = random.randint(1,5)
            self.velocityY = random.randint(1,5)
        if self.centerX >= 580 or self.centerY >= 580:
            self.velocityX -= random.randint(1,5)
            self.velocityY -= random.randint(1,5)

        self.centerX += self.velocityX
        self.centerY += self.velocityY


class Player(Ball):
    def __init__(self, centerX=None, centerY=None, direction=None, color=None, radius=None):
        super().__init__(self,radius)
        self.centerX = round(width/2)
        self.centerY = round(height/2)
        self.color = Colors["white"]
    
    def update(self, screen, ball = Ball()):
        v1 = pygame.math.Vector2(self.centerX, self.centerY)
        v2 = pygame.math.Vector2(ball.centerX, ball.centerY)
        
        hit = 1
        if v1.distance_to(v2) <= self.radius + ball.radius - 2: 

            nv = v2 - v1
            m1 = pygame.math.Vector2(self.velocityX, self.velocityY).reflect(nv)
            m2 = pygame.math.Vector2(ball.velocityX, ball.velocityY).reflect(nv)

            self.centerX += round(m1.x)
            self.centerY += round(m1.y)

            ball.centerX += round(m2.x)
            ball.centerY += round(m2.y)

            print("Hit")
        

def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particles")

    pygame.init()
    clock = pygame.time.Clock()

    balls = [Ball() for _ in range(2)]
    playa = Player()
    
    timer = 1
    running = True
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        screen.fill(Colors["black"])

        playa.draw(screen=screen)

        for ball in balls:
            ball.draw(screen =screen)
            playa.update(screen=screen, ball=ball)
            ball.update(screen= screen)

        clock.tick(60)
        pygame.display.update()
        
        timer += 1
        if timer %750 == 0:
            balls.append(Ball())

if __name__ == "__main__":
    main()
