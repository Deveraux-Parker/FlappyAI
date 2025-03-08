import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Generate random light background color
def get_light_color():
    return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

background_color = get_light_color()

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = 8  # Acceleration per jump
        self.max_upward_velocity = -15  # Maximum upward speed
        self.shape = random.choice(['square', 'circle', 'triangle'])
        self.color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        self.size = 30

    def jump(self):
        self.velocity = max(self.max_upward_velocity, self.velocity - self.jump_strength)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        if self.shape == 'square':
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.x + self.size//2, self.y + self.size//2), self.size//2)
        elif self.shape == 'triangle':
            points = [(self.x, self.y + self.size),
                      (self.x + self.size//2, self.y),
                      (self.x + self.size, self.y + self.size)]
            pygame.draw.polygon(screen, self.color, points)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 80
        self.gap = 200
        self.gap_position = random.randint(100, HEIGHT - 200)
        self.color = random.choice([(0, 100, 0), (139, 69, 19), (64, 64, 64)])
        self.passed = False

    def move(self):
        self.x -= 3
        if self.x < -self.width:
            self.x = WIDTH
            self.gap_position = random.randint(100, HEIGHT - 200)
            self.passed = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.gap_position))
        pygame.draw.rect(screen, self.color, (self.x, self.gap_position + self.gap, self.width, HEIGHT - self.gap_position - self.gap))

# Ground setup
ground_color = random.choice([(139, 69, 19), (205, 133, 63)])
ground_height = 50

# Score variables
score = 0
best_score = 0
font = pygame.font.Font(None, 36)

# Initialize game objects
clock = pygame.time.Clock()
bird = Bird()
pipes = [Pipe(WIDTH), Pipe(WIDTH + WIDTH//2)]
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    bird.jump()
                else:
                    # Reset game
                    game_over = False
                    bird = Bird()
                    pipes = [Pipe(WIDTH), Pipe(WIDTH + WIDTH//2)]
                    score = 0
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                running = False

    if not game_over:
        # Update bird
        bird.update()

        # Check ground collision
        if bird.y + bird.size >= HEIGHT - ground_height:
            game_over = True

        # Update pipes and check collisions
        for pipe in pipes:
            pipe.move()
            # Horizontal collision check
            if (pipe.x < bird.x + bird.size < pipe.x + pipe.width) or (pipe.x < bird.x < pipe.x + pipe.width):
                # Vertical collision check
                if bird.y < pipe.gap_position or bird.y + bird.size > pipe.gap_position + pipe.gap:
                    game_over = True
            # Score update
            if bird.x > pipe.x + pipe.width and not pipe.passed:
                score += 1
                pipe.passed = True
                if score > best_score:
                    best_score = score

        # Draw everything
        screen.fill(background_color)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        pygame.draw.rect(screen, ground_color, (0, HEIGHT - ground_height, WIDTH, ground_height))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 150, 10))
    else:
        # Game over screen
        game_over_text = font.render("Game Over! Press SPACE to restart", True, (0, 0, 0))
        best_score_text = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2 - 20))
        screen.blit(best_score_text, (WIDTH//2 - 120, HEIGHT//2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()