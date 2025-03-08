"""
# Flappy Bird Game Implementation

## Requirements:
- Install pygame using `pip install pygame`
- Run this script to play the game
"""

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
LIGHT_COLORS = [(135, 206, 250), (250, 250, 210), (230, 230, 250)]
DARK_COLORS = [(0, 0, 139), (47, 79, 79), (139, 0, 0)]
LAND_COLORS = [(139, 69, 19), (255, 215, 0)]
PIPE_COLORS = [(0, 100, 0), (165, 42, 42), (85, 85, 85)]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Background color
background_color = random.choice(LIGHT_COLORS)
screen.fill(background_color)

# Land color
land_color = random.choice(LAND_COLORS)

# Bird properties
bird_radius = 20
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
bird_acceleration = 1
bird_shapes = ['circle', 'square', 'triangle']
bird_shape = random.choice(bird_shapes)
bird_color = random.choice(DARK_COLORS)

# Pipes
pipe_width = 50
pipe_gap = 150
pipe_velocity = -3
pipes = []
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks()

# Score
score = 0
font = pygame.font.SysFont(None, 35)
best_score = 0

def draw_bird():
    if bird_shape == 'circle':
        pygame.draw.circle(screen, bird_color, (bird_x + bird_radius, int(bird_y + bird_radius)), bird_radius)
    elif bird_shape == 'square':
        pygame.draw.rect(screen, bird_color, (bird_x, bird_y, bird_radius * 2, bird_radius * 2))
    elif bird_shape == 'triangle':
        points = [(bird_x, bird_y + bird_radius * 2), (bird_x + bird_radius * 2, bird_y), (bird_x - bird_radius * 2, bird_y)]
        pygame.draw.polygon(screen, bird_color, points)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, random.choice(PIPE_COLORS), pipe['top'])
        pygame.draw.rect(screen, random.choice(PIPE_COLORS), pipe['bottom'])

def draw_land():
    pygame.draw.rect(screen, land_color, (0, SCREEN_HEIGHT - 70, SCREEN_WIDTH, 70))

def check_collision():
    global bird_y
    if bird_y + bird_radius >= SCREEN_HEIGHT - 70 or bird_y <= bird_radius:
        return True
    for pipe in pipes:
        if bird_x < pipe['top'].right and bird_x + bird_radius > pipe['top'].left:
            if bird_y < pipe['top'].bottom or bird_y + bird_radius > pipe['bottom'].top:
                return True
    return False

def update_score():
    global score, best_score
    score += 1
    if score > best_score:
        best_score = score

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    # Update bird position
    bird_velocity += bird_acceleration
    bird_y += bird_velocity

    # Add new pipes
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe > pipe_frequency:
        pipe_height = random.randint(100, 400)
        pipes.append({'top': pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height),
                      'bottom': pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap)})
        last_pipe = current_time

    # Move pipes
    for pipe in pipes:
        pipe['top'].x += pipe_velocity
        pipe['bottom'].x += pipe_velocity

        # Remove pipes that have left the screen
        if pipe['top'].x < -pipe_width:
            pipes.remove(pipe)

    # Check for collision
    if check_collision():
        screen.fill(background_color)
        text = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        score = 0
        pipes.clear()
        bird_y = SCREEN_HEIGHT // 2
        bird_velocity = 0

    # Draw everything
    screen.fill(background_color)
    draw_bird()
    draw_pipes()
    draw_land()
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()