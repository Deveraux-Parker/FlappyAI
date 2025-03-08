import pygame
import random
import sys

pygame.init()

# Game constants
screen_width = 480
screen_height = 800
FPS = 60

# Colors
light_colors = [
    (173, 216, 230),  # Light blue
    (204, 255, 229),  # Light green
    (255, 229, 204),  # Light yellow
    (204, 229, 255),  # Light blueish
    (229, 204, 255)  # Light purple
]

dark_colors = [
    (0, 0, 0),
    (30, 30, 30),
    (50, 50, 50),
    (80, 80, 80),
    (100, 100, 100)
]

land_colors = [(139, 69, 19), (255, 255, 0)]  # Dark brown or yellow

pipe_colors = [
    (0, 100, 0),  # Dark green
    (210, 180, 140),  # Light brown
    (100, 100, 100)  # Dark gray
]

# Initialize screen and clock
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Bird parameters
bird_size = 30
bird_x = screen_width // 2 - bird_size // 2
bird_y = screen_height // 2
bird_vel = 0
gravity = 0.5
jump_strength = -8

bird_shape = random.choice(['square', 'circle', 'triangle'])
bird_color = random.choice(dark_colors)

# Land parameters
land_height = 100
land_color = random.choice(land_colors)
land_rect = pygame.Rect(0, screen_height - land_height, screen_width, land_height)

# Pipes parameters
pipe_speed = 3
pipe_gap = 150
pipe_width = 50
pipes = []

ADDPIPE = pygame.USEREVENT
pygame.time.set_timer(ADDPIPE, 1200)  # Every 1.2 seconds

# Score
score = 0
best_score = 0
font = pygame.font.Font(None, 48)  # Larger font
score_font = pygame.font.Font(None, 36)

background_color = random.choice(light_colors)


def draw_bird(screen, x, y, shape, color):
    if shape == 'square':
        pygame.draw.rect(screen, color, (x, y, bird_size, bird_size))
    elif shape == 'circle':
        pygame.draw.circle(screen, color, (x + bird_size // 2, y + bird_size // 2), bird_size // 2)
    elif shape == 'triangle':
        points = [
            (x + bird_size // 2, y),
            (x, y + bird_size),
            (x + bird_size, y + bird_size)
        ]
        pygame.draw.polygon(screen, color, points)


running = True
game_over = False

while running:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel += jump_strength
            if event.type == ADDPIPE:
                # Create new pipe
                pipe_color = random.choice(pipe_colors)
                max_pipe_height = screen_height - land_height - pipe_gap - 1
                pipe_height = random.randint(150, max_pipe_height)
                top_pipe = pygame.Rect(screen_width, 0, pipe_width, pipe_height)
                bottom_pipe_height = (screen_height - land_height) - (pipe_height + pipe_gap)
                bottom_pipe = pygame.Rect(screen_width, pipe_height + pipe_gap, pipe_width, bottom_pipe_height)
                pipes.append({
                    'top_rect': top_pipe,
                    'bottom_rect': bottom_pipe,
                    'has_scored': False,
                    'color': pipe_color
                })

        # Update bird's physics
        bird_vel += gravity
        bird_y += bird_vel
        bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

        # Check land collision
        if bird_rect.colliderect(land_rect):
            game_over = True
            if score > best_score:
                best_score = score

        # Check pipe collisions
        for pipe in pipes:
            if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
                game_over = True
                if score > best_score:
                    best_score = score
                break

        # Update pipes
        pipes_to_remove = []
        for pipe in pipes:
            pipe['top_rect'].x -= pipe_speed
            pipe['bottom_rect'].x -= pipe_speed
            if pipe['top_rect'].x + pipe_width < 0:
                pipes_to_remove.append(pipe)
            if not pipe['has_scored'] and bird_rect.x > pipe['top_rect'].x + pipe_width:
                score += 1
                pipe['has_scored'] = True
        for p in pipes_to_remove:
            pipes.remove(p)

        # Draw everything
        screen.fill(background_color)
        for pipe in pipes:
            pygame.draw.rect(screen, pipe['color'], pipe['top_rect'])
            pygame.draw.rect(screen, pipe['color'], pipe['bottom_rect'])
        draw_bird(screen, bird_x, bird_y, bird_shape, bird_color)
        pygame.draw.rect(screen, land_color, land_rect)

        # Improved score display with shadow effect
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (screen_width - 150, 10))
        score_text_shadow = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text_shadow, (screen_width - 153, 13))

        pygame.display.flip()
    else:
        # Game over screen with centered text
        screen.fill(background_color)

        # Game Over text
        game_over_text = font.render(f"GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Best Score text
        best_score_text = font.render(f"Best: {best_score}", True, (255, 0, 0))
        best_score_rect = best_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(best_score_text, best_score_rect)

        # Restart instructions
        restart_text = font.render("Press SPACE to restart", True, (255, 0, 0))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 70))
        screen.blit(restart_text, restart_rect)

        quit_text = font.render("ESC or Q to quit", True, (255, 0, 0))
        quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 120))
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Handle events in game over state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    # Restart the game
                    bird_x = screen_width // 2 - bird_size // 2
                    bird_y = screen_height // 2
                    bird_vel = 0
                    score = 0
                    pipes = []
                    background_color = random.choice(light_colors)
                    bird_shape = random.choice(['square', 'circle', 'triangle'])
                    bird_color = random.choice(dark_colors)
                    land_color = random.choice(land_colors)
                    game_over = False

    clock.tick(FPS)

pygame.quit()
sys.exit()