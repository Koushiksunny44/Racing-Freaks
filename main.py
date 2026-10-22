
import random
import pygame

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Freaks")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 64)

# Colours
GRASS = (35, 125, 55)
ROAD = (65, 65, 70)
WHITE = (240, 240, 240)
RED = (220, 45, 45)
BLUE = (40, 130, 240)
BLACK = (20, 20, 20)
YELLOW = (255, 220, 50)

# Track
ROAD_LEFT = 200
ROAD_WIDTH = 400

# Player car
CAR_WIDTH = 50
CAR_HEIGHT = 85
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 30
car_speed = 6

# Enemy traffic
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 85
enemies = []
enemy_speed = 5
spawn_timer = 0

# Game state
score = 0
game_over = False
line_y = 0


def draw_car(x, y, colour):
    pygame.draw.rect(
        screen, colour,
        (x, y, CAR_WIDTH, CAR_HEIGHT),
        border_radius=10
    )
    pygame.draw.rect(
        screen, BLACK,
        (x + 8, y + 12, CAR_WIDTH - 16, 22),
        border_radius=5
    )


def reset_game():
    global car_x, enemies, enemy_speed
    global score, game_over, line_y, spawn_timer

    car_x = WIDTH // 2 - CAR_WIDTH // 2
    enemies = []
    enemy_speed = 5
    score = 0
    game_over = False
    line_y = 0
    spawn_timer = 0


running = True

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            car_x += car_speed

        car_x = max(ROAD_LEFT + 15, car_x)
        car_x = min(
            ROAD_LEFT + ROAD_WIDTH - CAR_WIDTH - 15,
            car_x
        )

        # Move road markings
        line_y = (line_y + enemy_speed) % 80

        # Spawn enemy traffic
        spawn_timer += dt
        if spawn_timer >= 1000:
            spawn_timer = 0

            lane_centres = [
                ROAD_LEFT + 75,
                ROAD_LEFT + ROAD_WIDTH // 2,
                ROAD_LEFT + ROAD_WIDTH - 75
            ]

            lane_x = random.choice(lane_centres) - ENEMY_WIDTH // 2
            enemies.append(
                pygame.Rect(
                    lane_x, -ENEMY_HEIGHT,
                    ENEMY_WIDTH, ENEMY_HEIGHT
                )
            )

        # Move enemies and award points for passing them
        for enemy in enemies:
            enemy.y += enemy_speed

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 1

        # Gradually increase difficulty
        enemy_speed = min(12, 5 + score // 8)

        # Collision detection
        player_rect = pygame.Rect(
            car_x, car_y, CAR_WIDTH, CAR_HEIGHT
        )

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True
                break

    # Draw background and road
    screen.fill(GRASS)

    pygame.draw.rect(
        screen, ROAD,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

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

    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(
            screen, WHITE,
            (WIDTH // 2 - 3, y + line_y, 6, 40)
        )

    # Draw cars
    draw_car(car_x, car_y, RED)

    for enemy in enemies:
        draw_car(enemy.x, enemy.y, BLUE)

    # Score display
    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    screen.blit(score_text, (20, 20))

    # Game-over overlay
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))

        title = large_font.render(
            "GAME OVER", True, YELLOW
        )
        final_score = font.render(
            f"Final Score: {score}", True, WHITE
        )
        restart = font.render(
            "Press R to Restart", True, WHITE
        )
        quit_text = font.render(
            "Press ESC to Quit", True, WHITE
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 230))
        )
        screen.blit(
            final_score,
            final_score.get_rect(center=(WIDTH // 2, 300))
        )
        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, 360))
        )
        screen.blit(
            quit_text,
            quit_text.get_rect(center=(WIDTH // 2, 405))
        )

    pygame.display.flip()

pygame.quit()
