"""Applecore (Standard) v3.8-beta.1-dev
Copyright (c) 2024-2026 HBCC1999. All rights reserved.
Licensed under the terms in LICENSE. Unauthorized redistribution prohibited.
Developed by HBCC1999
Textures: Some are made by the author and some are AI-generated.
Audio: From Youtube Studio
Font by: Codeman38
----------------------------------------------------------------------------
"""

# using pygame-ce instead of pygame because pygame-ce is more up to date and has more features than pygame
import pygame
import random
import os
import sys
import time
import datetime
import psutil as p
from pathlib import Path
import math

pygame.init()

pygame.mixer.init()

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    """

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_data_path(file_name):
    """Path to the game-related data files, that are located in AppData/Local"""
    appdata = os.getenv("LOCALAPPDATA")
    folder = Path(appdata) / "Applecore" / "GameData"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder / file_name)

def save_data(data, file_name="highscores.txt", mode="w"):
    """Save the data to game files in Appdata/GameData, only to be used for game-data files, not assets"""
    with open(save_data_path(file_name), mode = mode) as f:
        f.write(data)

def read_data(file_name="highscores.txt"):
    """Read the data from game files in Appdata/GameData, only to be used for game-data files, not assets"""
    with open(save_data_path(file_name), "r") as f:
        data = f.read()
    return data

GAME_VERSION = __doc__.split("\n")[0]
print(__doc__, end="")

version = GAME_VERSION[GAME_VERSION.index("v"):]
snake = 30
testing_mode = False
debug_activated = False
DEFAULT_FPS = 60
scr = []
today_date = datetime.date.today()
# is_independence_month = (today_date.month == 8 and today_date.day == 14)
game_window = pygame.display.set_mode((900, 600))
is_independence_month = (today_date.month == 8) # Applies for the whole month of August.
if is_independence_month:
    # august_background = pygame.image.load(resource_path("assets/august_background.jpg"))
    # august_background = pygame.transform.scale(august_background, (900, 600)).convert_alpha()
    green_apple = pygame.image.load(resource_path("assets/green_apple.png")).convert_alpha()
    green_apple = pygame.transform.scale(green_apple, (snake, snake))
else:
    green_apple = None
mute_music = False
target_fps = DEFAULT_FPS
optimization_constant = 2.8 #This is a constant that is based of to calculate optimization index in gameloop its value is based of 70/25, where 25 is optimization index
# that implies that the system is optimized enough to run the game at 70% of display refresh rate and this is the highest in the middle tier fps

# display
BASE_VELOCITY = 384 # (8 * fps:=48) pixels per second, regardless of the frames
icon = pygame.image.load(resource_path('assets/appicon.png'))
icon = pygame.transform.scale(icon, (32, 32)).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_VERSION)
myimg = pygame.image.load(resource_path('assets/menu_screen_image.jpg'))
myimg = pygame.transform.scale(myimg, (900, 600)).convert_alpha()
go = pygame.image.load(resource_path('assets/game_over_screen.jpg'))
go = pygame.transform.scale(go, (900, 600)).convert_alpha()
default_background_image = pygame.image.load(resource_path('assets/background_image.jpg'))
default_background_image = pygame.transform.scale(default_background_image, (900, 600)).convert_alpha()
background_image = default_background_image
red_apple = pygame.image.load(resource_path('assets/apple.png'))
red_apple = pygame.transform.scale(red_apple, (snake, snake)).convert_alpha()
# s_i = pygame.image.load(resource_path('assets/sicon.png'))
# si = pygame.transform.scale(s_i, (43, 43)).convert_alpha()
setting_page = pygame.image.load(resource_path('assets/settings_page_image.png'))
setting_page = pygame.transform.scale(setting_page, (900, 600)).convert_alpha()
display_refresh_rate = pygame.display.get_current_refresh_rate()
p.cpu_percent(interval=None); time.sleep(0.3)
cpu_unused = 100 - p.cpu_percent(interval=None)
battery_unused = 100 if p.sensors_battery() is None else p.sensors_battery().percent
vram_unused = 100 - p.virtual_memory().percent
optimization_index = ((battery_unused*0.7)*(cpu_unused*0.2)*(vram_unused*0.1))/100

# colors
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 250, 10)
black = (0, 0, 0)
orange = (240, 150,7)
yellow = (240, 250, 5)
time1 = 0
time_taken_to_score = 0

# user name
if os.path.exists(save_data_path("user_info.txt")):
    username = read_data("user_info.txt").split("\n")[0]
    if len(username) <3 or len(username) > 20:
        username = "Player" + str(random.randint(0, 50)) + str(random.randint(50, 100))
        save_data(username, file_name="user_info.txt")
else:
    username = "Player" + str(random.randint(0, 50)) + str(random.randint(50, 100))
    save_data(username, file_name="user_info.txt")

print("Hello "+username)
# username = open(resource_path("user_info.txt")).read()[2:8]

# Better in-game-info management, now the game will check if the in-game-info
# file is corrupted or not, and if it is corrupted then it will reset the file to default values
gamefilecontent = ""
if os.path.exists(save_data_path('highscores.txt')):
    gamefilecontent = read_data("highscores.txt")
in_game_info = gamefilecontent.split("\n")
debug_mode = ((not len(in_game_info)<4) and in_game_info[3] == "True")
print(f"Debug: Debug mode set to {debug_mode}")

first_line_of_file = gamefilecontent.split("\n")[0] if gamefilecontent else ""

try:
    should_reset_gamefilecontent = (
        not first_line_of_file.isdigit() or
        not in_game_info[1].replace('.', '', 1).isdigit() or
        in_game_info[2] not in ('True', 'False')
    )

except IndexError:
    should_reset_gamefilecontent = True # The file is corrupted or empty

if should_reset_gamefilecontent:
    save_data("0\n0\nFalse")
    in_game_info = ["0", "0", "False"]

# This is a variable that determines whether the game should adjust its FPS based on the optimization index or not,
# if set to False the game will run at a constant FPS regardless of the optimization index
Dynamic_FPS = (in_game_info[2] == "True")

text_input = ""

# snake appearing function
def plot_snake(game_window, color, s_lst, snake):
    """Plots the snake on the game window,
    s_lst is a list of tuples containing the coordinates of the snake's body segments, 
    and snake is the size of each segment. Visually, the snake is represented as a series of squares drawn on the game window."""
    for x, y in s_lst:
        pygame.draw.rect(game_window, color, pygame.Rect(x, y,snake,snake), 20)

clock = pygame.time.Clock()

# controlling user input (text)
def usertext(event):
    """Accepting keyboard input from user and storing in variable.
    This feature is not fully implemented yet,
    stay tuned for the future updates!"""
    global text_input
    if event.key == pygame.K_BACKSPACE:
        if text_input:
            text_input=text_input[:-1]
        print(text_input)
    else:
        text_input+=event.unicode
        print(text_input)


# font
# printing text on game
_font_cache = {}
def get_font(size, italic, bold):
    """Returns specified font from _font_cache, thus preventing unnecessary IO calls for same key"""
    key = (size, italic, bold)
    if key not in _font_cache:
        font = pygame.font.Font(resource_path("assets/PressStart2P-Regular.ttf"), size=size)
        font.set_bold(bold)
        font.set_italic(italic)
        _font_cache[key] = font
        print(f"Debug: Loaded font for {key=}")

    return _font_cache[key]


def fading_text(text, color, x, y, bold=False, italic=False, size=16, period=2.0):
    """Fading text (in and out) using sin wave."""
    font = get_font(size, italic, bold)
    text_show = font.render(text, True, color)
    # oscillates smoothly between 0 and 255
    alpha = int((math.sin(time.time() * (2 * math.pi / period)) * 0.5 + 0.5) * 255)
    text_show.set_alpha(alpha)
    game_window.blit(text_show, (x, y))

_alpha_states = {}
def fading_background_filter(surface: pygame.Surface, x=0, y=0, start_alpha=100,
                             target_alpha=0, fade_speed=2, reset=False, cycle=False):
    """Frame-based fading background, reset=True means you can redisplay the effect on the same surface on repeted calls.
    If you want an oscilating-fade, then turn cycle to True, and fade_speed to the value of period of this oscillation."""
    fade_in = start_alpha > target_alpha

    # background_filter = surface.get_rect()
    # background_filter.topleft = (x, y)
    # game_window.blit(surface, background_filter)

    overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0,0,0,255))

    current_alpha = _alpha_states.get(surface) if not cycle else int((math.sin(time.time() * (2 * math.pi / fade_speed)) * 0.5 + 0.5) * 255)

    if not cycle:
        if current_alpha is None:
            _alpha_states[surface] = start_alpha
            current_alpha = start_alpha

        if fade_in and current_alpha>target_alpha:
            current_alpha = max(current_alpha - fade_speed, target_alpha)
        elif fade_in and current_alpha < 255:
            current_alpha = min(current_alpha + fade_speed, 255)
        elif not fade_in and current_alpha < target_alpha:
            current_alpha = min(current_alpha + fade_speed, target_alpha)
        elif not fade_in and current_alpha > 0:
            current_alpha = max(current_alpha - fade_speed, 0)

        if current_alpha != _alpha_states[surface]:
            _alpha_states[surface] = current_alpha

    overlay.set_alpha(current_alpha)

    game_window.blit(surface, (x,y))
    game_window.blit(overlay, (x,y))

_fade_states = {}
def fade_in_text(text, color, x, y, bold=False, italic=False, size=16, key=None, background_box=True,
                padding=2, bg_color=(0,0,0), bg_alpha=128, reset=False, duration:float=1):
    """Fade text in from transparent to opaque over `duration` seconds, then stays opaque."""
    font = get_font(size, italic, bold)
    text_show = font.render(text, True, color)

    fade_key = key if key is not None else text

    if reset or fade_key not in _fade_states:
        _fade_states[fade_key] = time.time()

    elapsed = time.time() - _fade_states[fade_key]
    progress = min(elapsed/duration, 1) if duration!=0 else 1
    alpha = int(progress*255)

    if background_box and len(text) != 0:
        text_rect = text_show.get_rect(topleft=(x, y))

        box_width = text_rect.width + padding * 2
        box_height = text_rect.height + padding * 2
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

        box_surface.fill((*bg_color, bg_alpha))
        game_window.blit(box_surface, (x - padding, y - padding))

    text_show.set_alpha(alpha)
    game_window.blit(text_show, (x,y))


def load_text(text: str, color: tuple, x: int|float, y: int|float,
            bold: bool=False, italic: bool=False,size: int=16, padding=4, bg_color=(0,0,0),
            bg_alpha=128, background_box=True):
    """Shows Text on Window.
    bold = True -> Bold text
    italic = True -> Italic text
    size = n -> Text size
    (x, y) -> Coords to place text on
    color -> RGB value of color for the foreground of text
    text -> String
    bg_color -> background box color
    bg_alpha -> background box transparency measure(255 - opaque, 0 - tansparent)
    padding -> Padding in box on x and y
    """
    font = get_font(size, italic, bold)

    # txt = font.render(text, True, color)
    text_surface = font.render(text, False, color)

    if background_box and len(text) != 0:
        text_rect = text_surface.get_rect(topleft=(x, y))

        # background box based on length of text
        box_width = text_rect.width + padding * 2
        box_height = text_rect.height + padding * 2
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        # bg_color = (0,0,0)
        
        # box color = color + alpha
        box_surface.fill((*bg_color, bg_alpha))

        # box + text display
        game_window.blit(box_surface, (x - padding, y - padding))

    game_window.blit(text_surface, (x, y))


def text_dimensions(text: str, bold: bool=False, italic: bool=False, size: int=16, 
                    padding=4, background_box=True):
    """Values of the width and height of the overlay panel(background box) and the text itself, in pixels."""

    font = get_font(size, italic, bold)
    # txt = font.render(text, True, color)
    text_width, text_height = font.size(text)

    if background_box and len(text) != 0:
        # background box based on length of text
        box_width = text_width + padding * 2
        box_height = text_height + padding * 2
        return text_width, text_height, box_width, box_height
    
    return text_width, text_height, 0, 0


def leftover_pixels(text: str, bold: bool=False, italic: bool=False, size: int=16,
                     padding=4, background_box=True, side: str="x", leftover: int=10):
    """Calculates the x or y coordinate so the text/box ends `leftover` 
    pixels away from the edge of the screen, along the given axis."""
    
    if side not in ("x", "y"):
        raise ValueError("side must be 'x' or 'y'")
    
    text_w, text_h, box_w, box_h = text_dimensions(
        text, bold=bold, italic=italic, size=size, 
        padding=padding, background_box=background_box
    )
    
    size_to_use = box_w if background_box else text_w
    screen_size = game_window.get_width()
    
    if side == "y":
        size_to_use = box_h if background_box else text_h
        screen_size = game_window.get_height()
    
    return screen_size - leftover - size_to_use


def independendence_day_page():
    """An easter egg to celibrate Pakistan's Independence day on 14th August. (any year)"""
    pygame.event.clear()
    start_time = time.time()
    quit_game = False

    while not quit_game:
        game_window.fill((220, 200, 240))
        # elapsed = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                    pygame.mixer.music.play(-1)
                return quit_game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if not mute_music:
                        pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                        pygame.mixer.music.play(-1)
                    return quit_game
            # elif elapsed >= 2:

        pygame.display.update()
        clock.tick(30)


def pause_window():
    """Pauses the game after esc key is pressed, in this state, snake attributes 
    can't be changed and time spent in this state is not accounted for in time_taken_to_score.
    Game remains paused until esc is pressed again or game is quit.
    Many other keybinds like O key, f3 or f1, pretty much everything is not functional in this state
    so as to provide legitimate gameplay. Also the FPS indicator is not shown in this state."""
    quit_game = False
    s_time = time.time()

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                sys.exit()
                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                    pygame.mixer.music.play(-1)
                return quit_game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game = False
                    quit_game=True
                    time_paused = time.time() - s_time
                    return time_paused
                
        pygame.display.update()
        clock.tick(30)


def settings_page():
    """Settings page, coming soon!"""
    save_text_time = 0
    global text_input
    global username
    allowuinput = False
    quit_game = False
    text_input = username

    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(setting_page, (0, 0))
        load_text(text_input, (0, 50, 240), 352, 127, bold=False, bg_color = (20,200,90), bg_alpha=100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    menu_screen()
                elif event.key == pygame.K_RETURN:
                    # Save new username
                    if len(text_input) > 2 and len(text_input) <= 20:
                        save_data(data=text_input, file_name="user_info.txt")
                        username = text_input
                        save_text_time = time.time()
                    else:
                        text_input = username
                elif event.key == pygame.K_BACKSPACE:
                    if text_input:
                        text_input=text_input[:-1]
                    print(text_input)
                else:
                    text_input+=event.unicode
                    print(text_input)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    m_p = event.pos
                    if m_p[0] > 260 and m_p[0] < 378 and m_p[1] > 95 and m_p[1] < 117:
                        print('successful')
                    if m_p[0] > 810 and m_p[0] < 850 and m_p[1] > 27 and m_p[1] < 64:
                        pygame.mixer.music.stop()
                        menu_screen()

        if time.time() - save_text_time < 1:
            fade_in_text("Username saved successfully", x=20, y=570, color=green)

        text_input = text_input.strip("\r")
        text_input = text_input.replace(" ", "_")
        if text_input and (text_input[0].isdigit() or not text_input[0].isascii()):
            text_input = "_" + text_input[1:]

        pygame.display.update()
        clock.tick(30)


def menu_screen():
    """Main menu screen, where the game starts and user can access settings or start the game."""
    global mute_music
    if not mute_music:
        pygame.mixer.music.load(resource_path("assets/menu_screen_music.mp3"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    quit_game = False
    
    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(myimg, (0, 0))

        # game_window.blit(si, (817, 56))
        # load_text('Pyth0n wants to eat some apples...'.title(), yellow, 200, 150)
        # load_text("Hello "+username+"!".title(), blue, 510, 50, b=True)
        # load_text('Help him out!!!'.title(), yellow, 300, 260)
        # load_text('press the space bar to play :)', yellow, 250, 400, True)
        fade_in_text(version, (220, 220, 190), leftover_pixels(version, leftover=3, size=13, bold=False), 583, bold=False, size=13)
        fade_in_text("Copyright HBCC1999. All rights reserved.", (220, 220, 190), 8, 583, bold=False, size=12)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    m_p = event.pos
                    if m_p[0] > 801 and m_p[0] < 856 and m_p[1] > 50 and m_p[1] < 123:
                        print('successful')
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/settings_page_music.mp3"))
                            pygame.mixer.music.play()
                        settings_page()
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/menu_screen_music.mp3"))
                            pygame.mixer.music.play(-1)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    mute_music = not mute_music
                    if mute_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(resource_path("assets/menu_screen_music.mp3"))
                        pygame.mixer.music.play(-1)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not mute_music:
                        pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                        pygame.mixer.music.play(-1)
                    gameloop()

        # load_text('Pyth0n wants to eat some apples...'.title(), blue, 200, 150)
        pygame.display.update()
        clock.tick(30)


# Main game loop / In-game loop
def gameloop():
    """Main game loop, where the actual gameplay happens. This function includes
    the main-game and game-over screen, as well as the logic for the snake's movement, 
    collision detection, scoring, and FPS optimization based on system performance."""
    global mute_music
    global optimization_index
    global target_fps
    global in_game_info
    global Dynamic_FPS
    global time_taken_to_score
    global testing_mode
    global debug_activated
    global background_image

    # ctime = time.localtime()
    # ctime = time.strftime("%H-%M-%S")
    # starting_time_for_timer = time.time()
    # timer = f"{}:{}:{time.time()-starting_time_for_timer}"

    time1 = None
    testing_mode_time_start = 0
    difficulty_mode_change_time_start = 0
    independence_month_toggle_time_start = 0
    Dynamic_FPS_time_start = 0
    debug_activated = False
    debug_score = False

    snake = 30
    apple_collrate = 12
    collrate = 7
    segment_spacing = 6 # how spaced each square should be, lower value equals better visuals
    distance_since_last_segment = 0
    trailing_buffer = 5
    fps = DEFAULT_FPS

    h_score = in_game_info[0]
    h_appocity = in_game_info[1]

    appocity = "0 apple/second"
    quit_game = False
    game_over = False

    score = 0

    # entity - related variables and constants
    difficulty_velocity_change = 0
    food_x = random.randint(40, 800)
    food_y = random.randint(50, 500)
    green_food_x= random.randint(40, 840)
    green_food_y= random.randint(25,550)
    snake_x = random.randint(350,520)
    snake_y = random.randint(200,400)
    death_frame = False

    velocity_x = 0
    velocity_y = 0
    init_velocity = BASE_VELOCITY
    init_velocity_change = 0

    pause_game = False
    s_lst = [[int(snake_x), int(snake_y)]]
    direction_changed = False
    s_length = 1
    s_controler = 3
    time_paused = 0
    show_green_apple = random.choice([False, False, False, False, True])
    time_before_game_loop = time.time()

    while not quit_game:
        dt = clock.tick(fps) / 1000.0  # Amount of seconds between each loop/frame and seconds because i follow SI units.
        dt = min(dt, 0.05) # Cap it at 50ms. So no stutters and wierd teleportation after toggling pause_menu
    
        if game_over:
            fps = 30
            if death_frame:
                death_frame = False
                appocity = (round(score/time_taken_to_score,2)) if time_taken_to_score != 0 else None
                
                # Checking if the current appocity is greater than the highest appocity and updating it if necessary
                if appocity is not None and (appocity) > float(h_appocity) and not testing_mode and not debug_activated:
                    h_appocity = str(appocity)
                    in_game_info[1] = str(appocity)
                
                # Checking if the current score is greater than the highscore and updating it if necessary
                if score > int(h_score) and not testing_mode and not debug_activated:
                    h_score = str(score)
                    in_game_info[0] = str(score)
                
                if in_game_info[2] != str(Dynamic_FPS):
                    in_game_info[2] = str(Dynamic_FPS)

                save_data("\n".join(in_game_info))

                show_green_apple = random.choice([False, False, False, False, True])

            game_window.fill(white)
            fading_background_filter(go)

            plot_snake(game_window, (blue[0]+80, blue[1], blue[2]-100), s_lst, snake) # Snake frozen in time after death.
            # game_window.blit(red_apple, (food_x, food_y)) if testing_mode else None

            difficulty = (
                "Easy"
                if apple_collrate == 16
                else "Medium"
                if apple_collrate == 12
                else "Hard"
                if apple_collrate == 8
                else "Ultra-Hard"
                if apple_collrate == 4
                else "not known"
            )

            fade_in_text("PRESS ENTER TO CONTINUE", red, 270, 218 + 6)
            fade_in_text(f"Highscore: {h_score}", (0, 191, 255), 10, 7, bold=False, key="highscore")
            fade_in_text(
                f"Highest Appocity: {h_appocity}",
                (0, 191, 255),
                leftover_pixels(
                    f"Highest Appocity: {h_appocity}",
                    bold=False,
                    size=16,
                    padding=4,
                    background_box=True,
                    side="x",
                    leftover=5,
                ),
                7,
                bold=False,
                key = "record-appocity"
            )

            scr.append(score)

            fade_in_text(
                f"Score: {score}",
                (yellow if (not testing_mode and not debug_activated) else orange),
                365,
                218 + 30 + 10,
                bold=False,
                key = "score"
            )
            fade_in_text(
                f"Time Taken: {time_taken_to_score}",
                (yellow if (not testing_mode and not debug_activated) else orange),
                330,
                218 + 60 + 10,
                bold=False,
                key = "time-taken-to-score"
            )
            # load_text(f'Appocity = {appocity if appocity is not None else "undefined"} {"apple" if (appocity is not None and appocity <= 1) else "apples"}/second'.capitalize()
            # ,(yellow if (not testing_mode and not debug_activated) else orange),
            # 330, 218+90, bold=False)
            fade_in_text(
                f"Appocity: {appocity if appocity is not None else 'None'} aps".capitalize(),
                (yellow if (not testing_mode and not debug_activated) else orange),
                300,
                218 + 90 + 10,
                bold=False,
                key = "appocity"
            )
            fade_in_text(
                f"Difficulty: {difficulty}",
                color=(
                    green
                    if difficulty == "Easy"
                    else yellow
                    if difficulty == "Medium"
                    else orange
                    if difficulty == "Hard"
                    else red
                    if difficulty == "Ultra-Hard"
                    else yellow
                ),
                x=310,
                y=218 + 120 + 10,
                bold=False,
                key = "difficulty"
            )
            fade_in_text("Go Again!", (0, 123, 255), 300 + 65, 218 + 150 + 10, size=20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        mute_music = not mute_music
                        if mute_music:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                            pygame.mixer.music.play(-1)

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_o:
                        if not mute_music:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                            pygame.mixer.music.play(-1)
                        scr.clear()
                        gameloop()
                    elif event.key == pygame.K_HOME:
                        scr.clear()
                        menu_screen()


        else:
            # Main Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    time_taken_to_score = round(time.time() - time1 - time_paused, 2) if time1 is not None else 0
                    appocity = (round(score/time_taken_to_score,2)) if time_taken_to_score != 0 else None
                    # Checking if the current appocity is greater than the highest appocity and updating it if necessary
                    if appocity is not None and (appocity) > float(h_appocity):
                        h_appocity = str(appocity)
                        in_game_info[1] = str(appocity)
                    # print(time_taken_to_score, appocity, h_appocity)
                    
                    # Checking if the current score is greater than the highscore and updating it if necessary
                    if score > int(h_score):
                        h_score = str(score)
                        in_game_info[0] = str(score)
                    
                    if in_game_info[2] != str(Dynamic_FPS):
                        in_game_info[2] = str(Dynamic_FPS)

                    save_data("\n".join(in_game_info))

                    quit_game = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("[Main Game]",event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_game = not pause_game
                        # time_paused = pause_window()
                    if event.key == pygame.K_F1:
                        mute_music = not mute_music
                        if mute_music:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                            pygame.mixer.music.play(-1)
                    # Testing Mode: LCtrl + T
                    if event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        testing_mode = not testing_mode
                        testing_mode_time_start = time.time()
                        # print(testing_mode)
                    #  Toggle Independence Month State, to access green apple
                    if testing_mode and event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        global is_independence_month
                        global green_apple
                        is_independence_month = not is_independence_month
                        independence_month_toggle_time_start = time.time()
                        # if is_independence_month and show_green_apple:
                        #     show_green_apple = False
                        if is_independence_month and green_apple is None:
                            green_apple = pygame.image.load(resource_path("assets/green_apple.png")).convert_alpha()
                            green_apple = pygame.transform.scale(green_apple, (snake, snake))
                            print("Loaded Green Apple")
                    if event.key == pygame.K_F3:
                        Dynamic_FPS_time_start = time.time()
                        Dynamic_FPS = not Dynamic_FPS
                        if not Dynamic_FPS:
                            target_fps = DEFAULT_FPS if display_refresh_rate >= DEFAULT_FPS else display_refresh_rate
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and velocity_x == 0 and init_velocity != 0:
                        velocity_x = init_velocity
                        velocity_y = 0
                        direction_changed = True
                    elif event.key == pygame.K_F12 and testing_mode and debug_mode:
                        debug_score = True
                        debug_activated = True
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and velocity_x == 0 and init_velocity != 0:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        direction_changed = True
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and velocity_y == 0 and init_velocity != 0:
                        velocity_y = -init_velocity
                        velocity_x = 0
                        direction_changed = True
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and velocity_y == 0 and init_velocity != 0:
                        velocity_y = init_velocity
                        velocity_x = 0
                        direction_changed = True
                    elif event.key == pygame.K_i and testing_mode:
                        debug_activated = True
                        if random.choice([1,2,3]) == 2:
                            score += 10
                        elif random.choice([1,2,3,4,5,6,7,8,9,10]) == 5:
                            score+=20
                    elif event.key == pygame.K_v:
                        init_velocity_change += 48
                    elif event.key == pygame.K_c:
                        if init_velocity != 0 and init_velocity != 1:
                            init_velocity_change -= 48
                        # else: #if want to reset velocity to default after pressing c beyond 0 velocity
                        #     init_velocity_change = 0
                    elif event.key == pygame.K_o:
                        game_over = True
                        death_frame = True
                        if time1 is not None:
                            time_taken_to_score = round(time.time() - time1 - time_paused, 2)
                        else:
                            time_taken_to_score = 0
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                            pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_x:
                        s_controler += 2
                    elif event.key == pygame.K_z:
                        if s_controler > 2:
                            s_controler -= 2
                        else:
                            s_controler = 0 # Golden Dandelion which is a golden dandelion
                    elif event.key == pygame.K_e:
                        difficulty_mode_change_time_start = time.time()
                        apple_collrate = 16
                        difficulty_velocity_change = 0
                    elif event.key == pygame.K_m:
                        difficulty_mode_change_time_start = time.time()
                        apple_collrate = 12
                        s_controler = 4
                        difficulty_velocity_change = 0
                    elif event.key == pygame.K_h:
                        difficulty_mode_change_time_start = time.time()
                        apple_collrate = 8
                        s_controler = 5
                        difficulty_velocity_change = round((BASE_VELOCITY)*(15/100))
                    elif event.key == pygame.K_u:
                        difficulty_mode_change_time_start = time.time()
                        apple_collrate = 4
                        s_controler = 6
                        difficulty_velocity_change = round((BASE_VELOCITY)*(30/100))

            game_window.fill(white)
            fading_background_filter(background_image, 0, 0)

            if (velocity_x != 0 or velocity_y !=0) and time1 is None:
                time1 = time.time()
                time_paused = 0

            velocity_x_f = (velocity_x * dt)
            velocity_y_f = (velocity_y * dt)

            snake_x += (velocity_x_f)
            snake_y += (velocity_y_f)

            if is_independence_month and show_green_apple:
                # 20% chance for the green apple to appear(only on 14 August)
                # background_image = august_background
                # pygame.draw.rect(game_window, (0, 130, 0),
                # pygame.Rect(green_food_x,green_food_y,snake,snake))
                game_window.blit(green_apple, (green_food_x, green_food_y))

                if (abs(snake_x-green_food_x) < apple_collrate and abs(snake_y-green_food_y) < apple_collrate) or debug_score:
                    green_food_x = random.randint(40, 840)
                    green_food_y = random.randint(25, 550)
                    score += 30
                    s_length += s_controler
                    show_green_apple = random.choice([False, True])
                    # pygame.mixer.music.stop()
                    # if independendence_day_page():
                    #     break
                    # else:
                    #     pygame.event.clear()
                    debug_score = False


            elif (abs(snake_x-food_x) < apple_collrate and abs(snake_y-food_y) < apple_collrate) or debug_score:
                score += 10
                # print(s_lst)
                food_x = random.randint(40, 840)
                food_y = random.randint(25, 550)
                s_length += s_controler
                # Bug fix for green apple vanishing after existing for a moment.
                if is_independence_month and not show_green_apple:
                    show_green_apple = random.choice([False, True]) if is_independence_month else False
                    # green_food_x = random.randint(40, 840)
                    # green_food_y = random.randint(25, 550)
                debug_score = False


            # New Snake rendering system(v3.7+)
            step_dist = abs(velocity_x_f) + abs(velocity_y_f)
            distance_since_last_segment += step_dist

            # direction_changed can also be synced with velocity_x and velocity_y but this approach works just fine
            if direction_changed:
                # Prevents redrawing a box on almost same positions to avoid self collision in extreme-case velocity scenarios.
                if not s_lst or abs(s_lst[-1][0]-snake_x) >= 1 or abs(s_lst[-1][1]-snake_y) >= 1:
                    s_lst.append([int(snake_x), int(snake_y)])
                distance_since_last_segment = 0
                direction_changed = False

            while distance_since_last_segment >= segment_spacing:
                head = []
                head.append(int(snake_x))
                head.append(int(snake_y))
                s_lst.append(head)
                distance_since_last_segment -= segment_spacing

            if len(s_lst) > s_length:
                del s_lst[0:len(s_lst) - s_length]
            
            # New version of self-collision check to comply with the new snake motion system
            # deadly_apple:
            #     self_collision = any(
            #         abs(head[0]-segment_x) < collrate and abs(head[1]-segment_y) < collrate
            #         for segment_x, segment_y in s_lst[:len(s_lst)-1]
            #     )
   
            self_collision = any(
                abs(head[0]-segment_x) < collrate and abs(head[1]-segment_y) < collrate
                for segment_x, segment_y in s_lst[:-1-trailing_buffer]
            )

            if self_collision:
                game_over = True
                death_frame = True
                if time1 is not None:
                    time_taken_to_score = round(time.time() - time1 - time_paused, 2)
                else:
                    time_taken_to_score = 0

                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                    pygame.mixer.music.play(-1)

            game_window.blit(red_apple, (food_x, food_y)) if not (is_independence_month and show_green_apple) else None


            if snake_x <= 0 or snake_x + snake > 900 or snake_y <= 0 or snake_y + snake > 600:
                game_over = True
                death_frame = True
                if time1 is not None:
                    time_taken_to_score = round(time.time() - time1 - time_paused, 2)
                else:
                    time_taken_to_score = 0

                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                    pygame.mixer.music.play(-1)


            # Dynamic FPS (v3.6+)
            if time.time()-time_before_game_loop >= 3 and Dynamic_FPS:
                cpu_unused = 100 - p.cpu_percent(interval=None)
                # Checking if the battery sensor is available and getting the battery unused percentage, if not available setting it to 100% unused
                battery_unused = 100 if p.sensors_battery() is None else p.sensors_battery().percent
                # battery_unused = random.randint(1, 50)
                vram_unused = 100 - p.virtual_memory().percent
                # New quantity that measures the overall optimization of the system for gaming, calculated using the battery, cpu and vram unused percentages
                optimization_index = ((battery_unused*0.7)*(cpu_unused*0.2)*(vram_unused*0.1))/100
                # print(optimization_index, battery_unused, cpu_unused, vram_unused)

                if battery_unused == 100 or p.sensors_battery().power_plugged:
                    # fps = display_refresh_rate
                    target_fps = display_refresh_rate

                if optimization_index >= 25:
                    # fps = display_refresh_rate
                    target_fps = display_refresh_rate

                elif (optimization_index != 0 and optimization_index < 25 and optimization_index >= 12) and battery_unused<30:
                    if display_refresh_rate >= 60:
                        target_fps = (round(optimization_index)* optimization_constant)/100 * display_refresh_rate
                    elif display_refresh_rate < 60:
                        target_fps = (round(optimization_index)* optimization_constant)/100 * display_refresh_rate
                        
                elif (optimization_index != 0 and optimization_index < 25 and optimization_index >= 12) and battery_unused>=25:
                    target_fps = 48 # mid-tear fps

                else:
                    # fps = 20
                    target_fps = 20 # lowest fps

                target_fps = 20 if target_fps < 20 else target_fps
                target_fps = int(target_fps)
                # print(optimization_index, target_fps)
                time_before_game_loop = time.time()
                print(f"Battery unused: {battery_unused}%, CPU unused: {cpu_unused}%, VRAM unused: {vram_unused}%, Optimization index: {optimization_index},fps:{fps}")
                
            if fps < target_fps:
                fps += 1
            elif fps > target_fps:
                fps -= 1
            else:
                fps = target_fps

            # Previous temporary solution to adjust the snake's speed based on the target FPS,
            # now replaced with a more dynamic approach.

            # if target_fps >= 48 and target_fps <= 60 and init_velocity != 7:
            #     init_velocity = 7
            #     # print("12")
            # elif target_fps <48 and target_fps >= 30 and init_velocity != 12:
            #     init_velocity = 12
            # elif target_fps < 30 and init_velocity != 16:
            #     init_velocity = 16

            init_velocity = BASE_VELOCITY + difficulty_velocity_change + init_velocity_change
            
            # Works according to game difficulty
            if difficulty_velocity_change != 0:
                floor = BASE_VELOCITY + difficulty_velocity_change
                if init_velocity < floor:
                    init_velocity = floor
                    init_velocity_change = 0

            # Sync init_velocity to both velocity_x and velocity_y
            if velocity_x != 0:
                velocity_x = init_velocity if velocity_x > 0 else -init_velocity
            if velocity_y != 0:
                velocity_y = init_velocity if velocity_y > 0 else -init_velocity

            plot_snake(game_window, blue, s_lst, snake) # Draw the snake

            fade_in_text('Score: ' + str(score)+ f' Highscore: {h_score}', green, 12, 10, key="score-panel", duration=0.5)

            # FPS indicator, green means constant frames and yellow means dynamic fps
            fade_in_text(str(fps), (yellow if Dynamic_FPS else green), leftover_pixels(str(fps), leftover=3), 7, key="current-fps", duration=0.5)
            
            # Debug/Test Mode State Indication
            if Dynamic_FPS:
                if time.time()-Dynamic_FPS_time_start < 0.5:
                    load_text("Debug: Dynamic FPS Enabled", green, 10, 575, bold = False)
            else:
                if time.time()-Dynamic_FPS_time_start < 0.5:
                    load_text("Debug: Dynamic FPS Disabled", red, 10, 575, bold = False)

            # Debug/Test Mode State Indication
            if testing_mode:
                if time.time()-testing_mode_time_start < 0.5:
                    load_text("Debug: Test Mode Enabled", green, 10, 575, bold = False)
            else:
                if time.time()-testing_mode_time_start < 0.5:
                    load_text("Debug: Test Mode Disabled", red, 10, 575, bold = False)

            # Difficulty Mode State Indication
            difficulty = (
                "Easy"
                if apple_collrate == 16
                else "Medium"
                if apple_collrate == 12
                else "Hard"
                if apple_collrate == 8
                else "Ultra-Hard"
                if apple_collrate == 4
                else "not known"
            )
            color = (
                green
                if difficulty == "Easy"
                else yellow
                if difficulty == "Medium"
                else orange
                if difficulty == "Hard"
                else red
                if difficulty == "Ultra-Hard"
                else yellow
            )

            if time.time()-difficulty_mode_change_time_start < 1:
                load_text(f"Set {username}'s Difficulty Mode to {difficulty}", color, 10, 575, bold = False)

            if time.time()-independence_month_toggle_time_start < 1:
                load_text(f"Debug: Independence Month State is set to {is_independence_month}", color, 10, 575, bold = False)

            if pause_game:
                time_paused += pause_window()
                pause_game = False

        pygame.display.update()

    pygame.quit()
    sys.exit()


def main():
    """Main Function, where the whole game comes up together!"""
    menu_screen()
    game_loop()
    


if __name__ == "__main__":
    main()
