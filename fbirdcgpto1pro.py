import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# -------------------------- CONSTANTS AND SETTINGS --------------------------
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
FPS = 60
PIPE_SPEED = 3
PIPE_WIDTH = 60
PIPE_GAP = 150  # Vertical gap between pipes
PIPE_DISTANCE = 300  # Horizontal distance between pipes
BIRD_SIZE = 20  # Base size for the bird's bounding box
GRAVITY = 0.4  # Gravity pulling the bird down
FLAP_ACCELERATION = 6  # How much velocity is subtracted when SPACE is pressed

# Font for score display
FONT = pygame.font.SysFont("Arial", 24, bold=True)
BIG_FONT = pygame.font.SysFont("Arial", 48, bold=True)


# -------------------------- COLOR HELPERS --------------------------
def random_light_color():
    """Return a random light (pastel) color."""
    return (
        random.randint(180, 255),
        random.randint(180, 255),
        random.randint(180, 255)
    )


def random_dark_color():
    """Return a random dark color."""
    return (
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(0, 100)
    )


def get_land_color():
    """Return either dark brown or yellow."""
    colors = [
        (101, 67, 33),  # Dark brown
        (255, 255, 0),  # Yellow
    ]
    return random.choice(colors)


def get_pipe_color():
    """Return either dark green, light brown, or dark gray."""
    colors = [
        (0, 100, 0),  # Dark green
        (210, 180, 140),  # Light brown
        (64, 64, 64),  # Dark gray
    ]
    return random.choice(colors)


# -------------------------- GAME OBJECTS --------------------------
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

        # Random shape and color
        self.shape = random.choice(["square", "circle", "triangle"])
        self.color = random_dark_color()

        # For collision detection we'll use a bounding box.
        # The bird's "hitbox" is roughly a square of side BIRD_SIZE
        self.width = BIRD_SIZE
        self.height = BIRD_SIZE

    def flap(self):
        """When SPACE is pressed, accelerate upwards."""
        # Subtract from velocity to move up
        self.velocity -= FLAP_ACCELERATION

    def update(self):
        """Update bird position by applying gravity and velocity."""
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, surface):
        """Draw the bird with its shape and color."""
        if self.shape == "square":
            pygame.draw.rect(
                surface,
                self.color,
                (self.x - self.width // 2, self.y - self.height // 2,
                 self.width, self.height)
            )
        elif self.shape == "circle":
            pygame.draw.circle(
                surface,
                self.color,
                (int(self.x), int(self.y)),
                self.width // 2
            )
        else:  # triangle
            # An upward-pointing triangle
            point1 = (self.x, self.y - self.height // 2)
            point2 = (self.x - self.width // 2, self.y + self.height // 2)
            point3 = (self.x + self.width // 2, self.y + self.height // 2)
            pygame.draw.polygon(surface, self.color, [point1, point2, point3])

    def get_rect(self):
        """Return the bounding rectangle for collision detection."""
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )


class Pipe:
    def __init__(self, x, gap_center, gap_height):
        self.x = x
        self.gap_center = gap_center
        self.gap_height = gap_height
        self.width = PIPE_WIDTH
        self.color = get_pipe_color()

    def update(self):
        """Move the pipe to the left."""
        self.x -= PIPE_SPEED

    def draw(self, surface):
        """Draw the top and bottom parts of the pipe."""
        # Top pipe rectangle
        top_rect = pygame.Rect(
            self.x,
            0,
            self.width,
            self.gap_center - self.gap_height // 2
        )
        # Bottom pipe rectangle
        bottom_rect = pygame.Rect(
            self.x,
            self.gap_center + self.gap_height // 2,
            self.width,
            SCREEN_HEIGHT - (self.gap_center + self.gap_height // 2)
        )
        pygame.draw.rect(surface, self.color, top_rect)
        pygame.draw.rect(surface, self.color, bottom_rect)

    def is_off_screen(self):
        """Check if the pipe has fully moved off the left of the screen."""
        return self.x + self.width < 0

    def check_collision(self, bird_rect):
        """Check collision with the bird's rectangle."""
        top_rect = pygame.Rect(
            self.x,
            0,
            self.width,
            self.gap_center - self.gap_height // 2
        )
        bottom_rect = pygame.Rect(
            self.x,
            self.gap_center + self.gap_height // 2,
            self.width,
            SCREEN_HEIGHT - (self.gap_center + self.gap_height // 2)
        )
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


# -------------------------- MAIN GAME LOGIC --------------------------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird (Randomized)")

    clock = pygame.time.Clock()

    # Global best score
    best_score = 0

    def reset_game():
        """Reset and return initial game objects and states."""
        bg_color = random_light_color()
        land_color = get_land_color()

        bird = Bird(x=SCREEN_WIDTH // 4, y=SCREEN_HEIGHT // 2)

        pipes = []
        # Start with one pipe to the right, so it scrolls onto the screen
        initial_x = SCREEN_WIDTH + 100
        # Random gap center
        gap_center = random.randint(150, SCREEN_HEIGHT - 150)
        pipes.append(Pipe(initial_x, gap_center, PIPE_GAP))

        score = 0
        return bird, pipes, score, bg_color, land_color

    # Start a new game
    bird, pipes, score, bg_color, land_color = reset_game()
    game_active = True

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    if game_active:
                        # Flap if game is active
                        bird.flap()
                    else:
                        # Restart if the game is over
                        bird, pipes, score, bg_color, land_color = reset_game()
                        game_active = True

        if game_active:
            # Update the bird
            bird.update()

            # Collision with ground or out of top bounds
            bird_rect = bird.get_rect()
            if bird.y + bird.height // 2 >= SCREEN_HEIGHT - 40:  # Collides with ground
                game_active = False
                if score > best_score:
                    best_score = score
            if bird.y - bird.height // 2 <= 0:  # Hits the top
                game_active = False
                if score > best_score:
                    best_score = score

            # Update and manage pipes
            for pipe in pipes:
                pipe.update()

            # Check for pipe collisions
            for pipe in pipes:
                if pipe.check_collision(bird_rect):
                    game_active = False
                    if score > best_score:
                        best_score = score
                    break

            # Remove off-screen pipes
            pipes = [p for p in pipes if not p.is_off_screen()]

            # Add new pipes if needed
            # If the last pipe is far enough left, add a new one
            if len(pipes) > 0:
                last_pipe = pipes[-1]
                if SCREEN_WIDTH - (last_pipe.x + last_pipe.width) > PIPE_DISTANCE:
                    # Generate a new pipe
                    new_x = SCREEN_WIDTH
                    new_gap_center = random.randint(150, SCREEN_HEIGHT - 150)
                    pipes.append(Pipe(new_x, new_gap_center, PIPE_GAP))

            # Scoring: if bird just passed the left edge of a pipe, increment
            for pipe in pipes:
                # if the bird's x is > pipe.x + pipe.width -> meaning we passed it
                if not hasattr(pipe, 'scored') or pipe.scored is False:
                    if bird.x > pipe.x + pipe.width:
                        score += 1
                        pipe.scored = True

        # -------------------------- DRAW SECTION --------------------------
        screen.fill(bg_color)

        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)

        # Draw ground (a rectangle at bottom)
        pygame.draw.rect(screen, land_color, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))

        # Draw bird
        bird.draw(screen)

        # Draw score (top right)
        score_surface = FONT.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_surface, score_rect)

        # If game over, display best score
        if not game_active:
            game_over_text = BIG_FONT.render("GAME OVER", True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(game_over_text, game_over_rect)

            best_score_text = FONT.render(f"Best Score: {best_score}", True, (0, 0, 0))
            best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(best_score_text, best_score_rect)

            restart_text = FONT.render("Press SPACE to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()


# Run the game
if __name__ == "__main__":
    main()
