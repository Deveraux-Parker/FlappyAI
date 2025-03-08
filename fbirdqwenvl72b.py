import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 30

# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_COLORS = [(0, 0, 0), (50, 50, 50), (100, 100, 100)]
LAND_COLORS = [(85, 65, 40), (255, 215, 0)]
PIPE_COLORS = [(0, 100, 0), (139, 69, 19), (105, 105, 105)]

# Game variables
gravity = 0.5
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Background
background_color = LIGHT_BLUE

# Land
land_y_pos = SCREEN_HEIGHT - 100
land_color = random.choice(LAND_COLORS)

# Bird
bird_shape = random.choice(['square', 'circle', 'triangle'])
bird_color = random.choice(DARK_COLORS)
bird_x_pos = 50
bird_y_pos = SCREEN_HEIGHT // 2

def draw_bird():
    if bird_shape == 'square':
        pygame.draw.rect(screen, bird_color, (bird_x_pos, bird_y_pos, 50, 50))
    elif bird_shape == 'circle':
        pygame.draw.circle(screen, bird_color, (bird_x_pos + 25, bird_y_pos + 25), 25)
    elif bird_shape == 'triangle':
        pygame.draw.polygon(screen, bird_color, [(bird_x_pos, bird_y_pos + 25), (bird_x_pos + 25, bird_y_pos), (bird_x_pos + 50, bird_y_pos + 25)])

# Pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

def create_pipe():
    pipe_color = random.choice(PIPE_COLORS)
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos, 70, SCREEN_HEIGHT - random_pipe_pos)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, 70, SCREEN_HEIGHT - random_pipe_pos - 150)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            pygame.draw.rect(screen, pipe_color, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, pipe)

# Score
font = pygame.font.Font(None, 36)

def show_score(score):
    score_surface = font.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH - 50, 50))
    screen.blit(score_surface, score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_y_pos = SCREEN_HEIGHT // 2
                bird_movement = 0
                score = 0
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.fill(background_color)

    if game_active:
        # Bird
        bird_movement += gravity
        bird_y_pos += bird_movement
        draw_bird()

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        show_score(int(score))

        # Collision
        for pipe in pipe_list:
            if bird_x_pos + 50 > pipe.left and bird_x_pos < pipe.right:
                if bird_y_pos < pipe.top or bird_y_pos + 50 > pipe.bottom:
                    game_active = False
                    high_score = update_score(int(score), high_score)
    else:
        game_over_surface = font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_surface, game_over_rect)

        high_score_surface = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_score_surface, high_score_rect)

    # Land
    pygame.draw.rect(screen, land_color, (0, land_y_pos, SCREEN_WIDTH, 100))

    pygame.display.update()
    clock.tick(FPS)