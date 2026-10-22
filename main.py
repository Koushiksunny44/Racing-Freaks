
import pygame

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Freaks")

clock = pygame.time.Clock()

# Colours (RGB)
GRASS = (35, 125, 55)
ROAD = (65, 65, 70)
WHITE = (240, 240, 240)
RED = (220, 45, 45)
BLACK = (20, 20, 20)

# Track settings
ROAD_LEFT = 200
ROAD_WIDTH = 400

# Player car
car_width = 50
car_height = 85
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 30
car_speed = 6

# Moving lane markings
line_y = 0
line_speed = 5

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read keyboard input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        car_x += car_speed

    # Keep the car inside the road
    car_x = max(ROAD_LEFT + 10, car_x)
    car_x = min(
        ROAD_LEFT + ROAD_WIDTH - car_width - 10,
        car_x
    )

    # Animate the road markings
    line_y += line_speed
    if line_y >= 80:
        line_y = 0

    # Draw the scene
    screen.fill(GRASS)

    pygame.draw.rect(
        screen, ROAD,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

    # Road edges
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT + 8, 0),
        (ROAD_LEFT + 8, HEIGHT), 4
    )
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT + ROAD_WIDTH - 8, 0),
        (ROAD_LEFT + ROAD_WIDTH - 8, HEIGHT), 4
    )

    # Dashed lane markings
    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(
            screen, WHITE,
            (WIDTH // 2 - 3, y + line_y, 6, 40)
        )

    # Draw the player car
    pygame.draw.rect(
        screen, RED,
        (car_x, car_y, car_width, car_height),
        border_radius=10
    )

    # Windscreen
    pygame.draw.rect(
        screen, BLACK,
        (car_x + 8, car_y + 12, car_width - 16, 22),
        border_radius=5
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
