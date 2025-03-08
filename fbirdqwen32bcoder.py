import pygame
import random
import sys

pygame.init()

screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")


def random_light_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


dark_green = (0, 128, 0)
light_brown = (210, 180, 140)
dark_gray = (105, 105, 105)
pipe_colors = [dark_green, light_brown, dark_gray]

bird_size = 30
pipe_width = 50
land_height = 100
gravity = 0.5
pipe_speed = 3
pipe_add_interval = 1500  # milliseconds
pipe_gap_min = 150
pipe_gap_max = 250
best_score = 0


def draw_game_over(screen, current_score, best_score):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Score: {current_score}", True, (255, 0, 0))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))
    best_text = font.render(f"Best: {best_score}", True, (255, 0, 0))
    screen.blit(best_text, (screen_width // 2 - best_text.get_width() // 2, screen_height // 2))
    restart_text = font.render("Press SPACE to restart or Q/ESC to quit", True, (255, 0, 0))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))


clock = pygame.time.Clock()
running = True
first_run = True

while running:
    game_over = False
    current_score = 0
    bird_x = 50
    bird_y = 250
    bird_vel = 0
    bird_shape = random.choice(['square', 'circle', 'triangle'])
    bird_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    land_color = random.choice([(139, 69, 19), (255, 255, 0)])

    if first_run:
        background_color = (173, 216, 230)  # Light blue first time
        first_run = False
    else:
        background_color = random_light_color()

    pipes = []
    last_pipe_time = pygame.time.get_ticks()

    while not game_over and running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel -= 10  # Upward thrust
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    game_over = True

        bird_vel += gravity
        bird_y += bird_vel

        if bird_y + bird_size > screen_height - land_height or bird_y < 0:
            game_over = True

        if current_time - last_pipe_time > pipe_add_interval:
            pipe_gap = random.randint(pipe_gap_min, pipe_gap_max)
            upper_height = random.randint(50, screen_height - land_height - pipe_gap - 50)
            lower_start_y = upper_height + pipe_gap
            lower_height = (screen_height - land_height) - lower_start_y
            pipe_color = random.choice(pipe_colors)
            new_pipe = {
                'x': screen_width,
                'upper_height': upper_height,
                'lower_start_y': lower_start_y,
                'lower_height': lower_height,
                'color': pipe_color,
                'scored': False
            }
            pipes.append(new_pipe)
            last_pipe_time = current_time

        remove_pipes = []
        for pipe in pipes:
            pipe['x'] -= pipe_speed

            bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
            upper_pipe_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['upper_height'])
            lower_pipe_rect = pygame.Rect(pipe['x'], pipe['lower_start_y'], pipe_width, pipe['lower_height'])

            if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
                game_over = True

            if bird_x > pipe['x'] + pipe_width and not pipe['scored']:
                current_score += 1
                pipe['scored'] = True

            if pipe['x'] + pipe_width < 0:
                remove_pipes.append(pipe)

        for pipe in remove_pipes:
            pipes.remove(pipe)

        screen.fill(background_color)

        for pipe in pipes:
            pygame.draw.rect(screen, pipe['color'], (pipe['x'], 0, pipe_width, pipe['upper_height']))
            pygame.draw.rect(screen, pipe['color'],
                             (pipe['x'], pipe['lower_start_y'], pipe_width, pipe['lower_height']))

        pygame.draw.rect(screen, land_color, (0, screen_height - land_height, screen_width, land_height))

        if bird_shape == 'square':
            pygame.draw.rect(screen, bird_color, (bird_x, bird_y, bird_size, bird_size))
        elif bird_shape == 'circle':
            pygame.draw.circle(screen, bird_color, (bird_x + bird_size // 2, bird_y + bird_size // 2), bird_size // 2)
        elif bird_shape == 'triangle':
            points = [
                (bird_x + bird_size // 2, bird_y),
                (bird_x, bird_y + bird_size),
                (bird_x + bird_size, bird_y + bird_size)
            ]
            pygame.draw.polygon(screen, bird_color, points)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {current_score}", True, (0, 0, 0))
        screen.blit(score_text, (screen_width - 150, 10))

        pygame.display.update()
        clock.tick(60)

    if running:
        best_score = max(best_score, current_score)
        while game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = False
                    elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False

            screen.fill(background_color)
            draw_game_over(screen, current_score, best_score)
            pygame.display.update()
            clock.tick(60)

pygame.quit()
sys.exit()