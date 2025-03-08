import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# Functions to generate random colors
def random_light_color():
    # Returns a random light color (each RGB channel between 200 and 255)
    return (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))

def random_dark_color():
    # Returns a random dark color (each RGB channel between 0 and 80)
    return (random.randint(0, 80), random.randint(0, 80), random.randint(0, 80))

# Initial background color (light blue) and land color options
background_color = (173, 216, 230)  # light blue
land_colors = [(101, 67, 33), (218, 165, 32)]  # dark brown or yellow-ish
land_color = random.choice(land_colors)
land_height = 100

# Pipe settings: width, gap size, and color options (dark green, light brown, dark gray)
pipe_width = 60
gap_height = 150
pipe_colors = [(0, 100, 0), (181, 101, 29), (105, 105, 105)]

# Bird settings: starting position, size, shape and color.
bird_size = 30
bird_x = 50
bird_y = HEIGHT // 2
bird_shapes = ["square", "circle", "triangle"]
bird_shape = random.choice(bird_shapes)
bird_color = random_dark_color()

# Game physics variables
gravity = 0.5
bird_velocity = 0

# Pipes list and timing for new pipes (in milliseconds)
pipes = []
pipe_frequency = 1500  # new pipe every 1500 ms
last_pipe_time = pygame.time.get_ticks() - pipe_frequency

# Score variables
score = 0
best_score = 0

# Game state and font for texts
game_active = True
font = pygame.font.SysFont(None, 36)

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_active, background_color, bird_shape, bird_color, land_color
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    score = 0
    game_active = True
    # Choose a new random light background color (after the initial light blue)
    background_color = random_light_color()
    # Randomly choose a bird shape and dark color
    bird_shape = random.choice(bird_shapes)
    bird_color = random_dark_color()
    # Randomly choose land color
    land_color = random.choice(land_colors)

def draw_bird(x, y):
    if bird_shape == "square":
        pygame.draw.rect(screen, bird_color, (x, y, bird_size, bird_size))
    elif bird_shape == "circle":
        radius = bird_size // 2
        pygame.draw.circle(screen, bird_color, (x + radius, y + radius), radius)
    elif bird_shape == "triangle":
        # Create an equilateral triangle shape
        point1 = (x + bird_size // 2, y)
        point2 = (x, y + bird_size)
        point3 = (x + bird_size, y + bird_size)
        pygame.draw.polygon(screen, bird_color, [point1, point2, point3])

def draw_pipes():
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, pipe['pipe_color'], (pipe['x'], 0, pipe_width, pipe['gap_y']))
        # Bottom pipe (leaving space for the land)
        bottom_pipe_height = HEIGHT - land_height - (pipe['gap_y'] + gap_height)
        pygame.draw.rect(screen, pipe['pipe_color'], (pipe['x'], pipe['gap_y'] + gap_height, pipe_width, bottom_pipe_height))

def draw_land():
    pygame.draw.rect(screen, land_color, (0, HEIGHT - land_height, WIDTH, land_height))

def draw_score():
    score_surface = font.render(str(score), True, (0, 0, 0))
    screen.blit(score_surface, (WIDTH - score_surface.get_width() - 10, 10))

def check_collisions():
    # Create a rect for the bird
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
    # Collision with the land
    if bird_y + bird_size > HEIGHT - land_height:
        return True
    # Collision with any pipe (top or bottom)
    for pipe in pipes:
        top_pipe_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['gap_y'])
        bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + gap_height,
                                       pipe_width, HEIGHT - land_height - (pipe['gap_y'] + gap_height))
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
    return False

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    # Accelerate the bird upward when SPACE is pressed
                    bird_velocity = -8
                else:
                    # Restart the game on SPACE after game over
                    reset_game()
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    if game_active:
        # Update bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Create new pipes at set intervals
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > pipe_frequency:
            gap_y = random.randint(50, HEIGHT - land_height - gap_height - 50)
            new_pipe = {
                'x': WIDTH,
                'gap_y': gap_y,
                'passed': False,
                'pipe_color': random.choice(pipe_colors)
            }
            pipes.append(new_pipe)
            last_pipe_time = current_time

        # Move pipes to the left
        for pipe in pipes:
            pipe['x'] -= 3

        # Remove pipes that have moved off screen
        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

        # Increase score when the bird passes a pipe
        for pipe in pipes:
            if not pipe['passed'] and pipe['x'] + pipe_width < bird_x:
                pipe['passed'] = True
                score += 1
                if score > best_score:
                    best_score = score

        # Check for collisions with pipes or the land
        if check_collisions():
            game_active = False

        # Draw game elements
        screen.fill(background_color)
        draw_pipes()
        draw_land()
        draw_bird(bird_x, bird_y)
        draw_score()

    else:
        # Game over screen: display the final frame and game over texts
        screen.fill(background_color)
        draw_pipes()
        draw_land()
        draw_bird(bird_x, bird_y)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        best_text = font.render(f"Best: {best_score}", True, (0, 0, 0))
        restart_text = font.render("Press SPACE to restart, Q or ESC to quit", True, (0, 0, 0))
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 3))
        screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 3 + 40))
        screen.blit(best_text, ((WIDTH - best_text.get_width()) // 2, HEIGHT // 3 + 80))
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 3 + 120))

    pygame.display.update()

pygame.quit()
sys.exit()
