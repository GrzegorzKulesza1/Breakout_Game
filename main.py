import pygame
import random

program_active, game_active = True, False
ball_dont_move = True
hit_red_brick = True
WIDTH, HEIGHT = 816, 600
points, hits_num = 0, 0
direction, speed = 0, 0


def display_score():
    score_surface = font40.render(f'Score: {points}', True, 'White')
    score_rect = score_surface.get_rect(topleft=(25, 11))
    screen.blit(score_surface, score_rect)

def display_bricks(active_bricks):
    for brick in active_bricks:
        index = active_bricks.index(brick)
        if index < 20:
            pygame.draw.rect(screen, 'Red', brick)
        elif index < 40:
            pygame.draw.rect(screen, 'Yellow', brick)
        else:
            pygame.draw.rect(screen, 'Green', brick)

def display_paddle():
    screen.blit(paddle_surface, paddle_rect)
    paddle_rect.center = (mouse_pos[0], 500)
    if paddle_rect.left <= 0:
        paddle_rect.left = 0
    elif paddle_rect.right >= WIDTH:
        paddle_rect.right = WIDTH

def display_ball(ball_obj):
    pygame.draw.circle(screen, 'Blue', ball_obj.center, 10)
    ball_obj = ball_obj.move(direction, speed)
    return ball_obj

def calculate_points(current_points):
    if brick_index < 20:
        current_points += 5
    elif brick_index < 40:
        current_points += 3
    else:
        current_points += 1
    return current_points


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()

# FONTS AND TEXTS
font30 = pygame.font.Font(None, 30)
font40 = pygame.font.Font(None, 40)
font120 = pygame.font.Font(None, 120)

game_name = font120.render("BREAKOUT", True, 'White', 'Black')
game_name_rect = game_name.get_rect(center=(WIDTH/2, 100))

start_surface = font40.render("Start", True, 'White', 'Black')
start_btn = start_surface.get_rect(center=(WIDTH / 2, 500))

exit_surface = font40.render("Exit", True, 'White', 'Black')
exit_btn = exit_surface.get_rect(center=(WIDTH / 2, 550))

text1 = font30.render("Breakout is an arcade game. The goal is to break all the blocks.",
                      True, 'White', 'Black')
text2 = font30.render("Bounce the ball off the paddle to do it. You can move your paddle", True, 'White', 'Black')
text3 = font30.render("using the mouse.", True, 'White', 'Black')
text1_rect = text1.get_rect(center=(400, 200))
text2_rect = text2.get_rect(center=(400, 230))
text3_rect = text3.get_rect(center=(400, 260))

text_ingame = font30.render('To start, press the left mouse button.', True, 'White', 'Black')
text_ingame_rect = text_ingame.get_rect(center=(400, 250))

win_game = font40.render("Congratulations, you broke all the bricks!", True, 'White', 'Black')
win_score = font40.render(f'Your score: 170', True, 'White', 'Black')
win_game_rect = win_game.get_rect(center=(400, 230))
win_score_rect = win_score.get_rect(center=(400, 270))

# STARTING BRICKS
starting_bricks = []
for i in range(50, 175, 25):
    for j in range(3, 813, 81):
        starting_bricks.append(pygame.Rect(j, i, 80, 20))
bricks = starting_bricks[:]

# PADDLE
paddle_surface = pygame.Surface((150, 10))
paddle_surface.fill('Grey')
paddle_rect = paddle_surface.get_rect(topleft=(300, 500))

# BALL
ball_rect = pygame.Rect(375, 500, 20, 20)

while program_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_active = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_btn_clicked = pygame.mouse.get_pressed()[0]

    if game_active:
        # hides cursor
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)

        screen.fill('Black')

        display_score()
        display_bricks(bricks)
        display_paddle()
        ball_rect = display_ball(ball_rect)

        # places the ball in the middle of the paddle
        if ball_dont_move:
            screen.blit(text_ingame, text_ingame_rect)
            ball_rect.midbottom = paddle_rect.midtop  # place the ball in the center of the paddle
            if mouse_btn_clicked:
                direction = random.randint(-6, 6)
                speed = -6
                ball_dont_move = False

        # CHECKS FOR COLLISIONS
        # with bricks
        if ball_rect.collidelist(bricks) != -1:
            brick_index = ball_rect.collidelist(bricks)
            # hides the hit brick on the screen
            bricks[brick_index] = pygame.Rect(bricks[brick_index][0], bricks[brick_index][1], 0, 0)
            speed *= -1

            points = calculate_points(points)
            if points == 170:
                game_active = False
                pygame.time.wait(100)

            # changes ball speed during the game
            hits_num += 1
            if hits_num == 4:
                speed += 2
            elif hits_num == 12:
                speed += 2
            elif brick_index < 20 and hit_red_brick:
                hit_red_brick = False
                speed += 2

        # collisions with paddle
        if ball_rect.colliderect(paddle_rect):
            # far right side of the paddle
            if -63 > paddle_rect.centerx - ball_rect.centerx:
                ball_rect.bottomleft = paddle_rect.topright
                direction = 4
            # far left side of the paddle
            elif 63 < paddle_rect.centerx - ball_rect.centerx:
                ball_rect.bottomright = paddle_rect.topleft
                direction = -4
            # right side of the paddle
            elif -6 > paddle_rect.centerx - ball_rect.centerx >= -63:
                direction = 2
            # left side of the paddle
            elif 6 < paddle_rect.centerx - ball_rect.centerx <= 63:
                direction = -2
            else:
                direction = 0
            speed *= -1

        # collisions with walls
        if ball_rect.left <= 0:
            ball_rect.left = 1
            direction *= -1
        elif ball_rect.right >= WIDTH:
            ball_rect.right = WIDTH - 1
            direction *= -1
        elif ball_rect.top <= 0:
            ball_rect.top = 1
            speed *= -1
        elif ball_rect.bottom >= HEIGHT:
            ball_rect.bottom = HEIGHT
            game_active = False
            pygame.time.wait(100)

    else:
        # shows cursor
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

        # shows constant menu items
        screen.fill("Black")
        screen.blit(game_name, game_name_rect)
        screen.blit(start_surface, start_btn)
        screen.blit(exit_surface, exit_btn)

        if points == 0:
            # description of the game
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)
        elif points == 170:
            # Player broke all the bricks
            screen.blit(win_game, win_game_rect)
            screen.blit(win_score, win_score_rect)
        else:
            # Standard score after game
            end_score = font40.render(f'Your score: {points}', True, 'White', 'Black')
            end_score_rect = end_score.get_rect(center=(400, 230))
            screen.blit(end_score, end_score_rect)

        # Checks if the player presses the start or exit button
        if start_btn.collidepoint(mouse_pos):
            pygame.draw.line(screen, 'White', start_btn.bottomleft, start_btn.bottomright, width=2)
            if mouse_btn_clicked:
                game_active, ball_dont_move = True, True
                points, hits_num = 0, 0
                direction, speed = 0, 0
                bricks = starting_bricks[:]
                pygame.time.wait(100)

        elif exit_btn.collidepoint(mouse_pos):
            pygame.draw.line(screen, 'White', exit_btn.bottomleft, exit_btn.bottomright, width=2)
            if mouse_btn_clicked:
                program_active = False
                pygame.time.wait(100)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
