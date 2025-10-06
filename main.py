
import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("เกมเก็บเหรียญ + แลกของ + เสียง")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COIN_COLOR = (255, 215, 0)

player_size = 30
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

coin_sound = pygame.mixer.Sound("coin.wav")

coin_radius = 10
coin_x = random.randint(coin_radius, WIDTH - coin_radius)
coin_y = random.randint(coin_radius, HEIGHT - coin_radius)

score = 0
max_score = 30
font = pygame.font.SysFont(None, 32)

show_shop = False
shop_message = ""

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                show_shop = not show_shop
                shop_message = ""
            if show_shop:
                if event.key == pygame.K_1:
                    if score >= 5:
                        score -= 5
                        player_speed += 2
                        shop_message = "แลกความเร็วเพิ่มแล้ว!"
                    else:
                        shop_message = "คะแนนไม่พอ (ต้องมี 5)"
                elif event.key == pygame.K_2:
                    if score >= 10:
                        score -= 10
                        shop_message = "ได้รับไอเทมพิเศษ!"
                    else:
                        shop_message = "คะแนนไม่พอ (ต้องมี 10)"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    player_center = (player_x + player_size // 2, player_y + player_size // 2)
    distance = ((player_center[0] - coin_x)**2 + (player_center[1] - coin_y)**2)**0.5

    if distance < player_size // 2 + coin_radius:
        score += 1
        coin_sound.play()
        if score >= max_score:
            running = False
        coin_x = random.randint(coin_radius, WIDTH - coin_radius)
        coin_y = random.randint(coin_radius, HEIGHT - coin_radius)

    screen.fill(WHITE)
    screen.blit(player_image, (player_x, player_y))
    pygame.draw.circle(screen, COIN_COLOR, (coin_x, coin_y), coin_radius)

    score_text = font.render(f"คะแนน: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if show_shop:
        shop_title = font.render("เมนูแลกของ: (กด 1 หรือ 2)", True, BLACK)
        option1 = font.render("1. เพิ่มความเร็ว (5 คะแนน)", True, BLACK)
        option2 = font.render("2. รับไอเทมพิเศษ (10 คะแนน)", True, BLACK)
        screen.blit(shop_title, (10, 50))
        screen.blit(option1, (10, 80))
        screen.blit(option2, (10, 110))
        if shop_message:
            msg = font.render(shop_message, True, (200, 0, 0))
            screen.blit(msg, (10, 150))

    pygame.display.flip()

screen.fill(WHITE)
end_text = font.render("คุณชนะแล้ว! คะแนนครบ 30", True, BLACK)
screen.blit(end_text, (100, HEIGHT // 2 - 20))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
sys.exit()
