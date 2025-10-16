import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        try:
            self.font = pygame.font.SysFont("Arial", 30)
        except pygame.error:
            self.font = pygame.font.Font(None, 30)
        self.game_over = False
        self.game_started = False
        self.score_selection = True
        self.winning_score = None

        pygame.mixer.init()
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        except pygame.error:
            print("Couldn't load sound files. Make sure you have paddle_hit.wav, wall_bounce.wav, and score.wav in the sounds directory.")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.game_started = False
        self.score_selection = False
        self.ball.reset()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.game_over:
            if keys[pygame.K_3]:
                self.winning_score = 3
                self.reset_game()
            elif keys[pygame.K_5]:
                self.winning_score = 5
                self.reset_game()
            elif keys[pygame.K_7]:
                self.winning_score = 7
                self.reset_game()
            elif keys[pygame.K_ESCAPE]:
                return False
        elif self.score_selection:
            if keys[pygame.K_3]:
                self.winning_score = 3
                self.score_selection = False
            if keys[pygame.K_5]:
                self.winning_score = 5
                self.score_selection = False
            if keys[pygame.K_7]:
                self.winning_score = 7
                self.score_selection = False

        if not self.game_started and not self.score_selection and keys[pygame.K_SPACE]:
            self.game_started = True

        if self.game_started and not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        return True

    def update(self):
        if self.game_started and not self.game_over:
            wall_hit = self.ball.move()
            if wall_hit and self.wall_bounce_sound:
                self.wall_bounce_sound.play()

            paddle_hit = self.ball.check_collision(self.player, self.ai)
            if paddle_hit and self.paddle_hit_sound:
                self.paddle_hit_sound.play()

            if self.ball.x <= 0:
                self.ai_score += 1
                if self.score_sound:
                    self.score_sound.play()
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                if self.score_sound:
                    self.score_sound.play()
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)

            if self.winning_score and (self.player_score >= self.winning_score or self.ai_score >= self.winning_score):
                self.game_over = True

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        if self.score_selection:
            score_text = self.font.render("Select Winning Score", True, WHITE)
            option3_text = self.font.render("Press 3 for 3 points", True, WHITE)
            option5_text = self.font.render("Press 5 for 5 points", True, WHITE)
            option7_text = self.font.render("Press 7 for 7 points", True, WHITE)
            screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2 - score_text.get_height()//2 - 60))
            screen.blit(option3_text, (self.width//2 - option3_text.get_width()//2, self.height//2 - option3_text.get_height()//2 - 20))
            screen.blit(option5_text, (self.width//2 - option5_text.get_width()//2, self.height//2 - option5_text.get_height()//2 + 20))
            screen.blit(option7_text, (self.width//2 - option7_text.get_width()//2, self.height//2 - option7_text.get_height()//2 + 60))

        if not self.game_started and not self.score_selection:
            start_text = self.font.render("Press Space to Start", True, WHITE)
            screen.blit(start_text, (self.width//2 - start_text.get_width()//2, self.height//2 - start_text.get_height()//2))

        if self.game_over:
            end_text = self.font.render("Game Over", True, WHITE)
            winner = "Player" if self.player_score >= self.winning_score else "AI"
            win_text = self.font.render(f"{winner} Wins!", True, WHITE)
            screen.blit(end_text, (self.width//2 - end_text.get_width()//2, self.height//2 - end_text.get_height()//2 - 20))
            screen.blit(win_text, (self.width//2 - win_text.get_width()//2, self.height//2 + win_text.get_height()//2 - 20))

            replay_text = self.font.render("Play Again?", True, WHITE)
            option3_text = self.font.render("Press 3 for Best of 3", True, WHITE)
            option5_text = self.font.render("Press 5 for Best of 5", True, WHITE)
            option7_text = self.font.render("Press 7 for Best of 7", True, WHITE)
            exit_text = self.font.render("Press ESC to Exit", True, WHITE)
            screen.blit(replay_text, (self.width//2 - replay_text.get_width()//2, self.height//2 + 40))
            screen.blit(option3_text, (self.width//2 - option3_text.get_width()//2, self.height//2 + 80))
            screen.blit(option5_text, (self.width//2 - option5_text.get_width()//2, self.height//2 + 120))
            screen.blit(option7_text, (self.width//2 - option7_text.get_width()//2, self.height//2 + 160))
            screen.blit(exit_text, (self.width//2 - exit_text.get_width()//2, self.height//2 + 200))
