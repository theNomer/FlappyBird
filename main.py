import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
FPS = 60
GRAVITY = 1
JUMP_HEIGHT = 15
PIPE_GAP = 200
PIPE_WIDTH = 50
PIPE_VELOCITY = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameObject:
    def __init__(self, x, y, width, height, color = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Bird(GameObject):
    def __init__(self, x, y, size, velocity):
        super().__init__(x, y, size, size)
        self.velocity = velocity

    def jump(self):
        self.velocity = -JUMP_HEIGHT

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

class Pipe(GameObject):
    def __init__(self, x, height, gap):
        upper_height = height
        lower_height = HEIGHT - height - gap
        super().__init__(x, 0, PIPE_WIDTH, upper_height, color = WHITE)
        self.lower_pipe = GameObject(x, HEIGHT - lower_height, PIPE_WIDTH, lower_height, color = WHITE)

    def move(self, velocity):
        self.rect.x -= velocity
        self.lower_pipe.rect.x -= velocity

    def draw(self, screen):
        super().draw(screen)
        self.lower_pipe.draw(screen)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird = Bird(WIDTH // 4, HEIGHT // 2, 30, 0)
        self.pipes = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

    def create_pipe(self):
        pipe_height = random.randint(HEIGHT // 6, HEIGHT - PIPE_GAP - HEIGHT // 6)
        return Pipe(WIDTH, pipe_height, PIPE_GAP)

    def collision_check(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect) or self.bird.rect.colliderect(pipe.lower_pipe.rect) or self.bird.rect.y > HEIGHT:
                self.quit_game()

    def draw_objects(self):
        self.screen.fill(BLACK)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_events()

            self.bird.update()

            if not self.pipes or self.pipes[-1].rect.x < WIDTH - WIDTH // 2:
                self.pipes.append(self.create_pipe())

            for pipe in self.pipes:
                pipe.move(PIPE_VELOCITY)

            self.pipes = [pipe for pipe in self.pipes if pipe.rect.x > -PIPE_WIDTH]

            self.collision_check()

            self.draw_objects()

            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
