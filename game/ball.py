import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = float(x)
        self.y = float(y)
        self.prev_x = float(x)
        self.prev_y = float(y)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = float(random.choice([-5, 5]))
        self.velocity_y = float(random.choice([-3, 3]))

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.velocity_x
        self.y += self.velocity_y

        wall_hit = False
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_hit = True
        return wall_hit

    def check_collision(self, player, ai):
        movement_rect = self.rect().union(pygame.Rect(int(self.prev_x), int(self.prev_y), self.width, self.height))
        paddle_hit = False

        if movement_rect.colliderect(player.rect()):
            if self.velocity_x < 0:
                self.velocity_x *= -1
                self.x = player.x + player.width
                paddle_hit = True
        
        if movement_rect.colliderect(ai.rect()):
            if self.velocity_x > 0:
                self.velocity_x *= -1
                self.x = ai.x - self.width
                paddle_hit = True
        
        return paddle_hit

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = float(random.choice([-3, -2, 2, 3]))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)