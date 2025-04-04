import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 40, bold=True)
small_font = pygame.font.SysFont("Arial", 25)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
SKY = (135, 206, 250)
YELLOW = (255, 255, 0)


def game_loop():
    # === BIRD SETTINGS ===
    bird_x = 100
    bird_y = 300
    bird_radius = 20
    bird_velocity = 0
    gravity = 0.5
    flap_power = -10

    # === PIPE SETTINGS ===
    pipe_width = 70
    pipe_gap = 150
    pipe_velocity = 3
    pipe_x = WIDTH
    pipe_height = random.randint(100, 400)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(SKY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = flap_power

        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_x -= pipe_velocity

        if pipe_x + pipe_width < 0:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)

        # Draw pipes
        pygame.draw.rect(screen, GREEN, (pipe_x, 0, pipe_width, pipe_height))
        bottom_pipe_y = pipe_height + pipe_gap
        pygame.draw.rect(screen, GREEN, (pipe_x, bottom_pipe_y, pipe_width, HEIGHT - bottom_pipe_y))

        # Draw bird
        pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)

        # Collision detection
        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe_rect = pygame.Rect(pipe_x, bottom_pipe_y, pipe_width, HEIGHT - bottom_pipe_y)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            running = False

        if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
            running = False

        pygame.display.update()

    show_restart_screen()


def show_restart_screen():
    screen.fill(SKY)
    
    # Text
    text = font.render("YOU SUCK. GET BETTER.", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Restart button
    button_text = small_font.render("RESTART", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 10, 120, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
                    game_loop()


# Start the game
game_loop()
