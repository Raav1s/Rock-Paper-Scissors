import pygame
import sys
import math
import random
import time

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock-Paper-Scissors Game")

button_width = 70
button_height = 40


# Define the new width and height
new_width = 100
new_height = 100


# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
# Define gradient colors
gradient_color_top = (135, 206, 250)  # Light blue (#87CEFA)
gradient_color_bottom = (0, 191, 255)  # Deep sky blue (#00BFFF)

# Set up clock
clock = pygame.time.Clock() #управления частотой обновления экрана или игрового цикла.

# Загружаем музыкальный файл
pygame.mixer.music.load('3d20874f20174bd.mp3')

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

# Function to simulate loading
def simulate_loading():
    total_steps = 100
    for i in range(total_steps):
        # Simulate loading by sleeping for a short duration
        pygame.time.delay(20)  # Decreased delay for faster movement
        # Calculate progress percentage
        progress = i / total_steps
        # Draw loading screen
        draw_loading_screen(progress)
        pygame.display.flip()

# Function to draw loading screen
def draw_loading_screen(progress):
    # Create gradient background
    for y in range(height):
        # Interpolate between gradient colors based on progress
        r = int(gradient_color_top[0] + (gradient_color_bottom[0] - gradient_color_top[0]) * progress)
        g = int(gradient_color_top[1] + (gradient_color_bottom[1] - gradient_color_top[1]) * progress)
        b = int(gradient_color_top[2] + (gradient_color_bottom[2] - gradient_color_top[2]) * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    # Draw game title with sinusoidal motion for each letter
    font = pygame.font.SysFont("arialblack", 35)
    text = "Rock-Paper-Scissors"
    text_width, text_height = font.size(text)
    amplitude = 10  # Amplitude of sinusoidal motion
    frequency = 0.05  # Frequency of sinusoidal motion
    for i, char in enumerate(text):
        angle = progress * 2 * math.pi + (i * 2 * math.pi) / len(text)
        displacement = amplitude * math.sin(angle)
        letter_render = font.render(char, True, black)
        screen.blit(letter_render, (width // 2.1 - text_width // 2 + i * 25, height // 2.6 + displacement))
    # Draw loading bar with gradient color
    bar_width = width // 2
    bar_height = 30
    bar_x = (width - bar_width) // 2
    bar_y = height // 2
    gradient_color_bottom1 = (255,229,141)
    gradient_color_top1 = (255,229,180)
    # Draw the loading bar with a gradient color
    for x in range(bar_x, int(bar_x + progress * bar_width)):
        # Interpolate between gradient colors based on progress
        r = int(gradient_color_bottom1[0] + (gradient_color_top1[0] - gradient_color_bottom1[0]) * progress)
        g = int(gradient_color_bottom1[1] + (gradient_color_top1[1] - gradient_color_bottom1[1]) * progress)
        b = int(gradient_color_bottom1[2] + (gradient_color_top1[2] - gradient_color_bottom1[2]) * progress)
        pygame.draw.line(screen, (r, g, b), (x, bar_y), (x, bar_y + bar_height))

# Function to display "PLAY" button
def show_play_button():
    screen.fill((0, 191, 255))  # Set background to deep sky blue
    font = pygame.font.SysFont("arialblack", 50)
    text = font.render("PLAY", True, (0, 0, 0))  # Render "PLAY" text in white color
    text_rect = text.get_rect(center=(width // 2, height // 2))  # Position text in the center of the screen
    screen.blit(text, text_rect)
    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(highlight_offset, highlight_offset),4)
    pygame.display.flip()

def exit_from_button_play():
    exit_play = True
    while exit_play:
        show_play_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 50 < mouse_pos[0] < width // 2 + 50 and height // 2 - 35 < mouse_pos[1] < height // 2 + 35:
                    # If mouse clicked on "PLAY" button
                    exit_play = False

def show_game_mode_buttons():
    screen.fill((0, 191, 255))  # Set background to deep sky blue
    font = pygame.font.SysFont("arialblack", 35)
    text_1_gamemode = font.render("GAMEMODE", True, (0, 0, 0))
    text_3_option = font.render("SETTING", True, (0, 0, 0))
    text_4_exit = font.render("EXIT", True, (0, 0, 0))
    text_rect_1_gamemode = text_1_gamemode.get_rect(center=(width // 2, height // 2 - 60))
    text_rect_3_option = text_3_option.get_rect(center=(width // 2, height // 2))
    text_rect_4_exit = text_4_exit.get_rect(center=(width // 2, height // 2 + 60))
    screen.blit(text_1_gamemode, text_rect_1_gamemode)
    screen.blit(text_3_option, text_rect_3_option)
    screen.blit(text_4_exit, text_rect_4_exit)
    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_1_gamemode.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_1_gamemode.inflate(highlight_offset, highlight_offset),4)
    if text_rect_3_option.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_3_option.inflate(highlight_offset, highlight_offset),4)
    if text_rect_4_exit.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_4_exit.inflate(highlight_offset, highlight_offset),4)
    pygame.display.flip()

# Variable to track whether music is currently playing
music_playing = True

# Function to toggle music
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()  # Pause music if currently playing
    else:
        pygame.mixer.music.unpause()  # Unpause music if currently paused
    music_playing = not music_playing  # Toggle music state




def setting_buttons():
    global music_playing, key_mappings
    screen.fill((0, 191, 255))  # Set background to deep sky blue
    font = pygame.font.SysFont("arialblack", 35)
    font2 = pygame.font.SysFont("arialblack", 25)
    text_1_audio = font.render("AUDIO", True, (0, 0, 0))
    text_4_keybindings = font.render("KEY BINDINGS", True, (0, 0, 0))
    text_5_back = font.render("BACK", True, (0, 0, 0))
    text_rect_1_audio = text_1_audio.get_rect(center=(width // 2, height // 2 - 100))
    text_rect_4_keybindings = text_4_keybindings.get_rect(center=(width // 2, height // 2))
    text_rect_5_back = text_5_back.get_rect(center=(width // 2, height // 2 + 100))

    # # Render current key bindings
    # key_bindings_text = font2.render(f"R: {pygame.key.name(key_mappings['Rock'])}, "
    #                                  f"P: {pygame.key.name(key_mappings['Paper'])}, "
    #                                  f"S: {pygame.key.name(key_mappings['Scissors'])}", True, (0, 0, 0))
    # text_rect_keybindings = key_bindings_text.get_rect(center=(width // 2, height // 2 + 40))

    # Render "ON" button text in gray if music is already playing
    if music_playing:
        text_2_on = font2.render("ON", True, (128, 128, 128))
    else:
        text_2_on = font2.render("ON", True, (0, 0, 0))
    text_rect_2_on = text_2_on.get_rect(center=(width // 2 - 50, height // 2 - 60))  # Position "ON" button

    # Render "OFF" button text in gray if music is paused
    if not music_playing:
        text_3_off = font2.render("OFF", True, (128, 128, 128))
    else:
        text_3_off = font2.render("OFF", True, (0, 0, 0))
    text_rect_3_off = text_3_off.get_rect(center=(width // 2 + 50, height // 2 - 60))  # Position "OFF" button

    screen.blit(text_1_audio, text_rect_1_audio)
    screen.blit(text_2_on, text_rect_2_on)
    screen.blit(text_3_off, text_rect_3_off)
    screen.blit(text_4_keybindings, text_rect_4_keybindings)
    # screen.blit(key_bindings_text, text_rect_keybindings)
    screen.blit(text_5_back, text_rect_5_back)

    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_2_on.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_2_on.inflate(highlight_offset, highlight_offset), 4)
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
            pygame.mixer.music.unpause()  # Unpause music when "ON" button is clicked
            music_playing = True
    if text_rect_3_off.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_3_off.inflate(highlight_offset, highlight_offset), 4)
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
            pygame.mixer.music.pause()  # Pause music when "OFF" button is clicked
            music_playing = False
    if text_rect_5_back.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_5_back.inflate(highlight_offset, highlight_offset), 4)

    # Check for key press to change key bindings
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                key_mappings['Rock'] = event.key
            elif event.key == pygame.K_p:
                key_mappings['Paper'] = event.key
            elif event.key == pygame.K_s:
                key_mappings['Scissors'] = event.key
    pygame.display.flip()


def exit_setting_buttons():
    exit_setting = True
    while exit_setting:
        setting_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100:
                    if height // 2 + 70 < mouse_pos[1] < height // 2 + 160:  # Adjusted y-coordinates for "Back" button
                        # If mouse clicked on "Back" button
                        exit_with_gamemode_setting_exit()

def exit_with_gamemode_setting_exit():
    exit_gamemode = True
    while exit_gamemode:
        show_game_mode_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 85 < mouse_pos[1] < height // 2 - 35:
                    # If mouse clicked on "GAMEMODE" button
                    exit_1_2_players_back()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 25 < mouse_pos[1] < height // 2+25:
                    exit_setting_buttons()
                elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 + 35 < mouse_pos[1] < height // 2 + 85:
                    pygame.quit()
                    sys.exit()


def gamemode():
    screen.fill((0, 191, 255))  # Set background to deep sky blue
    font = pygame.font.SysFont("arialblack", 35)
    text_1_player = font.render("1PLAYER", True, (0, 0, 0))  # Render "1 Player" text in white color
    text_2_players = font.render("2PLAYERS", True, (0, 0, 0))# Render "2 Players" text in white color
    text_3_back = font.render("BACK", True, (0, 0, 0))
    text_rect_1_player = text_1_player.get_rect(center=(width // 2, height // 2 - 60))  # Position "1 Player" button
    text_rect_2_players = text_2_players.get_rect(center=(width // 2, height // 2))  # Position "2 Players" button
    text_rect_3_back = text_3_back.get_rect(center=(width // 2, height // 2 + 60))
    screen.blit(text_1_player, text_rect_1_player)
    screen.blit(text_2_players, text_rect_2_players)
    screen.blit(text_3_back, text_rect_3_back)
    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_1_player.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_1_player.inflate(highlight_offset, highlight_offset), 4)  # Highlight "1 PLAYER" button
    if text_rect_2_players.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_2_players.inflate(highlight_offset, highlight_offset), 4)  # Highlight "2 PLAYERS" button
    if text_rect_3_back.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_3_back.inflate(highlight_offset, highlight_offset),4)  # Highlight "BACK" button
    pygame.display.flip()

def exit_1_2_players_back():
    exit_players = True
    while exit_players:
        gamemode()  # Call the gamemode function to display game mode options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100:
                    if height // 2 - 85 < mouse_pos[1] < height // 2 - 35:  # Adjusted y-coordinates for "1 Player" button
                        # If mouse clicked on "1 Player" button
                        screen.fill((0, 191, 255))
                        handle_one_player_mode()
                    elif height // 2 - 25 < mouse_pos[1] < height // 2 + 25:  # Adjusted y-coordinates for "2 Players" button
                        # If mouse clicked on "2 Players" button
                        handle_two_players_mode()
                        screen.fill((0, 191, 255))
                    elif height // 2 + 35 < mouse_pos[1] < height // 2 + 85:  # Adjusted y-coordinates for "Back" button
                        # If mouse clicked on "Back" button
                        exit_with_gamemode_setting_exit()
                        screen.fill((0, 191, 255))

# Define default key mappings
key_mappings = {
    "Rock": pygame.K_a,
    "Paper": pygame.K_s,
    "Scissors": pygame.K_d
}

key_mappings2 = {
    "Scissors": pygame.K_j,
    "Paper": pygame.K_k,
    "Rock": pygame.K_l
}


def handle_one_player_mode_buttons():
    font = pygame.font.SysFont("arialblack", 30)
    text_rock = font.render("R", True, (0, 0, 0))
    text_paper = font.render("P", True, (0, 0, 0))
    text_scissors = font.render("S", True, (0, 0, 0))
    text_rect_rock = text_rock.get_rect(center=(width // 2 - 150, height // 1.3))  # Position "ROCK" button
    text_rect_paper = text_paper.get_rect(center=(width // 2, height // 1.3))  # Position "PAPER" button
    text_rect_scissors = text_scissors.get_rect(center=(width // 2 + 150, height // 1.3))  # Position "SCISSORS" button
    screen.blit(text_rock, text_rect_rock)
    screen.blit(text_paper, text_rect_paper)
    screen.blit(text_scissors, text_rect_scissors)
    x = - 160
    for action, key in key_mappings.items():
        text = font.render(f"{pygame.key.name(key)}", True, (128, 128, 128))
        screen.blit(text, (width // 2 + x, height // 1.2))
        x += 150


    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_rock.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_rock.inflate(highlight_offset, highlight_offset),
                         4)  # Highlight "ROCK" button
    if text_rect_paper.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_paper.inflate(highlight_offset, highlight_offset),
                         4)  # Highlight "PAPER" button
    if text_rect_scissors.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_scissors.inflate(highlight_offset, highlight_offset),
                         4)  # Highlight "SCISSORS" button
    pygame.display.flip()

def draw_game_screen(player_score, computer_score, draw_score, player_choice, computer_choice, round_outcome):
    screen.fill((0, 191, 255))
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player: {player_score}", True, black)
    computer_text = font.render(f"Computer: {computer_score}", True, black)
    draw_text = font.render(f"Draw: {draw_score}", True, black)

    # Draw player and computer choices
    choices_text = font.render(f"Player: {player_choice}   Computer: {computer_choice}", True, black)
    screen.blit(player_text, (20, 20))
    screen.blit(computer_text, (width - computer_text.get_width() - 20, 20))
    screen.blit(draw_text, (width // 2 - draw_text.get_width() // 2, 20))
    screen.blit(choices_text, (width // 2 - choices_text.get_width() // 2, height // 2 - 50))

    # Display round outcome label
    if round_outcome:
        outcome_text = font.render(round_outcome, True, (255, 0, 0))
        screen.blit(outcome_text, (width // 2 - outcome_text.get_width() // 2, height // 2 + 20))


# Function to determine the winner of the game
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Tie"
    elif (player_choice == "Rock" and computer_choice == "Scissors") or \
            (player_choice == "Scissors" and computer_choice == "Paper") or \
            (player_choice == "Paper" and computer_choice == "Rock"):
        return "Player"
    else:
        return "Computer"



def in_game():
    screen.fill((0, 191, 255))
    font = pygame.font.SysFont("arialblack", 35)
    text_1_gamemode = font.render("RESUME", True, (0, 0, 0))
    text_3_option = font.render("SETTINGS", True, (0, 0, 0))
    text_home = font.render("HOME", True, (0, 0, 0))
    text_4_exit = font.render("EXIT", True, (0, 0, 0))
    text_rect_1_gamemode = text_1_gamemode.get_rect(center=(width // 2, height // 2 - 90))
    text_rect_3_option = text_3_option.get_rect(center=(width // 2, height // 2 - 30))
    text_rect_home = text_home.get_rect(center=(width // 2, height // 2 + 30))
    text_rect_4_exit = text_4_exit.get_rect(center=(width // 2, height // 2 + 90))
    screen.blit(text_1_gamemode, text_rect_1_gamemode)
    screen.blit(text_3_option, text_rect_3_option)
    screen.blit(text_home, text_rect_home)
    screen.blit(text_4_exit, text_rect_4_exit)
    # Highlight buttons when hovered over
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_1_gamemode.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_1_gamemode.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_3_option.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_3_option.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_home.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_home.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_4_exit.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_4_exit.inflate(highlight_offset, highlight_offset), 4)
    pygame.display.flip()


def exit_setting_ingame():
    exit_setting = True
    while exit_setting:
        setting_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100:
                    if height // 2 + 70 < mouse_pos[1] < height // 2 + 160:  # Adjusted y-coordinates for "Back" button
                        # If mouse clicked on "Back" button
                        return


# Function to handle one player mode
def handle_one_player_mode():
    computer_score = 0
    player_score = 0
    draw_score = 0
    player_choice = ""
    computer_choice = ""

    round_outcome = ""
    run = True
    paused = False
    while run:
        if not paused:
            handle_one_player_mode_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse click events
                    mouse_pos = pygame.mouse.get_pos()
                    for action, key in key_mappings.items():
                        if (height // 1.3 - 15 < mouse_pos[1] < height // 1.3 + 15 and
                                width // 2 - 150 + list(key_mappings.keys()).index(action) * 150 < mouse_pos[0] < width // 2 - 150 + (list(key_mappings.keys()).index(action) + 1) * 150):
                            screen.fill((0, 191, 255))
                            player_choice = action
                            computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                            result = determine_winner(player_choice, computer_choice)
                            if result == "Computer":
                                computer_score += 1
                                round_outcome = "Computer Wins!"
                            elif result == "Player":
                                player_score += 1
                                round_outcome = "Player Wins!"
                            else:
                                draw_score += 1
                                round_outcome = "Draw!"
                            break
                elif event.type == pygame.KEYDOWN:
                    # Handle key press events
                    keys = pygame.key.get_pressed()
                    for action, key in key_mappings.items():
                        if keys[key]:
                            screen.fill((0, 191, 255))
                            player_choice = action
                            computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                            result = determine_winner(player_choice, computer_choice)
                            if result == "Computer":
                                computer_score += 1
                                round_outcome = "Computer Wins!"
                            elif result == "Player":
                                player_score += 1
                                round_outcome = "Player Wins!"
                            else:
                                draw_score += 1
                                round_outcome = "Draw!"
                            break
        else:

            while paused:
                in_game()  # Show pause menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 115 < mouse_pos[
                            1] < height // 2 - 65:
                            # If mouse clicked on "GAMEMODE" button
                            paused = False
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 55 < mouse_pos[
                            1] < height // 2 - 5:
                            exit_setting_ingame()
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 + 5 < mouse_pos[
                            1] < height // 2 + 55:
                            exit_with_gamemode_setting_exit()
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 + 65 < mouse_pos[
                            1] < height // 2 + 115:
                            pygame.quit()
                            sys.exit()
        draw_game_screen(player_score, computer_score, draw_score, player_choice, computer_choice, round_outcome)
        handle_one_player_mode_buttons()
        if round_outcome:
            pygame.display.flip()
            time.sleep(1)  # Display outcome for 1 second
            round_outcome = ""  # Reset round outcome label
    pygame.display.flip()
    clock.tick(60)



def choose_2_player_option():
    font = pygame.font.SysFont("arialblack", 35)
    text_1_together = font.render("TOGETHER", True, (0, 0, 0))
    text_2_server = font.render("SERVER", True, (0, 0, 0))
    text_3_back = font.render("BACK", True, (0, 0, 0))
    text_rect_1_together = text_1_together.get_rect(center=(width // 2, height // 2 - 60))
    text_rect_2_server = text_2_server.get_rect(center=(width // 2, height // 2))
    text_rect_3_back = text_3_back.get_rect(center=(width // 2, height // 2 + 60))
    screen.blit(text_1_together, text_rect_1_together)
    screen.blit(text_2_server, text_rect_2_server)
    screen.blit(text_3_back, text_rect_3_back)
    pygame.display.flip()

def draw_game_screen_2_player(player1_score, player2_score, draw_score, player1_choice, player2_choice, round_outcome):
    screen.fill((0, 191, 255))
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player1: {player1_score}", True, black)
    computer_text = font.render(f"Player2: {player2_score}", True, black)
    draw_text = font.render(f"Draw: {draw_score}", True, black)
    choices_text = font.render(f"Player1: {player1_choice}   Player2: {player2_choice}", True, black)
    screen.blit(player_text, (20, 20))
    screen.blit(computer_text, (width - computer_text.get_width() - 20, 20))
    screen.blit(draw_text, (width // 2 - draw_text.get_width() // 2, 20))
    screen.blit(choices_text, (width // 2 - choices_text.get_width() // 2, height // 2 - 50))
    if round_outcome:
        outcome_text = font.render(round_outcome, True, (255, 0, 0))
        screen.blit(outcome_text, (width // 2 - outcome_text.get_width() // 2, height // 2 + 20))
def handle_two_player_mode_buttons():
    font = pygame.font.SysFont("arialblack", 30)
    text_rock1 = font.render("R", True, (0, 0, 0))
    text_paper1 = font.render("P", True, (0, 0, 0))
    text_scissors1 = font.render("S", True, (0, 0, 0))
    text_rect_rock1 = text_rock1.get_rect(center=(width // 2 - 300, height // 1.3))
    text_rect_paper1 = text_paper1.get_rect(center=(width // 2 - 225, height // 1.3))
    text_rect_scissors1 = text_scissors1.get_rect(center=(width // 2 - 150, height // 1.3))
    screen.blit(text_rock1, text_rect_rock1)
    screen.blit(text_paper1, text_rect_paper1)
    screen.blit(text_scissors1, text_rect_scissors1)
    mouse_pos = pygame.mouse.get_pos()
    highlight_offset = 10
    if text_rect_rock1.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_rock1.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_paper1.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_paper1.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_scissors1.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_scissors1.inflate(highlight_offset, highlight_offset), 4)

    x = -300
    for action, key in key_mappings.items():
        text = font.render(f"{pygame.key.name(key)}", True, (128, 128, 128))
        text_rect = text.get_rect(center=(width // 2 + x, height // 1.2))
        screen.blit(text, text_rect)
        x += 75

    text_rock2 = font.render("R", True, (0, 0, 0))
    text_paper2 = font.render("P", True, (0, 0, 0))
    text_scissors2 = font.render("S", True, (0, 0, 0))
    text_rect_rock2 = text_rock2.get_rect(center=(width // 2 + 300, height // 1.3))
    text_rect_paper2 = text_paper2.get_rect(center=(width // 2 + 225, height // 1.3))
    text_rect_scissors2 = text_scissors2.get_rect(center=(width // 2 + 150, height // 1.3))
    screen.blit(text_rock2, text_rect_rock2)
    screen.blit(text_paper2, text_rect_paper2)
    screen.blit(text_scissors2, text_rect_scissors2)
    if text_rect_rock2.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_rock2.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_paper2.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_paper2.inflate(highlight_offset, highlight_offset), 4)
    if text_rect_scissors2.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (0, 0, 0), text_rect_scissors2.inflate(highlight_offset, highlight_offset), 4)
    x = 150
    for action, key in key_mappings2.items():
        text = font.render(f"{pygame.key.name(key)}", True, (128, 128, 128))
        text_rect = text.get_rect(center=(width // 2 + x, height // 1.2))
        screen.blit(text, text_rect)
        x += 75
    pygame.display.flip()

def determine_winner2(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "Tie"
    elif (player1_choice == "Rock" and player2_choice == "Scissors") or \
            (player1_choice == "Scissors" and player2_choice == "Paper") or \
            (player1_choice == "Paper" and player2_choice == "Rock"):
        return "Player1"
    else:
        return "Player2"


def together():
    player1_score = 0
    player2_score = 0
    draw_score = 0
    player1_choice = ""
    player2_choice = ""
    round_outcome = ""
    run = True
    paused = False

    while run:
        if not paused:
            handle_two_player_mode_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                    else:
                        for action, key in key_mappings.items():
                            if event.key == key:
                                player1_choice = action
                        for action, key in key_mappings2.items():
                            if event.key == key:
                                player2_choice = action
                        if player1_choice and player2_choice:
                            result = determine_winner2(player1_choice, player2_choice)
                            if result == "Player2":
                                player2_score += 1
                                round_outcome = "Player2 Wins!"
                            elif result == "Player1":
                                player1_score += 1
                                round_outcome = "Player1 Wins!"
                            else:
                                draw_score += 1
                                round_outcome = "Draw!"

                            # Display the outcome for 1 second
                            draw_game_screen_2_player(player1_score, player2_score, draw_score, player1_choice,
                                                      player2_choice,
                                                      round_outcome)
                            pygame.display.flip()
                            time.sleep(1)

                            # Reset choices and outcome
                            player1_choice = ""
                            player2_choice = ""
                            round_outcome = ""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for action, key in key_mappings.items():
                        if (height // 1.3 - 15 < mouse_pos[1] < height // 1.3 + 15 and
                                width // 2 - 300 + list(key_mappings.keys()).index(action) * 75 < mouse_pos[
                                    0] < width // 2 - 300 + (list(key_mappings.keys()).index(action) + 1) * 75):
                            player1_choice = action
                    for action, key in key_mappings2.items():
                        if (height // 1.3 - 15 < mouse_pos[1] < height // 1.3 + 15 and
                                width // 2 + 300 - list(key_mappings2.keys()).index(action) * 75 < mouse_pos[
                                    0] < width // 2 + 300 - (list(key_mappings2.keys()).index(action) + 1) * 75):
                            player2_choice = action

                    # Check if both players have made their choices
                    if player1_choice and player2_choice:
                        result = determine_winner2(player1_choice, player2_choice)
                        if result == "Player2":
                            player2_score += 1
                            round_outcome = "Player2 Wins!"
                        elif result == "Player1":
                            player1_score += 1
                            round_outcome = "Player1 Wins!"
                        else:
                            draw_score += 1
                            round_outcome = "Draw!"

                        # Display the outcome for 1 second
                        draw_game_screen_2_player(player1_score, player2_score, draw_score, player1_choice,
                                                  player2_choice,
                                                  round_outcome)
                        pygame.display.flip()
                        time.sleep(1)

                        # Reset choices and outcome
                        player1_choice = ""
                        player2_choice = ""
                        round_outcome = ""
        else:
            while paused:
                in_game()  # Показать меню паузы
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 115 < mouse_pos[
                            1] < height // 2 - 65:
                            # Если мышь нажата на кнопку "GAMEMODE"
                            paused = False
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 - 55 < mouse_pos[
                            1] < height // 2 - 5:
                            exit_setting_ingame()
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 + 5 < mouse_pos[
                            1] < height // 2 + 55:
                            exit_with_gamemode_setting_exit()
                        elif width // 2 - 100 < mouse_pos[0] < width // 2 + 100 and height // 2 + 65 < mouse_pos[
                            1] < height // 2 + 115:
                            pygame.quit()
                            sys.exit()

        draw_game_screen_2_player(player1_score, player2_score, draw_score, player1_choice, player2_choice,
                                  round_outcome)
        handle_two_player_mode_buttons()
        pygame.display.flip()
        clock.tick(60)

def handle_two_players_mode():
    run = True
    while run:
        screen.fill((0, 191, 255))
        choose_2_player_option()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width // 2 - 100 < mouse_pos[0] < width // 2 + 100:
                    if height // 2 - 85 < mouse_pos[1] < height // 2 - 35:
                        together()
                    elif height // 2 - 25 < mouse_pos[1] < height // 2 + 25:
                        pass
                    elif height // 2 + 35 < mouse_pos[1] < height // 2 + 85:
                        exit_1_2_players_back()

        pygame.display.update()

# Main code
pygame.mixer.music.play(-1)
simulate_loading()
exit_from_button_play()
exit_with_gamemode_setting_exit()
pygame.quit()
sys.exit()