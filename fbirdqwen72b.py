import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 30
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
PIPE_SPEED = 5

# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BROWN = (210, 180, 140)
DARK_GRAY = (105, 105, 105)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Random Background Color
BACKGROUND_COLOR = LIGHT_BLUE

# Random Land Color
LAND_COLOR = random.choice([DARK_BROWN, YELLOW])

# Random Bird Shape and Color
BIRD_SHAPES = ['square', 'circle', 'triangle']
BIRD_SHAPE = random.choice(BIRD_SHAPES)
BIRD_COLOR = random.choice([BLACK, DARK_GRAY, DARK_BROWN])

# Random Pipe Color
PIPE_COLOR = random.choice([DARK_GREEN, LIGHT_BROWN, DARK_GRAY])

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.acceleration = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.acceleration = 0

    def update(self):
        self.velocity += GRAVITY + self.acceleration
        self.y += self.velocity
        self.acceleration = 0

    def draw(self):
        if BIRD_SHAPE == 'square':
            pygame.draw.rect(screen, BIRD_COLOR, (self.x, self.y, 30, 30))
        elif BIRD_SHAPE == 'circle':
            pygame.draw.circle(screen, BIRD_COLOR, (self.x + 15, self.y + 15), 15)
        elif BIRD_SHAPE == 'triangle':
            points = [(self.x + 15, self.y), (self.x, self.y + 30), (self.x + 30, self.y + 30)]
            pygame.draw.polygon(screen, BIRD_COLOR, points)

    def check_collision(self, pipes):
        if self.y < 0 or self.y > SCREEN_HEIGHT - 50:
            return True
        for pipe in pipes:
            if pygame.Rect(self.x, self.y, 30, 30).colliderect(pipe[0]) or pygame.Rect(self.x, self.y, 30, 30).colliderect(pipe[1]):
                return True
        return False

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 50, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def move(self):
        self.x -= PIPE_SPEED
        self.top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 50, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def draw(self):
        pygame.draw.rect(screen, PIPE_COLOR, self.top_pipe)
        pygame.draw.rect(screen, PIPE_COLOR, self.bottom_pipe)

    def off_screen(self):
        return self.x < -50

# Main game loop
def main():
    bird = Bird()
    pipes = []
    last_pipe_time = 0
    score = 0
    high_score = 0
    running = True
    game_over = False

    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird.flap()
                        bird.acceleration = -1 * FLAP_STRENGTH / 2
                    else:
                        game_over = False
                        bird = Bird()
                        pipes = []
                        score = 0
                        last_pipe_time = 0
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > PIPE_FREQUENCY:
                pipes.append(Pipe(SCREEN_WIDTH))
                last_pipe_time = current_time

            bird.update()
            bird.draw()

            for pipe in pipes:
                pipe.move()
                pipe.draw()
                if pipe.off_screen():
                    pipes.remove(pipe)
                if pipe.x + 50 < bird.x and not pipe.passed:
                    score += 1
                    pipe.passed = True

            if bird.check_collision(pipes):
                game_over = True
                if score > high_score:
                    high_score = score

            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH - 120, 20))

            pygame.draw.rect(screen, LAND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        else:
            game_over_text = font.render(f"Game Over! Best Score: {high_score}", True, BLACK)
            restart_text = font.render("Press SPACE to Restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()