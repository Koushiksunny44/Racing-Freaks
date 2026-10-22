
import pygame

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Freaks")

# Game loop settings
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background colour: dark grey
    screen.fill((30, 30, 30))

    # Display the updated frame
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(60)

pygame.quit()
