import pygame
import sys
import random
import time

FPS = 8
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
LIGHT_GREEN = (0, 160, 0)
WHITE = (255, 255, 255)
WIDTH = 1090
HEIGHT = 790
SCORE = 0
FON = pygame.image.load('fon.jpg')
APPLE = pygame.image.load('apple.png')
GOLD_APPLE = pygame.image.load('gold_apple.png')
HEAD_SNAKE = pygame.image.load('snake_head.png')
BODY_SNAKE = pygame.image.load('snake_body.png')
start_spawn_food = False
start_game = 0
luck = 0
screen = pygame.display.set_mode((
    WIDTH, HEIGHT))
POLE = []
for i in range(18):
    for j in range(1, 13):
        x = i * 50 + (i + 1) * 10
        y = j * 50 + (j + 1) * 10
        POLE.append([x, y])


class Menu():
    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        pygame.init()
        screen.blit(FON, (0, 0))
        intro_text = ["Змейка!", "",
                      "Правила игры:",
                      "Ешь яблоки и расти!",
                      "Золотое яблоко - +100 очков",
                      "Красное яблоко - +20 очков",
                      "Чтобы начать нажмите:",
                      "любую клавишу!"]
        screen.blit(screen, (0, 0))
        font = pygame.font.Font('UpheavalPro.ttf', 40)
        text_coord = 70
        for line in intro_text:
            string_rendered = font.render(line, 5, pygame.Color(BLACK))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            intro_rect.midtop = (500, text_coord)
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    return
            pygame.display.flip()


class Game():
    def win(self):
        go_font = pygame.font.Font('UpheavalPro.ttf', 50)
        go_surf = go_font.render(f'WIN! SCORE: {SCORE}', True, RED)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (545, 10)
        screen.blit(go_surf, go_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def game_over(self):
        go_font = pygame.font.Font('UpheavalPro.ttf', 50)
        go_surf = go_font.render(f'Game over! SCORE: {SCORE}', True, RED)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (545, 10)
        screen.blit(go_surf, go_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
        return change_to

    def generation_pole(self):
        screen.fill(BLACK)
        for i in range(18):
            for j in range(1, 12):
                x = i * 50 + (i + 1) * 10
                y = j * 50 + (j + 1) * 10
                pygame.draw.rect(screen, GREEN, (x, y, 50, 50))


class Food():
    def __init__(self):
        global start_spawn_food, luck
        if start_spawn_food is False:
            self.food_pos = [490, 370]
            self.food_pos_gold = [-100, -100]
            start_spawn_food = True
        else:
            a = random.choice(POLE)
            self.food_pos = [a[0], a[1]]
        b = random.randint(1, 10)
        if b == 5:
            luck = 1
            a = random.choice(POLE)
            self.food_pos_gold = [a[0], a[1]]

    def draw_food(self):
        global luck
        screen.blit(APPLE, (self.food_pos[0], self.food_pos[1]))
        if luck == 1:
            screen.blit(GOLD_APPLE, (self.food_pos_gold[0], self.food_pos_gold[1]))


class Snake():
    def __init__(self):
        self.snake_head_pos = [130, 370]
        self.snake_body = [[10, 370], [70, 370], [130, 370]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        global HEAD_SNAKE
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 60
            HEAD_SNAKE = pygame.image.load('snake_head.png')
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 60
            HEAD_SNAKE = pygame.image.load('snake_head_left.png')
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 60
            HEAD_SNAKE = pygame.image.load('snake_head_verh.png')
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 60
            HEAD_SNAKE = pygame.image.load('snake_head_vniz.png')

    def snake_body_mechanism(self, food_pos, food_pos_gold):
        global SCORE, luck
        b = random.randint(1, 10)
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            if self.snake_body == POLE:
                game.win()
            SCORE += 20
            if b == 5:
                luck = 1
                a = random.choice(POLE)
                food_pos_gold = [a[0], a[1]]
                if a in self.snake_body:
                    while a in self.snake_body:
                        a = random.choice(POLE)
                        food_pos_gold = [a[0], a[1]]
            a = random.choice(POLE)
            food_pos = [a[0], a[1]]
            if a in self.snake_body:
                while a in self.snake_body:
                    a = random.choice(POLE)
                    food_pos = [a[0], a[1]]
        elif (self.snake_head_pos[0] == food_pos_gold[0] and
              self.snake_head_pos[1] == food_pos_gold[1] and luck == 1):
            if self.snake_body == POLE:
                game.win()
            SCORE += 100
            luck = 0
        else:
            self.snake_body.pop()
        screen.fill(BLACK)
        for i in range(18):
            for j in range(1, 13):
                x = i * 50 + (i + 1) * 10
                y = j * 50 + (j + 1) * 10
                pygame.draw.rect(screen, GREEN, (x, y, 50, 50))
        pygame.draw.rect(screen, GREEN, (0, 0, 1220, 60))
        return food_pos, food_pos_gold

    def draw_snake(self):
        global start_game
        if start_game > 1:
            i = 0
            for pos in self.snake_body:
                if i == 0:
                    screen.blit(HEAD_SNAKE, (pos[0], pos[1]))
                    i += 1
                else:
                    screen.blit(BODY_SNAKE, (pos[0], pos[1]))
        start_game += 1

    def check_for_boundaries(self):
        pygame.init()
        if any((
                self.snake_head_pos[0] > WIDTH - 60
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > HEIGHT - 60
                or self.snake_head_pos[1] < 70
        )):
            game.game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game.game_over()


snake = Snake()
food = Food()
game = Game()
menu = Menu()
menu.start_screen()
pygame.display.set_caption("Змейка!")
fps_controller = pygame.time.Clock()
while True:
    snake.change_to = game.event_loop(snake.change_to)
    snake.validate_direction_and_change()
    snake.change_head_position()
    food.food_pos, food.food_pos_gold = snake.snake_body_mechanism(food.food_pos, food.food_pos_gold)
    snake.draw_snake()
    food.draw_food()
    snake.check_for_boundaries()
    pygame.init()
    font = pygame.font.Font('UpheavalPro.ttf', 50)
    text = font.render(f"SCORE: {SCORE}", True, (0, 0, 0))
    screen.blit(text, (0, 0))
    pygame.display.flip()
    fps_controller.tick(FPS)
