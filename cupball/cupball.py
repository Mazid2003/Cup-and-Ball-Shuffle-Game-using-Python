import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 500
WHITE = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 149, 237)
BLACK = (0, 0, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cup and Ball Game")

# Load images
cup_img = pygame.image.load("cup1.png")  
cup_img = pygame.transform.scale(cup_img, (100, 150))
ball_img = pygame.image.load("ball1.png")  
ball_img = pygame.transform.scale(ball_img, (40, 40))

# Cup positions
original_positions = [(200, 200), (350, 200), (500, 200)]
cup_positions = original_positions[:]
cup_mapping = [0, 1, 2]  # Tracks which cup is where
ball_cup = random.randint(0, 2)  # Ball starts under a random cup
revealed = False
game_over = False

# Button dimensions
button_rect = pygame.Rect(300, 400, 200, 50)

# Title Font
title_font = pygame.font.Font(None, 50)

# Function to animate cup swapping
def swap_cups(idx1, idx2):
    """Swaps two cups smoothly by animating their movement."""
    global ball_cup

    steps = 20  # Animation steps
    dx1 = (cup_positions[idx2][0] - cup_positions[idx1][0]) // steps
    dx2 = (cup_positions[idx1][0] - cup_positions[idx2][0]) // steps

    for step in range(steps):
        screen.fill(WHITE)
        draw_title()

        # Animate the movement of swapping cups
        for i in range(3):
            if i == idx1:
                new_pos1 = (cup_positions[idx1][0] + dx1 * step, cup_positions[idx1][1])
                screen.blit(cup_img, new_pos1)
            elif i == idx2:
                new_pos2 = (cup_positions[idx2][0] + dx2 * step, cup_positions[idx2][1])
                screen.blit(cup_img, new_pos2)
            else:
                screen.blit(cup_img, cup_positions[i])

        pygame.display.update()
        pygame.time.delay(30)

    # Swap cup positions
    cup_positions[idx1], cup_positions[idx2] = cup_positions[idx2], cup_positions[idx1]

    # Swap cup mapping
    cup_mapping[idx1], cup_mapping[idx2] = cup_mapping[idx2], cup_mapping[idx1]

    # Update ball's new position
    if ball_cup == idx1:
        ball_cup = idx2
    elif ball_cup == idx2:
        ball_cup = idx1

# Function to shuffle cups
def shuffle_cups():
    pygame.time.delay(500)  # Pause before shuffling
    num_swaps = 5  # Number of swaps
    for _ in range(num_swaps):
        idx1, idx2 = random.sample(range(3), 2)  # Pick two cups
        swap_cups(idx1, idx2)  # Swap them

# Function to draw title
def draw_title():
    title_text = title_font.render("Find the Ball Under the Cup!", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

# Function to draw game elements
def draw_game():
    screen.fill(WHITE)
    draw_title()

    # Draw cups
    for i, pos in enumerate(cup_positions):
        screen.blit(cup_img, pos)
        if revealed and i == ball_cup:
            screen.blit(ball_img, (pos[0] + 30, pos[1] + 100))  # Show ball under cup

    # Draw restart button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_color = HOVER_COLOR if button_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

    font = pygame.font.Font(None, 36)
    text = font.render("Restart Game", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.update()

# Function to restart game
def restart_game():
    global ball_cup, revealed, cup_positions, game_over, cup_mapping
    ball_cup = random.randint(0, 2)  # Reset ball under a random cup
    cup_positions = original_positions[:]  # Reset cup positions
    cup_mapping = [0, 1, 2]  # Reset logical mapping
    revealed = True  # Show ball before shuffling
    draw_game()
    pygame.time.delay(500)
    revealed = False
    game_over = False  # Reset game state
    shuffle_cups()  # Start shuffling

# Main game loop
running = True
while running:
    draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_rect.collidepoint(x, y) and game_over:
                restart_game()

            if game_over:
                continue

            # Check if a cup is clicked
            for i, pos in enumerate(cup_positions):
                if pos[0] < x < pos[0] + 100 and pos[1] < y < pos[1] + 150:
                    revealed = True
                    draw_game()
                    pygame.time.delay(1000)
                    if i == ball_cup:
                        print("🎉 Correct! You found the ball!")
                    else:
                        print(f"❌ Wrong! The ball was under cup {cup_positions.index(cup_positions[ball_cup]) + 1}.")
                    pygame.time.delay(2000)
                    game_over = True  # Now user must restart to play again

pygame.quit()
