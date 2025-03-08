import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BG_COLOR = (135, 206, 235)  # Light blue
LAND_COLORS = [(139, 69, 19), (255, 215, 0)]  # Dark brown, yellow
PIPE_COLORS = [(0, 100, 0), (165, 42, 42), (105, 105, 105)]  # Dark green, light brown, dark gray
BIRD_COLORS = [(0, 0, 0), (105, 105, 105), (50, 50, 50)]  # Dark colors

# Bird shapes
BIRD_SHAPES = ['square', 'circle', 'triangle']

# Game variables
bird_x = 50
bird_y = 300
bird_shape = random.choice(BIRD_SHAPES)
bird_color = random.choice(BIRD_COLORS)
bird_velocity = 0
gravity = 0.5
jump_strength = -10
score = 0
best_score = 0
land_height = 100
pipe_gap = 150
pipe_width = 70
pipe_velocity = 3
pipes = []

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Fonts
font = pygame.font.Font(None, 36)

# Helper functions
def draw_bird():
    if bird_shape == 'square':
        pygame.draw.rect(screen, bird_color, (bird_x, bird_y, 20, 20))
    elif bird_shape == 'circle':
        pygame.draw.circle(screen, bird_color, (bird_x + 10, bird_y + 10), 10)
    elif bird_shape == 'triangle':
        pygame.draw.polygon(screen, bird_color, [(bird_x, bird_y + 20), (bird_x + 20, bird_y + 20), (bird_x + 10, bird_y)])

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, pipe[2], (pipe[0], pipe[1], pipe_width, pipe[3]))
        pygame.draw.rect(screen, pipe[2], (pipe[0], pipe[1] + pipe[3] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe[1] - pipe[3] - pipe_gap))

def move_pipes():
    for pipe in pipes:
        pipe[0] -= pipe_velocity
    pipes[:] = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

def add_pipe():
    pipe_height = random.randint(100, 400)
    pipe_color = random.choice(PIPE_COLORS)
    pipes.append([SCREEN_WIDTH, 0, pipe_color, pipe_height])

def check_collision():
    for pipe in pipes:
        if (bird_x + 20 > pipe[0] and bird_x < pipe[0] + pipe_width and
            (bird_y < pipe[1] + pipe[3] or bird_y + 20 > pipe[1] + pipe[3] + pipe_gap)):
            return True
    if bird_y + 20 >= SCREEN_HEIGHT - land_height:
        return True
    return False

def reset_game():
    global bird_y, bird_velocity, score, bird_shape, bird_color
    bird_y = 300
    bird_velocity = 0
    score = 0
    bird_shape = random.choice(BIRD_SHAPES)
    bird_color = random.choice(BIRD_COLORS)
    pipes.clear()
    add_pipe()

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                    game_over = False
                bird_velocity = jump_strength
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipes
        move_pipes()
        if pipes and pipes[-1][0] < SCREEN_WIDTH - 200:
            add_pipe()
        if pipes and pipes[0][0] < -pipe_width:
            pipes.pop(0)
            score += 1

        # Check for collisions
        if check_collision():
            game_over = True
            if score > best_score:
                best_score = score

    # Draw everything
    screen.fill(BG_COLOR)
    draw_bird()
    draw_pipes()
    pygame.draw.rect(screen, random.choice(LAND_COLORS), (0, SCREEN_HEIGHT - land_height, SCREEN_WIDTH, land_height))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 100, 20))
    if game_over:
        game_over_text = font.render(f'Game Over! Best Score: {best_score}', True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        restart_text = font.render('Press SPACE to restart', True, (255, 255, 255))
        screen.blit(restart_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()