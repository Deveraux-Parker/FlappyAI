import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GAP_HEIGHT = 150
PIPE_WIDTH = 50
PIPE_SPEED = 4
LAND_HEIGHT = 50
GRAVITY = 0.5
JUMP_STRENGTH = -12

# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_BROWN = (101, 67, 33)
YELLOW = (204, 204, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BROWN = (150, 75, 0)
DARK_GRAY = (64, 64, 64)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

def random_light_color():
    return (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))

def random_dark_color():
    return (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))

class Bird:
    def __init__(self):
        self.size = 30
        self.x = 50
        self.y = SCREEN_HEIGHT // 2 - self.size // 2
        self.velocity = 0
        self.shape = random.choice(['square', 'circle', 'triangle'])
        self.color = random_dark_color()
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self):
        self.velocity += JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        if self.shape == 'square':
            pygame.draw.rect(screen, self.color, self.rect)
        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, self.rect.center, self.size//2)
        elif self.shape == 'triangle':
            points = [
                (self.x, self.y + self.size),
                (self.x + self.size//2, self.y),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(screen, self.color, points)

def create_pipe():
    gap_y = random.randint(100, SCREEN_HEIGHT - GAP_HEIGHT - 100)
    pipe_color = random.choice([DARK_GREEN, LIGHT_BROWN, DARK_GRAY])
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, gap_y + GAP_HEIGHT, PIPE_WIDTH, SCREEN_HEIGHT - gap_y - GAP_HEIGHT)
    return {'top': top_pipe, 'bottom': bottom_pipe, 'color': pipe_color, 'scored': False}

def reset_game():
    global bird, pipes, score, background_color, land_color, game_active
    bird = Bird()
    pipes = []
    score = 0
    background_color = random_light_color()
    land_color = random.choice([DARK_BROWN, YELLOW])
    game_active = True

# Initial game state
background_color = LIGHT_BLUE
land_color = random.choice([DARK_BROWN, YELLOW])
bird = Bird()
pipes = []
score = 0
best_score = 0
game_active = False
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird.jump()
                else:
                    if game_over:
                        reset_game()
                    else:
                        game_active = True
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    screen.fill(background_color)

    if game_active:
        # Bird update
        bird.update()

        # Ground/top collision
        if bird.rect.bottom >= SCREEN_HEIGHT - LAND_HEIGHT or bird.rect.top <= 0:
            game_active = False
            game_over = True

        # Pipe generation
        if pygame.time.get_ticks() % 1500 < 30:
            pipes.append(create_pipe())

        # Pipe logic
        for pipe in pipes:
            pipe['top'].x -= PIPE_SPEED
            pipe['bottom'].x -= PIPE_SPEED

            # Scoring
            if not pipe['scored'] and bird.rect.left > pipe['top'].right:
                score += 1
                pipe['scored'] = True
                if score > best_score:
                    best_score = score

            # Collision
            if bird.rect.colliderect(pipe['top']) or bird.rect.colliderect(pipe['bottom']):
                game_active = False
                game_over = True

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['top'].right > 0]

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, pipe['color'], pipe['top'])
            pygame.draw.rect(screen, pipe['color'], pipe['bottom'])

        # Draw bird
        bird.draw()
    else:
        # Game over screen
        if game_over:
            text = font.render(f"Score: {score}  Best: {best_score}", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
        else:
            start_text = font.render("Press SPACE to start", True, BLACK)
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))

    # Draw land
    pygame.draw.rect(screen, land_color, (0, SCREEN_HEIGHT - LAND_HEIGHT, SCREEN_WIDTH, LAND_HEIGHT))

    # Draw score
    score_text = font.render(str(score), True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 50, 10))

    pygame.display.update()
    clock.tick(FPS)