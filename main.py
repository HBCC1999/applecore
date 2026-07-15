"""Applecore (Standard) v3.7-alpha.1
Developed by HBCC1999
Textures: Some are made by the author and some are AI-generated.
Audio: From Youtube Studio
----------------------------------------------------------------
"""
# using pygame-ce instead of pygame because pygame-ce is more up to date and has more features than pygame
import pygame
import random
import os
import sys
import time
import datetime
import psutil as p

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

GAME_VERSION = __doc__.split("\n")[0]
print(__doc__, end="")
snake = 30
DEFAULT_FPS = 60
scr = []
today_date = datetime.date.today()
is_independence_day = (today_date.month == 8 and today_date.day == 14)
mute_music = False
target_fps = DEFAULT_FPS
optimization_constant = 2.8 #This is a constant that is based of to calculate optimization index in gameloop its value is based of 70/25, where 25 is optimization index
# that implies that the system is optimized enough to run the game at 70% of display refresh rate and this is the highest in the middle tier fps

# display
game_window = pygame.display.set_mode((900, 600))
BASE_VELOCITY = 384 # (8 * fps:=48) pixels per second, regardless of the frames
icon = pygame.image.load(resource_path('assets/appicon.png'))
icon = pygame.transform.scale(icon, (32, 32)).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_VERSION)
myimg = pygame.image.load(resource_path('assets/menu_screen_image.png'))
myimg = pygame.transform.scale(myimg, (900, 600)).convert_alpha()
go = pygame.image.load(resource_path('assets/game_over_screen.png'))
go = pygame.transform.scale(go, (900, 600)).convert_alpha()
bk = pygame.image.load(resource_path('assets/background_image.png'))
bk = pygame.transform.scale(bk, (900, 600)).convert_alpha()
apl = pygame.image.load(resource_path('assets/apple.png'))
apl = pygame.transform.scale(apl, (snake, snake)).convert_alpha()
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
yellow = (240, 250, 5)
time1 = 0
time_taken_to_score = 0

# user name
if os.path.exists(resource_path("assets/user_info.txt")):
    with open(resource_path("assets/user_info.txt")) as f:
        user_name = f.read()[2:8]
else:
    with open(resource_path("assets/user_info.txt"),"w") as f:
        f.write("")
        user_name = 'player'
# user_name = open(resource_path("assets/user_info.txt")).read()[2:8]

# Better in-game-info management, now the game will check if the in-game-info
# file is corrupted or not and if it is corrupted then it will reset the file to default values
gamefilecontent = ""
if os.path.exists(resource_path('assets/highscores.txt')):
    with open(resource_path('assets/highscores.txt'), 'r') as f:
        gamefilecontent = f.read()
in_game_info = gamefilecontent.split("\n")

first_line_of_file = gamefilecontent.split("\n")[0] if gamefilecontent else ""

should_reset_gamefilecontent = (
    not first_line_of_file.isdigit() or
    not in_game_info[1].replace('.', '', 1).isdigit() or
    not len(in_game_info)>3 or
    in_game_info[2] not in ('True', 'False')
)

if should_reset_gamefilecontent:
    with open(resource_path('assets/highscores.txt'), 'w') as f:
        f.write("0\n0\nFalse")
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
    if event.key == pygame.K_BACKSPACE:
        if text_input:
            text_input=text_input[:-1]
        print(text_input)
    else:
        text_input+=event.unicode
        print(text_input)

# font
# printing text on game
def load_text(text, color, x, y, b=False):
    """
    Shows Text on Window, b is for bold text, if b is True then the text will be bold, if b is False then the text will be normal.
    """
    if not b:
        font = pygame.font.SysFont(None, 40, italic=True)
        txt = font.render(text, True, color)
        game_window.blit(txt, (x, y))
    elif b:
        font = pygame.font.SysFont(None, 40, bold=True)
        txt = font.render(text, True, color)
        game_window.blit(txt, (x, y))

def independendence_day_page():
    """An easter egg to celibrate Pakistan's Independence day on 14th August. (any year)"""
    pygame.event.clear()
    start_time = time.time()
    quit_game = False
    while not quit_game:
        game_window.fill((220, 200, 240))
        elapsed = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                    pygame.mixer.music.play(-1)
                return quit_game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return quit_game
            # elif elapsed >= 2:

        pygame.display.update()
    clock.tick(30)

def Pause_Window():
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

def settingpage():
    """Settings page, coming soon!"""
    allowuinput = False
    quit_game = False
    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(setting_page, (0, 0))
        load_text("  "+user_name, blue, 245, 95)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
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

        pygame.display.update()
    clock.tick(30)

def menuscreen():
    """Main menu screen, where the game starts and user can access settings or start the game."""
    if not mute_music:
        pygame.mixer.music.load(resource_path("assets/menu_screen_music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    quit_game = False
    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(myimg, (0, 0))
        # game_window.blit(si, (817, 56))
        # load_text('Pyth0n wants to eat some apples...'.title(), yellow, 200, 150)
        # load_text("Hello "+user_name+"!".title(), blue, 510, 50, b=True)
        # load_text('Help him out!!!'.title(), yellow, 300, 260)
        # load_text('press the space bar to play :)', yellow, 250, 400, True)\
        load_text(f'version: {GAME_VERSION[GAME_VERSION.index("v"):]}', yellow, 320, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    m_p = event.pos
                    if m_p[0] > 817 and m_p[0] < 845 and m_p[1] > 56 and m_p[1] < 90:
                        print('successful')
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/settings_page_music.mp3"))
                            pygame.mixer.music.play()
                        settingpage()
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/menu_screen_music.mp3"))
                            pygame.mixer.music.play(-1)

            elif event.type == pygame.KEYDOWN:
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

    # ctime = time.localtime()
    # ctime = time.strftime("%H-%M-%S")
    # starting_time_for_timer = time.time()
    # timer = f"{}:{}:{time.time()-starting_time_for_timer}"
    time1 = None

    collrate = 12
    trailing_buffer = 5
    fps = DEFAULT_FPS

    h_score = in_game_info[0]
    h_appocity = in_game_info[1]

    appocity = "0 apple/second"
    quit_game = False
    game_over = False

    score = 0

    # entity - related variables and constants
    food_x = random.randint(40, 800)
    food_y = random.randint(50, 500)
    green_food_x= random.randint(20,900)
    green_food_y= random.randint(30,525)
    snake = 30
    snake_x = random.randint(350,520)
    snake_y = random.randint(200,400)
    velocity_x = 0
    velocity_y = 0
    init_velocity = BASE_VELOCITY
    pause_game = False
    s_lst = []
    s_length = 1
    s_controler = 3
    time_paused = 0
    show_green_apple = random.choice([False, False, False, False, True])
    time_before_game_loop = time.time()
    init_velocity_change = 0
    while not quit_game:
        dt = clock.tick(fps) / 1000.0  # Amount of seconds between each loop/frame and seconds because i follow SI units.
        dt = min(dt, 0.05) # Cap it at 50ms. So no stutters and wierd teleportation after toggling pause_menu
        if game_over:
            fps = 30
            appocity = (round(score/time_taken_to_score,2)) if time_taken_to_score != 0 else None
            # Checking if the current appocity is greater than the highest appocity and updating it if necessary
            if appocity is not None and (appocity) > float(h_appocity):
                h_appocity = str(appocity)
                in_game_info[1] = str(appocity)
            
            # Checking if the current score is greater than the highscore and updating it if necessary
            if score > int(h_score):
                h_score = str(score)
                in_game_info[0] = str(score)
            
            if in_game_info[2] != str(Dynamic_FPS):
                in_game_info[2] = str(Dynamic_FPS)

            with open(resource_path('assets/highscores.txt'), 'w') as f:
                # f.write(str(h_score)+f.read()[0:f.read().index("\n")])
                f.write("\n".join(in_game_info))

            # with open(resource_path("assets/highscores.txt")) as i:
            #     h_appocity = int(i.read()[i.read().index("\n")+1:])
            # print(h_appocity)
            show_green_apple = random.choice([False, False, False, False, True])
            game_window.fill(white)
            game_window.blit(go, (0, 0))
            load_text('           PRESS ENTER TO CONTINUE',
                  red, 900/2-300, 600/2+125)
            load_text(f'Highscore: {h_score}                                 Highest Appocity: {h_appocity}', blue, 50, 7)
            load_text('Made By Hashir Ahmad', blue, 300, 500+20)
            scr.append(score)
            load_text(f'your score is : {score}, achieved in {time_taken_to_score} seconds'.capitalize()
            ,yellow, 900/2-300+30, 600/2+100+30+20)
            load_text(f'Appocity = {appocity if appocity is not None else "undefined"} {"apple" if appocity == 1 else "apples"}/second'.capitalize()
            ,yellow, 900/2-300+40, 600/2+100+60+20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True

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
                            pygame.mixer.music.load(resource_path("assets/main_game_music.mp3"))
                            pygame.mixer.music.play(-1)
                        scr.clear()
                        gameloop()
                    elif event.key == pygame.K_HOME:
                        scr.clear()
                        menuscreen()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    time_taken_to_score = (round(time.time() - time1, 2) - time_paused) if time1 is not None else 0
                    appocity = (round(score/time_taken_to_score,2)) if time_taken_to_score != 0 else None
                    # Checking if the current appocity is greater than the highest appocity and updating it if necessary
                    if appocity is not None and (appocity) > float(h_appocity):
                        h_appocity = str(appocity)
                        in_game_info[1] = str(appocity)
                    print(time_taken_to_score, appocity, h_appocity)
                    
                    # Checking if the current score is greater than the highscore and updating it if necessary
                    if score > int(h_score):
                        h_score = str(score)
                        in_game_info[0] = str(score)
                    
                    if in_game_info[2] != str(Dynamic_FPS):
                        in_game_info[2] = str(Dynamic_FPS)

                    with open(resource_path('assets/highscores.txt'), 'w') as f:
                        # f.write(str(h_score)+f.read()[0:f.read().index("\n")])
                        f.write("\n".join(in_game_info))

                    quit_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_game = True
                        time_paused = Pause_Window()
                    if event.key == pygame.K_F1:
                        mute_music = not mute_music
                        if mute_music:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    if event.key == pygame.K_F3:
                        Dynamic_FPS = not Dynamic_FPS
                        if not Dynamic_FPS:
                            target_fps = DEFAULT_FPS if display_refresh_rate >= DEFAULT_FPS else display_refresh_rate
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and velocity_x == 0:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and velocity_x == 0:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and velocity_y == 0:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and velocity_y == 0:
                        velocity_y = init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_i:
                        if random.choice([1,2,3]) == 2:
                            score += 10
                        elif random.choice([1,2,3,4,5,6,7,8,9,10]) == 5:
                            score+=20
                    elif event.key == pygame.K_v:
                        init_velocity_change += 48
                    elif event.key == pygame.K_c:
                        if init_velocity != 0 or init_velocity != 1:
                            init_velocity_change -= 48
                        else:
                            init_velocity_change = 0
                    elif event.key == pygame.K_o:
                        game_over = True
                        if time1 is not None:
                            time_taken_to_score = round(time.time() - time1, 2) - time_paused
                        else:
                            time_taken_to_score = 0
                        if not mute_music:
                            pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                            pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_x:
                        s_controler += 3
                    elif event.key == pygame.K_z:
                        s_controler -= 3
                    elif event.key == pygame.K_e:
                        collrate = 16
                    elif event.key == pygame.K_m:
                        collrate = 9
                        s_controler = 4
                    elif event.key == pygame.K_h:
                        collrate = 6
                        s_controler = 5
                    elif event.key == pygame.K_u:
                        collrate = 4
                        s_controler = 6
                        init_velocity = 9

            if (velocity_x != 0 or velocity_y !=0) and time1 is None:
                time1 = time.time()

            velocity_x_f = (velocity_x * dt)
            velocity_y_f = (velocity_y * dt)

            snake_x += (velocity_x_f)
            snake_y += (velocity_y_f)

            if abs(snake_x-food_x) < collrate and abs(snake_y-food_y) < collrate:
                score += 10
                # print(s_lst)
                food_x = random.randint(40, 600)
                food_y = random.randint(40, 400)
                s_length += s_controler
            game_window.fill(white)
            game_window.blit(bk, (0, 0))

            load_text('Score: ' + str(score)+ f' Highscore: {h_score}', green, 12, 10)
            # FPS indicator, green means constant frames and yellow means dynamic fps
            load_text(str(fps), (yellow if Dynamic_FPS else green), 12+850, 7)

            # ctime = time.localtime()
            # ctime = time.strftime("%H-%M-%S")

            head = []
            head.append(int(snake_x))
            head.append(int(snake_y))
            s_lst.append(head)

            if len(s_lst) > s_length:
                del s_lst[0]
            
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
                if time1 is not None:
                    time_taken_to_score = round(time.time() - time1, 2)
                else:
                    time_taken_to_score = 0

                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                    pygame.mixer.music.play(-1)

            game_window.blit(apl, (food_x, food_y))

            if is_independence_day:
                # 20% chance for the green apple to appear(only on 14 August)
                if show_green_apple:
                    pygame.draw.rect(game_window, (0, 130, 0),
                    pygame.Rect(green_food_x,green_food_y,snake,snake))
                    if abs(snake_x-green_food_x) < collrate and abs(snake_y-green_food_y) < collrate:
                        pygame.mixer.music.stop()
                        if independendence_day_page():
                            break
                        else:
                            pygame.event.clear()

            if snake_x < 0 or snake_x > 900 or snake_y < 0 or snake_y > 600:
                game_over = True
                if time1 is not None:
                    time_taken_to_score = round(time.time() - time1, 2)
                else:
                    time_taken_to_score = 0

                if not mute_music:
                    pygame.mixer.music.load(resource_path("assets/game_over_music.mp3"))
                    pygame.mixer.music.play(-1)

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

            init_velocity = BASE_VELOCITY + init_velocity_change
            # print(init_velocity)

            plot_snake(game_window, blue, s_lst, snake)

        pygame.display.update()

    pygame.quit()
    sys.exit()

def main():
    """Main Function, where the whole game comes up together!"""
    menuscreen()

if __name__ == '__main__':
    main()
