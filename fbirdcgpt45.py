import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 32)

# Colors
LIGHT_COLORS = [(173, 216, 230), (240, 230, 140), (224, 255, 255), (245, 222, 179)]
DARK_COLORS = [(139, 0, 0), (0, 0, 139), (0, 100, 0), (139, 69, 19), (85, 85, 85)]
GROUND_COLORS = [(139, 69, 19), (204, 204, 0)]
PIPE_COLORS = [(0, 100, 0), (205, 133, 63), (64, 64, 64)]

# Game variables
gravity = 0.5
bird_acceleration = -8


class Bird:
    def __init__(self):
        self.x, self.y = 100, HEIGHT // 2
        self.vel_y = 0
        self.shape = random.choice(['circle', 'square', 'triangle'])
        self.color = random.choice(DARK_COLORS)

    def update(self):
        self.vel_y += gravity
        self.y += self.vel_y

    def flap(self):
        self.vel_y += bird_acceleration

    def draw(self):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.x, int(self.y)), 15)
        elif self.shape == 'square':
            pygame.draw.rect(screen, self.color, (self.x - 15, self.y - 15, 30, 30))
        else:  # triangle
            pygame.draw.polygon(screen, self.color, [(self.x, self.y - 18), (self.x - 18, self.y + 15), (self.x + 18, self.y + 15)])

    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 30)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 70
        self.gap = random.randint(150, 200)
        self.height = random.randint(100, HEIGHT - self.gap - 100)
        self.color = random.choice(PIPE_COLORS)

    def update(self):
        self.x -= 3

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, self.height + self.gap, self.width, HEIGHT - self.height - self.gap - ground_height))

    def collide(self, bird_rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + self.gap, self.width, HEIGHT - self.height - self.gap - ground_height)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


# Initializing game elements
def init_game():
    global bird, pipes, score, ground_height, bg_color
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    ground_height = 50
    bg_color = random.choice(LIGHT_COLORS)


init_game()
high_score = 0
running = True
game_active = True

# Game loop
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird.flap()
                else:
                    init_game()
                    game_active = True
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    if game_active:
        bird.update()
        bird_rect = bird.get_rect()

        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe(WIDTH))

        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                score += 1

            if pipe.collide(bird_rect) or bird.y > HEIGHT - ground_height or bird.y < 0:
                game_active = False
                if score > high_score:
                    high_score = score

    # Drawing
    screen.fill(bg_color)

    for pipe in pipes:
        pipe.draw()

    bird.draw()

    pygame.draw.rect(screen, random.choice(GROUND_COLORS), (0, HEIGHT - ground_height, WIDTH, ground_height))

    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    if not game_active:
        best_score_text = font.render(f'Best Score: {high_score}', True, (255, 0, 0))
        screen.blit(best_score_text, (WIDTH//2 - best_score_text.get_width()//2, HEIGHT//2 - best_score_text.get_height()//2))

    pygame.display.flip()

pygame.quit()
