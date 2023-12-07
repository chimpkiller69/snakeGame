import pygame
import random

#46lr
#33ud

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Определение констант игры
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
BLOCK_SIZE = 20
FONT_SIZE = 32
INITIAL_SNAKE_LENGTH = 3
SPEED = 8

# Инициализация Pygame
pygame.init()

# Создание класса игры
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.snake = Snake()
        self.apple = Apple()

    def run(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")

            self.screen.fill(BLACK)

            # Обновление змейки и проверка столкновений
            self.snake.update()
            if self.snake.check_collision():
                game_over = True

            # Проверка, съела ли змейка яблоко
            if self.snake.head_position() == self.apple.position:
                self.snake.grow()
                self.apple.move()

            # Отображение змейки и яблока
            self.snake.draw(self.screen)
            self.apple.draw(self.screen)

            # Отображение очков
            score_text = self.font.render("Score: {}".format(self.snake.score), True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width(), 0))

            # Обновление экрана и задержка
            pygame.display.update()
            self.clock.tick(SPEED)

        pygame.quit()

# Создание класса змейки
class Snake:
    def __init__(self):
        self.score = 0
        self.direction = "RIGHT"
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        for i in range(INITIAL_SNAKE_LENGTH - 1):
            x, y = self.positions[0]
            x -= BLOCK_SIZE
            self.positions.append((x, y))

    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def update(self):
        x, y = self.positions[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        # Добавление новой головы
        self.positions.insert(0, (x, y))

        # Удаление последнего сегмента, если змейка не выросла
        if len(self.positions) > self.score + INITIAL_SNAKE_LENGTH:
            self.positions.pop()

    def grow(self):
        self.score += 1

    def head_position(self):
        return self.positions[0]

    def check_collision(self):
        x, y = self.head_position()
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True
        for position in self.positions[1:]:
            if position == self.head_position():
                return True
        return False

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GREEN, rect)

# Создание класса яблока
class Apple:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        return (x, y)

    def move(self):
        self.position = self.random_position()

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, RED, rect)
        
if __name__ == '__main__':
    game = SnakeGame()
    game.run()
