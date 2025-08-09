import pygame, sys, random, math

# Global setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Hub")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def transition_effect(text="Loading", duration=1200):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    start = pygame.time.get_ticks()
    dot_count = 0

    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start
        alpha = min(255, int(255 * (elapsed / duration)))
        fade.set_alpha(alpha)

        # Animate dots: "Loading.", "Loading..", "Loading..."
        if elapsed % 500 < 100:
            dot_count = (dot_count + 1) % 4
        dots = "." * dot_count

        screen.fill((20, 20, 30))
        loading_text = font.render(f"{text}{dots}", True, (255, 255, 255))
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(fade, (0, 0))

        pygame.display.flip()
        if elapsed >= duration:
            break
        clock.tick(60)
# -------- Snake Game --------
def run_snake():
    BLOCK = 20
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (BLOCK, 0)
    apple = (random.randint(0, WIDTH//BLOCK - 1)*BLOCK, random.randint(0, HEIGHT//BLOCK - 1)*BLOCK)
    score = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: direction = (0, -BLOCK)
                elif e.key == pygame.K_DOWN: direction = (0, BLOCK)
                elif e.key == pygame.K_LEFT: direction = (-BLOCK, 0)
                elif e.key == pygame.K_RIGHT: direction = (BLOCK, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if head in snake or not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT): return
        snake.insert(0, head)
        if head == apple:
            score += 1
            apple = (random.randint(0, WIDTH//BLOCK - 1)*BLOCK, random.randint(0, HEIGHT//BLOCK - 1)*BLOCK)
        else:
            snake.pop()

        pygame.draw.rect(screen, (255,0,0), (*apple, BLOCK, BLOCK))
        for s in snake: pygame.draw.rect(screen, (0,255,0), (*s, BLOCK, BLOCK))
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()
        clock.tick(10)

# -------- Dodge Game --------
def run_dodge():
    player = pygame.Rect(WIDTH//2, HEIGHT-50, 40, 40)
    blocks = [pygame.Rect(random.randint(0, WIDTH-30), -60*i, 30, 30) for i in range(10)]
    speed = 5
    score = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0: player.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH: player.move_ip(5, 0)

        for b in blocks:
            b.move_ip(0, speed)
            if b.colliderect(player): return
            if b.top > HEIGHT:
                b.y = -30
                b.x = random.randint(0, WIDTH - b.width)
                score += 1

        pygame.draw.rect(screen, (0,255,0), player)
        for b in blocks: pygame.draw.rect(screen, (255,0,0), b)
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()
        clock.tick(60)

# -------- Main Menu --------
def main_menu():
    WIDTH, HEIGHT = 800, 600
    running = True
    games = [("Snake", run_snake), ("Dodge", run_dodge), ("Flapy", run_flappy), ("Break out", run_breakout), ("Pong", run_pong), ("Memory", run_memory), ("Clicker", run_clicker), ("Asteroids", run_asteroids), ("Quess the number", run_guess_the_number), ("Geometry dash", run_geometry_dash)]  # Add more as we go
    selected_index = 0
    visible_limit = 6
    scroll_offset = 0

    # Background animation
    background_shapes = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(40)]

    while True:
        # Glowing background color
        ticks = pygame.time.get_ticks()
        r = 20 + int(20 * math.sin(ticks * 0.002))
        g = 20 + int(20 * math.sin(ticks * 0.004))
        b = 30 + int(20 * math.sin(ticks * 0.003))
        screen.fill((r, g, b))

        # Floating cube animation
        for shape in background_shapes:
            shape[0] -= 1
            if shape[0] < -20:
                shape[0] = WIDTH + random.randint(0, 100)
                shape[1] = random.randint(0, HEIGHT - 20)
            pygame.draw.rect(screen, (50, 255, 255), pygame.Rect(shape[0], shape[1], 20, 20))

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_index > 0:
                        selected_index -= 1
                        if selected_index < scroll_offset:
                            scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    if selected_index < len(games) - 1:
                        selected_index += 1
                        if selected_index >= scroll_offset + visible_limit:
                            scroll_offset += 1
                elif event.key == pygame.K_RETURN:
                    name, func = games[selected_index]
                    transition_effect(f"Loading {name}")
                    func()

        # Draw menu items
        for i in range(visible_limit):
            idx = scroll_offset + i
            if idx >= len(games):
                break
            name, _ = games[idx]
            y = 120 + i * 60
            rect = pygame.Rect(200, y, 400, 50)
            is_selected = idx == selected_index
            color = (0, 200, 255) if is_selected else (80, 80, 120)
            pygame.draw.rect(screen, color, rect)
            label = font.render(name, True, (255, 255, 255))
            screen.blit(label, (rect.x + 20, rect.y + 10))

        # Scrollbar indicator
        info = font.render(f"{selected_index + 1}/{len(games)}", True, (180, 180, 200))
        screen.blit(info, (WIDTH - 120, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)

def run_flappy():
    bird = pygame.Rect(100, HEIGHT//2, 30, 30)
    gravity = 0
    pipes = []
    pipe_timer = 0
    score = 0
    running = True

    while running:
        screen.fill((135, 206, 235))
        gravity += 1
        bird.y += gravity // 3

        pipe_timer += 1
        if pipe_timer > 60:
            h = random.randint(100, 400)
            pipes.append(pygame.Rect(WIDTH, 0, 50, h))
            pipes.append(pygame.Rect(WIDTH, h + 150, 50, HEIGHT - h - 150))
            pipe_timer = 0

        for p in pipes:
            p.x -= 5
            if p.colliderect(bird): return

        pipes = [p for p in pipes if p.x > -50]
        score += 0.01

        pygame.draw.rect(screen, (255, 255, 0), bird)
        for p in pipes: pygame.draw.rect(screen, (0, 255, 0), p)

        score_text = font.render(f"Score: {int(score)}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: gravity = -25

        clock.tick(60)
def run_breakout():
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, 15, 15)
    paddle = pygame.Rect(WIDTH//2 - 60, HEIGHT - 30, 120, 10)
    blocks = [pygame.Rect(x * 60 + 20, y * 20 + 40, 50, 15) for x in range(13) for y in range(5)]
    dx, dy = 4, -4
    running = True
    score = 0

    while running:
        screen.fill((0, 0, 0))
        ball.x += dx
        ball.y += dy

        if ball.left <= 0 or ball.right >= WIDTH: dx *= -1
        if ball.top <= 0: dy *= -1
        if ball.bottom >= HEIGHT: return

        if ball.colliderect(paddle): dy *= -1
        for block in blocks[:]:
            if ball.colliderect(block):
                blocks.remove(block)
                dy *= -1
                score += 1
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0: paddle.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH: paddle.move_ip(6, 0)

        pygame.draw.rect(screen, (255, 255, 255), ball)
        pygame.draw.rect(screen, (200, 200, 200), paddle)
        for block in blocks:
            pygame.draw.rect(screen, (255, 0, 0), block)

        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return

        clock.tick(60)
def run_pong():
    WIDTH, HEIGHT = 800, 600
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    BALL_RADIUS = 10
    PADDLE_SPEED = 6
    WINNING_SCORE = 10

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)
    win_font = pygame.font.Font(None, 72)
    menu_font = pygame.font.Font(None, 48)
    clock = pygame.time.Clock()

    def reset_ball(ball, ball_speed):
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed[0] = 5 * random.choice((1, -1))
        ball_speed[1] = 5 * random.choice((1, -1))

    def display_winner(text):
        win_text = win_font.render(text, True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    def difficulty_menu():
        while True:
            screen.fill(BLACK)
            options = [
                ("1. Easy", 3),
                ("2. Medium", 5),
                ("3. Hard", 7),
                ("4. Impossible", 10)
            ]
            title = win_font.render("Select AI Difficulty", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
            for i, (label, _) in enumerate(options):
                txt = menu_font.render(label, True, WHITE)
                screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 + i * 50 - 40))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        return options[event.key - pygame.K_1][1]

    def mode_menu():
        while True:
            screen.fill(BLACK)
            title = win_font.render("PONG", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
            single = menu_font.render("1. Single Player", True, WHITE)
            two = menu_font.render("2. Two Player", True, WHITE)
            screen.blit(single, (WIDTH // 2 - single.get_width() // 2, HEIGHT // 2))
            screen.blit(two, (WIDTH // 2 - two.get_width() // 2, HEIGHT // 2 + 60))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None, None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        ai_speed = difficulty_menu()
                        return True, ai_speed
                    elif event.key == pygame.K_2:
                        return False, 0

    def game_loop(single_player, ai_speed):
        player1 = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        player2 = pygame.Rect(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        ball_speed = [5 * random.choice((1, -1)), 5 * random.choice((1, -1))]
        score1, score2 = 0, 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1.top > 0: player1.y -= PADDLE_SPEED
            if keys[pygame.K_s] and player1.bottom < HEIGHT: player1.y += PADDLE_SPEED

            if single_player:
                if ball.centery > player2.centery and player2.bottom < HEIGHT:
                    player2.y += ai_speed
                elif ball.centery < player2.centery and player2.top > 0:
                    player2.y -= ai_speed
            else:
                if keys[pygame.K_UP] and player2.top > 0: player2.y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and player2.bottom < HEIGHT: player2.y += PADDLE_SPEED

            ball.x += ball_speed[0]
            ball.y += ball_speed[1]

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed[1] *= -1

            if ball.colliderect(player1) or ball.colliderect(player2):
                ball_speed[0] *= -1.1
                ball_speed[1] *= 1.1

            if ball.left <= 0:
                score2 += 1
                reset_ball(ball, ball_speed)
            elif ball.right >= WIDTH:
                score1 += 1
                reset_ball(ball, ball_speed)

            if score1 >= WINNING_SCORE:
                display_winner("Player 1 Wins!")
                return
            elif score2 >= WINNING_SCORE:
                winner = "Computer Wins!" if single_player else "Player 2 Wins!"
                display_winner(winner)
                return

            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, player1)
            pygame.draw.rect(screen, WHITE, player2)
            pygame.draw.ellipse(screen, WHITE, ball)
            pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

            score_text1 = font.render(str(score1), True, WHITE)
            score_text2 = font.render(str(score2), True, WHITE)
            screen.blit(score_text1, (WIDTH//2 - 50, 20))
            screen.blit(score_text2, (WIDTH//2 + 30, 20))

            pygame.display.flip()
            clock.tick(60)

    single, ai_speed = mode_menu()
    if single is not None:
        game_loop(single, ai_speed)
def run_memory():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ROWS, COLS = 4, 4
    CARD_SIZE = 100
    GAP = 20

    # Grid layout
    grid_width = COLS * CARD_SIZE + (COLS - 1) * GAP
    grid_height = ROWS * CARD_SIZE + (ROWS - 1) * GAP
    start_x = (WIDTH - grid_width) // 2
    start_y = (HEIGHT - grid_height) // 2

    # Create card positions
    card_positions = []
    for row in range(ROWS):
        for col in range(COLS):
            x = start_x + col * (CARD_SIZE + GAP)
            y = start_y + row * (CARD_SIZE + GAP)
            card_positions.append(pygame.Rect(x, y, CARD_SIZE, CARD_SIZE))

    # Create card values (2 of each)
    values = list(range(1, (ROWS * COLS) // 2 + 1)) * 2
    random.shuffle(values)
    revealed = [False] * len(values)
    matched = [False] * len(values)
    selection = []

    # Main loop
    while True:
        screen.fill((20, 20, 30))
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        for i, rect in enumerate(card_positions):
            if rect.collidepoint((mx, my)) and click and not revealed[i] and not matched[i]:
                revealed[i] = True
                selection.append(i)
                if len(selection) == 2:
                    pygame.time.wait(600)
                    a, b = selection
                    if values[a] == values[b]:
                        matched[a] = matched[b] = True
                    else:
                        revealed[a] = revealed[b] = False
                    selection = []

        for i, rect in enumerate(card_positions):
            color = (100, 100, 255) if not revealed[i] else (0, 200, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255,255,255), rect, 2)
            if revealed[i] or matched[i]:
                txt = font.render(str(values[i]), True, (255, 255, 255))
                screen.blit(txt, (rect.x + CARD_SIZE//2 - txt.get_width()//2,
                                  rect.y + CARD_SIZE//2 - txt.get_height()//2))

        pygame.display.flip()
        clock.tick(60)
def run_clicker():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Game state
    money = 0
    click_value = 1
    click_upgrade_cost = 50
    auto_clickers = 0
    auto_clicker_cost = 100
    last_auto_click = 0

    while True:
        screen.fill((20, 20, 30))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # Mouse click position
                if click_zone.collidepoint((mx, my)):
                    money += click_value
                elif click_upgrade_btn.collidepoint((mx, my)) and money >= click_upgrade_cost:
                    money -= click_upgrade_cost
                    click_value += 1
                    click_upgrade_cost = int(click_upgrade_cost * 1.5)
                elif auto_clicker_btn.collidepoint((mx, my)) and money >= auto_clicker_cost:
                    money -= auto_clicker_cost
                    auto_clickers += 1
                    auto_clicker_cost = int(auto_clicker_cost * 1.5)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return

        # Click money zone
        click_zone = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 100)


        # Upgrade: click value
        click_upgrade_btn = pygame.Rect(50, 100, 240, 60)
        

        # Upgrade: auto-clicker
        auto_clicker_btn = pygame.Rect(50, 180, 240, 60)
        

        # Auto-click income
        now = pygame.time.get_ticks()
        if now - last_auto_click >= 1000:
            money += auto_clickers
            last_auto_click = now

        # UI Drawing
        pygame.draw.rect(screen, (0, 200, 255), click_zone)
        screen.blit(font.render("CLICK", True, (255, 255, 255)), (click_zone.x + 50, click_zone.y + 35))

        pygame.draw.rect(screen, (50, 50, 100), click_upgrade_btn)
        screen.blit(font.render(f"Upgrade Click (${click_upgrade_cost})", True, (255,255,255)), (click_upgrade_btn.x + 10, click_upgrade_btn.y + 10))

        pygame.draw.rect(screen, (50, 100, 50), auto_clicker_btn)
        screen.blit(font.render(f"Auto-Clicker (${auto_clicker_cost})", True, (255,255,255)), (auto_clicker_btn.x + 10, auto_clicker_btn.y + 10))

        screen.blit(font.render(f"Money: ${money}", True, (255,255,255)), (50, 40))
        screen.blit(font.render(f"Click Power: +{click_value}", True, (255,255,255)), (50, 320))
        screen.blit(font.render(f"Auto-Clickers: {auto_clickers}", True, (255,255,255)), (50, 360))

        pygame.display.flip()
        clock.tick(60)

def run_asteroids():
    player = pygame.Rect(WIDTH//2, HEIGHT - 50, 30, 30)
    asteroids = [pygame.Rect(random.randint(0, WIDTH-30), -60*i, 30, 30) for i in range(10)]
    score = 0
    while True:
        screen.fill((10, 10, 20))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0: player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += 5
        for a in asteroids:
            a.y += 4
            if a.colliderect(player): return
            if a.top > HEIGHT:
                a.y = -30
                a.x = random.randint(0, WIDTH - 30)
                score += 1
        pygame.draw.rect(screen, (0, 200, 200), player)
        for a in asteroids: pygame.draw.rect(screen, (200, 200, 0), a)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        pygame.display.flip()
        for e in pygame.event.get(): 
            if e.type == pygame.QUIT: return
        clock.tick(60)
def run_guess_the_number():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Guess the Number")
    font = pygame.font.Font(None, 48)
    input_font = pygame.font.Font(None, 36)

    target = random.randint(1, 100)
    guess = ""
    result = "Enter a number between 1 and 100"
    color = (255, 255, 255)
    active = True
    play_again = False

    button = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 60, 160, 40)

    while True:
        screen.fill((20, 20, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if guess.isdigit():
                        num = int(guess)
                        if num < target:
                            result = "Too low!"
                        elif num > target:
                            result = "Too high!"
                        else:
                            result = "Correct! 🎉"
                            color = (0, 255, 0)
                            active = False
                            play_again = True
                    else:
                        result = "Enter digits only!"
                    guess = ""
                elif event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                else:
                    if len(guess) < 3:
                        guess += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and play_again:
                if button.collidepoint(event.pos):
                    target = random.randint(1, 100)
                    result = "Enter a number between 1 and 100"
                    color = (255, 255, 255)
                    active = True
                    play_again = False
                    guess = ""

        txt_box = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 - 30, 160, 40)
        pygame.draw.rect(screen, color, txt_box, 2)
        txt_surface = input_font.render(guess, True, color)
        screen.blit(txt_surface, (txt_box.x + 10, txt_box.y + 5))

        result_msg = font.render(result, True, color)
        screen.blit(result_msg, (WIDTH//2 - result_msg.get_width()//2, HEIGHT//2 - 100))

        if play_again:
            pygame.draw.rect(screen, (0, 150, 150), button)
            btn_text = input_font.render("Play Again", True, (255, 255, 255))
            screen.blit(btn_text, (button.x + 20, button.y + 5))

        pygame.display.flip()
        clock.tick(30)
def run_geometry_dash():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    player = pygame.Rect(100, HEIGHT - 80, 40, 40)
    velocity_y = 0
    gravity = 0.8
    jump_force = -12

    scroll_x = 0
    score = 0
    level_length = 5000

    ground_height = 40
    ground_y = HEIGHT - ground_height

    blocks = []
    floor_spikes = []
    platform_spikes = []
    spawn_timer = 0
    win = False

    def spawn_block(x):
        y = random.choice([ground_y - 60, ground_y - 80])  # Reachable only
        return pygame.Rect(x, y, 80, 20)

    def spawn_floor_spike(x):
        return pygame.Rect(x, ground_y - 30, 30, 30)

    def spawn_platform_spike(block):
        # Spawns directly on the ground, same x as block
        return pygame.Rect(block.x + 25, ground_y - 30, 30, 30)

    while True:
        screen.fill((30, 30, 30))

        if win:
            msg = font.render("Level Complete!", True, (0, 255, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and velocity_y == 0:
                    velocity_y = jump_force

        spawn_timer += 1
        if spawn_timer > 60:
            x = WIDTH + scroll_x
            r = random.random()
            if r < 0.6:
                block = spawn_block(x)
                blocks.append(block)
                # Add a spike below the platform at ground level
                platform_spikes.append(spawn_platform_spike(block))
            elif r < 0.85:
                floor_spikes.append(spawn_floor_spike(x))
            spawn_timer = 0

        velocity_y += gravity
        player.y += velocity_y

        safe_landing = False
        for block in blocks:
            bx = block.x - scroll_x
            block_screen = pygame.Rect(bx, block.y, block.width, block.height)
            if player.colliderect(block_screen):
                if velocity_y > 0 and player.bottom <= block.y + 10:
                    player.bottom = block.y
                    velocity_y = 0
                    safe_landing = True
                else:
                    return

        if player.bottom >= ground_y and not safe_landing:
            player.bottom = ground_y
            velocity_y = 0

        for spike in floor_spikes + platform_spikes:
            sx = spike.x - scroll_x
            hitbox = pygame.Rect(sx, spike.y, spike.width, spike.height)
            if hitbox.colliderect(player):
                return

        scroll_x += 6
        score += 1
        if scroll_x > level_length:
            win = True

        pygame.draw.rect(screen, (0, 255, 255), player)
        pygame.draw.rect(screen, (100, 100, 100), (0, ground_y, WIDTH, ground_height))
        screen.blit(font.render(f"Distance: {score}", True, (255, 255, 255)), (10, 10))

        for block in blocks:
            bx = block.x - scroll_x
            if -80 < bx < WIDTH:
                pygame.draw.rect(screen, (150, 150, 150), (bx, block.y, block.width, block.height))

        for spike in floor_spikes + platform_spikes:
            sx = spike.x - scroll_x
            if -30 < sx < WIDTH:
                pygame.draw.polygon(screen, (255, 50, 50), [
                    (sx, spike.bottom),
                    (sx + spike.width // 2, spike.top),
                    (sx + spike.width, spike.bottom)
                ])

        pygame.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main_menu()
