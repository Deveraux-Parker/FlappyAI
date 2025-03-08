import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 250)
DARK_BROWN = (101, 67, 33)
YELLOW = (218, 165, 32)
DARK_GREEN = (0, 100, 0)
LIGHT_BROWN = (139, 69, 19)
DARK_GRAY = (64, 64, 64)


# Function to generate random light color
def random_light_color():
    return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))


# Function to generate random dark color
def random_dark_color():
    return (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))


# Function to generate random ground color
def random_ground_color():
    return random.choice([DARK_BROWN, YELLOW])


# Function to generate random pipe color
def random_pipe_color():
    return random.choice([DARK_GREEN, LIGHT_BROWN, DARK_GRAY])


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for score display
font = pygame.font.Font(None, 36)


class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.size = 20
        self.velocity = 0
        self.shape = random.choice(["square", "circle", "triangle"])
        self.color = random_dark_color()

    def jump(self):
        # Multiple presses will accelerate the bird upward
        # Adding to the current velocity makes it go faster upward
        self.velocity += JUMP_STRENGTH
        # Cap the velocity to prevent too rapid acceleration
        self.velocity = max(self.velocity, JUMP_STRENGTH * 2)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        if self.shape == "square":
            pygame.draw.rect(screen, self.color,
                             (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)
        elif self.shape == "triangle":
            points = [
                (self.x, self.y - self.size // 2),
                (self.x - self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 2, self.y + self.size // 2)
            ]
            pygame.draw.polygon(screen, self.color, points)

    def get_rect(self):
        if self.shape == "square":
            return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
        elif self.shape == "circle":
            return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
        elif self.shape == "triangle":
            return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(200, SCREEN_HEIGHT - GROUND_HEIGHT - 200)
        self.width = 50
        self.passed = False
        self.color = random_pipe_color()

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.gap_y - PIPE_GAP // 2))
        # Draw bottom pipe
        pygame.draw.rect(screen, self.color, (
        self.x, self.gap_y + PIPE_GAP // 2, self.width, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2) - GROUND_HEIGHT))

    def is_offscreen(self):
        return self.x + self.width < 0

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, self.width,
                                  SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2) - GROUND_HEIGHT)
        return [top_rect, bottom_rect]


class Game:
    def __init__(self):
        self.best_score = 0
        self.background_color = LIGHT_BLUE  # Start with light blue
        self.ground_color = random_ground_color()
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.game_over = False
        if self.score > 0 or self.best_score > 0:  # Only change after first game
            self.background_color = random_light_color()
        self.ground_color = random_ground_color()

    def update(self):
        if not self.game_over:
            self.bird.update()

            # Create new pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_time > PIPE_FREQUENCY:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.last_pipe_time = current_time

            # Update pipes
            for pipe in self.pipes:
                pipe.update()

                # Check if pipe is passed
                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1

            # Remove offscreen pipes
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]

            # Check collisions
            self.check_collisions()

    def check_collisions(self):
        bird_rect = self.bird.get_rect()

        # Check ground collision
        if self.bird.y + self.bird.size // 2 > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.game_over = True

        # Check ceiling collision
        if self.bird.y - self.bird.size // 2 < 0:
            self.game_over = True

        # Check pipe collisions
        for pipe in self.pipes:
            pipe_rects = pipe.get_rects()
            for rect in pipe_rects:
                if bird_rect.colliderect(rect):
                    self.game_over = True

        # Update best score
        if self.game_over and self.score > self.best_score:
            self.best_score = self.score

    def draw(self):
        # Draw background
        screen.fill(self.background_color)

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()

        # Draw ground
        pygame.draw.rect(screen, self.ground_color, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        # Draw bird
        self.bird.draw()

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

        # Draw game over screen
        if self.game_over:
            game_over_text = font.render("Game Over", True, BLACK)
            best_score_text = font.render(f"Best Score: {self.best_score}", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            quit_text = font.render("Press Q or ESC to quit", True, BLACK)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(best_score_text,
                        (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 40))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 3 + 80))
            screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 3 + 120))


def main():
    game = Game()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.game_over:
                        game.reset()
                    else:
                        game.bird.jump()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()