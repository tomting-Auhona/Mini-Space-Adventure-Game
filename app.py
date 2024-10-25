import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Adventure")

# Function to load leaderboard from file
# Function to load leaderboard from file
def load_leaderboard():
    global leaderboard
    try:
        with open("leaderboard.txt", "r") as file:
            leaderboard = []
            for line in file:
                name, score = line.strip().split()
                leaderboard.append({'name': name, 'score': int(score)})
    except FileNotFoundError:
        leaderboard = []  # If file doesn't exist, start with an empty leaderboard

# Load leaderboard at the start
load_leaderboard()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw text on the screen
def draw_text(text, x, y, size=36, color=WHITE):
    font = pygame.font.Font(None, size)  # Use default pygame font
    text_surface = font.render(text, True, color)  # Create text surface
    screen.blit(text_surface, (x, y))  # Render the text onto the screen

# Function to ask for player name
def input_name():
    global player_name
    screen.fill(BLACK)
    draw_text("Enter Your Name:", 250, 250)
    pygame.display.update()

    input_active = True
    player_name = ""
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip() != "":
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(BLACK)
        draw_text("Enter Your Name:", 250, 250)
        draw_text(player_name, 250, 300)
        pygame.display.update()

# Function to show the instruction card
def show_instructions():
    screen.fill(BLACK)
    draw_text("Welcome to Space Adventure!", 150, 100, size=50)
    draw_text("Instructions:", 300, 200)
    draw_text("1. Use arrow keys to move your spaceship.", 200, 250)
    draw_text("2. Collect orbs for points and power-ups.", 200, 300)
    draw_text("3. Avoid asteroids and survive as long as you can.", 200, 350)
    draw_text("Press any key to start...", 250, 500)
    pygame.display.update()
    wait_for_key()

# Function to show the leaderboard
def show_leaderboard():
    screen.fill(BLACK)
    draw_text("Leaderboard", 250, 100, size=50)

    # Sort the leaderboard by score
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)

    y_offset = 200
    for i, entry in enumerate(sorted_leaderboard[:5]):  # Show top 5
        draw_text(f"{i + 1}. {entry['name']} - Score: {entry['score']}", 200, y_offset)
        y_offset += 50

    draw_text("Press any key to exit...", 250, 500)
    pygame.display.update()
    wait_for_key()

# Function to update the leaderboard
def update_leaderboard():
    global player_name, score
    leaderboard.append({'name': player_name, 'score': score})
    show_leaderboard()

# Function to save leaderboard to file
# Function to save leaderboard to file
def save_leaderboard():
    with open("leaderboard.txt", "w") as file:
        for entry in leaderboard:
            # Ensure the leaderboard data is saved correctly
            file.write(f"{entry['name']} {entry['score']}\n")

# Function to wait for key press after leaderboard is shown
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Function to check for collision between objects
def is_collision(x1, y1, x2, y2, size=50):
    return abs(x1 - x2) < size and abs(y1 - y2) < size

# Load background images
background = pygame.image.load('internship/bg1.png').convert()
background = pygame.transform.scale(background, (800, 600))

# Load spaceship, asteroid, egg, and orbs images
spaceship = pygame.image.load('internship/spaceship.png')
spaceship = pygame.transform.scale(spaceship, (64, 64))

asteroid_img = pygame.image.load('internship/ast1.png')
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))

egg_img = pygame.image.load('internship/egg.png')
egg_img = pygame.transform.scale(egg_img, (50, 50))

orb_red = pygame.image.load('internship/orb_red.png')
orb_red = pygame.transform.scale(orb_red, (40, 40))

orb_green = pygame.image.load('internship/orb_green_0.png')
orb_green = pygame.transform.scale(orb_green, (40, 40))

orb_purple = pygame.image.load('internship/orb_purple_0.png')
orb_purple = pygame.transform.scale(orb_purple, (40, 40))

# Initialize positions and velocities
spaceship_x = 400
spaceship_y = 500
spaceship_speed_x = 0
spaceship_speed_y = 0

asteroids = [{'x': random.randint(0, 740), 'y': -50, 'speed': random.randint(3, 6)} for _ in range(3)]
egg_x, egg_y = random.randint(0, 750), -50
egg_speed = 4

orbs = [
    {'img': orb_red, 'x': random.randint(0, 750), 'y': -50, 'speed': 4, 'type': 'points'},
    {'img': orb_green, 'x': random.randint(0, 750), 'y': -50, 'speed': 4, 'type': 'health'},
    {'img': orb_purple, 'x': random.randint(0, 750), 'y': -50, 'speed': 4, 'type': 'speed'}
]

# Set game variables
clock = pygame.time.Clock()
spaceship_health = 5
score = 0
orb_collected = False
speed_boost = False
speed_boost_timer = 0
player_name = ""

leaderboard = []

# Ask player for their name
input_name()

# Show the instruction card before the game starts
show_instructions()

# Function to show the restart button
# Function to show the restart button
def show_restart_button():
    screen.fill(BLACK)
    draw_text("Game Over!", 300, 150, size=50)
    draw_text("Click to Restart", 300, 300, size=36)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
                reset_game()

# Function to reset the game
def reset_game():
    global spaceship_health, score, spaceship_x, spaceship_y, asteroids, orb_collected, speed_boost, running
    spaceship_health = 5
    score = 0
    spaceship_x, spaceship_y = 400, 500
    asteroids = [{'x': random.randint(0, 740), 'y': -50, 'speed': random.randint(3, 6)} for _ in range(3)]
    orb_collected = False
    speed_boost = False
    running = True  # Ensure the game loop continues after resetting

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_speed_x = -5 if not speed_boost else -8
            if event.key == pygame.K_RIGHT:
                spaceship_speed_x = 5 if not speed_boost else 8
            if event.key == pygame.K_UP:
                spaceship_speed_y = -5 if not speed_boost else -8
            if event.key == pygame.K_DOWN:
                spaceship_speed_y = 5 if not speed_boost else 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_speed_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                spaceship_speed_y = 0

    # Update positions
    spaceship_x += spaceship_speed_x
    spaceship_y += spaceship_speed_y

    for asteroid in asteroids:
        asteroid['y'] += asteroid['speed']
        if asteroid['y'] > 600:
            asteroid['y'] = -50
            asteroid['x'] = random.randint(0, 740)

    # Check for collisions with asteroids
    for asteroid in asteroids:
        if is_collision(spaceship_x, spaceship_y, asteroid['x'], asteroid['y']):
            spaceship_health -= 1
            print(f"Collision! Health: {spaceship_health}")
            asteroid['y'] = -50  # Respawn the asteroid
            asteroid['x'] = random.randint(0, 740)

    if spaceship_health <= 0:
        print("Game Over!")
        update_leaderboard()
        save_leaderboard()  # Save the leaderboard to a file
        show_restart_button()
        continue

    # Draw background and spaceship
    screen.blit(background, (0, 0))

    # Move and check collisions with orbs
    for orb in orbs:
        orb['y'] += orb['speed']
        if orb['y'] > 600:
            orb['y'] = -50
            orb['x'] = random.randint(0, 750)
        screen.blit(orb['img'], (orb['x'], orb['y']))

        if is_collision(spaceship_x, spaceship_y, orb['x'], orb['y']):
            orb_collected = True
            if orb['type'] == 'points':
                score += 1
                print(f"Red orb collected! Score: {score}")
            elif orb['type'] == 'health':
                spaceship_health = min(spaceship_health + 1, 5)
                print(f"Green orb collected! Health: {spaceship_health}")
            elif orb['type'] == 'speed':
                speed_boost = True
                speed_boost_timer = pygame.time.get_ticks()
                print("Purple orb collected! Speed boost activated!")
            orb['y'] = -50  # Respawn orb

    # Handle speed boost timer
    if speed_boost and pygame.time.get_ticks() - speed_boost_timer > 5000:  # 5 seconds boost
        speed_boost = False
        print("Speed boost expired.")

    # Draw the spaceship
    screen.blit(spaceship, (spaceship_x, spaceship_y))

    # Draw the spaceship
    screen.blit(spaceship, (spaceship_x, spaceship_y))

    # Draw asteroids
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid['x'], asteroid['y']))

    # Display health, score, and level
    draw_text(f"Health: {spaceship_health}", 10, 10)
    draw_text(f"Score: {score}", 10, 50)

    # Update the screen
    pygame.display.update()
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()