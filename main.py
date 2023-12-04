import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
FPS = 60
GRAVITY = 1
JUMP_HEIGHT = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

bird_size = 30
bird_x = WIDTH // 4
bird_y = HEIGHT // 2
bird_velocity = 0

pipe_width = 50
pipe_height = 300
pipe_gap = 200
pipe_velocity = 5
pipes = []

clock = pygame.time.Clock()

def draw_bird(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, bird_size, bird_size])

def draw_pipe(x, height):
    pygame.draw.rect(screen, WHITE, [x, 0, pipe_width, height])
    pygame.draw.rect(screen, WHITE, [x, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -JUMP_HEIGHT

    bird_velocity += GRAVITY
    bird_y += bird_velocity

    if len(pipes) == 0 or pipes[-1][0] < WIDTH - WIDTH // 2:
        pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
        pipes.append([WIDTH, pipe_height])

    for pipe in pipes:
        pipe[0] -= pipe_velocity

    pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]

    for pipe in pipes:
        if (
            bird_x < pipe[0] + pipe_width
            and bird_x + bird_size > pipe[0]
            and (bird_y < pipe[1] or bird_y + bird_size > pipe[1] + pipe_gap)
        ):
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    for pipe in pipes:
        draw_pipe(pipe[0], pipe[1])

    draw_bird(bird_x, bird_y)

    pygame.display.flip()

    clock.tick(FPS)
