import pygame
import random
import os
import sys
import time
import datetime

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

GAME_VERSION = "AppleCore v1.3.5"
snake = 30
scr = []
today_date = datetime.date.today()
is_independence_day = (today_date.month == 8 and today_date.day == 14)
mute_music = False

# display
game_window = pygame.display.set_mode((900, 600))
icon = pygame.image.load(resource_path('assets/appicon.png'))
icon = pygame.transform.scale(icon, (32, 32)).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_VERSION)
myimg = pygame.image.load(resource_path('assets/images.png'))
myimg = pygame.transform.scale(myimg, (900, 600)).convert_alpha()
go = pygame.image.load(resource_path('assets/g_over.png'))
go = pygame.transform.scale(go, (900, 600)).convert_alpha()
bk = pygame.image.load(resource_path('assets/back.png'))
bk = pygame.transform.scale(bk, (900, 600)).convert_alpha()
apl = pygame.image.load(resource_path('assets/app.png'))
apl = pygame.transform.scale(apl, (snake, snake)).convert_alpha()
# s_i = pygame.image.load(resource_path('assets/sicon.png'))
# si = pygame.transform.scale(s_i, (43, 43)).convert_alpha()
setting_page = pygame.image.load(resource_path('assets/settingpage.png'))
setting_page = pygame.transform.scale(setting_page, (900, 600)).convert_alpha()

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
if os.path.exists("assets/user_info.txt"):
    with open(resource_path("assets/user_info.txt")) as f:
        user_name = f.read()[2:8]
else:
    with open(resource_path("assets/user_info.txt"),"w") as f:
        f.write("")
        user_name = None
# user_name = open(resource_path("assets/user_info.txt")).read()[2:8]

text_input = ""

# snake appearing function
def plot_snake(game_window, color, s_lst, snake):
    for x, y in s_lst:
        pygame.draw.rect(game_window, color, pygame.Rect(x, y,snake,snake), 20)

clock = pygame.time.Clock()

# controlling user input (text)
def usertext(event):
    if event.key == pygame.K_BACKSPACE:
        if text_input:
            text_input=text_input[:-1]
        print(text_input)
    else:
        text_input+=event.unicode
        print(text_input)

# font
# printing text on game
def stext(text, color, x, y, b=False):
    """
    Shows Text on Screen
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
                    pygame.mixer.music.load("assets/b.mp3")
                    pygame.mixer.music.play(-1)
                return quit_game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return quit_game
            # elif elapsed >= 2:

        pygame.display.update()
    clock.tick(30)

def Pause_Window():
    quit_game = False
    s_time = time.time()
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                if not mute_music:
                    pygame.mixer.music.load("assets/b.mp3")
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

def stp():
    allowuinput = False
    quit_game = False
    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(setting_page, (0, 0))
        stext("  "+user_name, blue, 245, 95)
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

def hpage():
    if not mute_music:
        pygame.mixer.music.load("assets/c.mp3")
        pygame.mixer.music.play(-1)
    quit_game = False
    while not quit_game:
        game_window.fill((220, 200, 240))
        game_window.blit(myimg, (0, 0))
        # game_window.blit(si, (817, 56))
        # stext('Pyth0n wants to eat some apples...'.title(), yellow, 200, 150)
        # stext("Hello "+user_name+"!".title(), blue, 510, 50, b=True)
        # stext('Help him out!!!'.title(), yellow, 300, 260)
        # stext('press the space bar to play :)', yellow, 250, 400, True)\
        stext(f'version: {GAME_VERSION[GAME_VERSION.index("v")+1:]}', yellow, 350, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    m_p = event.pos
                    if m_p[0] > 817 and m_p[0] < 845 and m_p[1] > 56 and m_p[1] < 90:
                        print('successful')
                        if not mute_music:
                            pygame.mixer.music.load("assets/settingsound.mp3")
                            pygame.mixer.music.play()
                        stp()
                        if not mute_music:
                            pygame.mixer.music.load("assets/c.mp3")
                            pygame.mixer.music.play(-1)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not mute_music:
                        pygame.mixer.music.load("assets/b.mp3")
                        pygame.mixer.music.play(-1)
                    gameloop()
        # stext('Pyth0n wants to eat some apples...'.title(), blue, 200, 150)
        pygame.display.update()
        clock.tick(30)

# game loop
def gameloop():
    global mute_music

    ctime = time.localtime()
    ctime = time.strftime("%H-%M-%S")
    time1 = None

    collrate = 12
    fps = 48
    if not os.path.exists(resource_path('assets/highscores.txt')):
        with open(resource_path('assets/highscores.txt'), 'w') as f:
            f.write('0\n0')
    with open(resource_path('assets/highscores.txt'), 'r') as f:
        list_of_highscore_and_appocity = f.read().split("\n")
        h_score = list_of_highscore_and_appocity[0]
        h_appocity = list_of_highscore_and_appocity[1]

    appocity = "0 apple/second"
    quit_game = False
    game_over = False

    score = 0

    food_x = random.randint(40, 800)
    food_y = random.randint(50, 500)
    green_food_x= random.randint(20,900)
    green_food_y= random.randint(30,525)
    snake = 30
    snake_x = random.randint(350,520)
    snake_y = random.randint(200,400)
    velocity_x = 0
    velocity_y = 0
    init_velocity = 8
    pause_game = False
    s_lst = []
    s_length = 1
    s_controler = 3
    time_paused = 0
    show_green_apple = random.choice([False, False, False, False, True])
    while not quit_game:
        if game_over:
            appocity = (round(score/time_taken_to_score,2)) if time_taken_to_score != 0 else None
            # Checking if the current appocity is greater than the highest appocity and updating it if necessary
            if appocity is not None and (appocity) > float(h_appocity):
                h_appocity = str(appocity)
                list_of_highscore_and_appocity[1] = str(appocity)
            
            # Checking if the current score is greater than the highscore and updating it if necessary
            if score > int(h_score):
                h_score = str(score)
                list_of_highscore_and_appocity[0] = str(score)

            with open(resource_path('assets/highscores.txt'), 'w') as f:
                # f.write(str(h_score)+f.read()[0:f.read().index("\n")])
                f.write("\n".join(list_of_highscore_and_appocity))
            # with open(resource_path("assets/highscores.txt")) as i:
            #     h_appocity = int(i.read()[i.read().index("\n")+1:])
            # print(h_appocity)
            show_green_apple = random.choice([False, False, False, False, True])
            game_window.fill(white)
            game_window.blit(go, (0, 0))
            stext('           PRESS ENTER TO CONTINUE',
                  red, 900/2-300, 600/2+125)
            stext(f'Highscore: {h_score}                                 Highest Appocity: {h_appocity}', blue, 50, 7)
            stext('Made By Hashir Ahmad', blue, 300, 500+20)
            scr.append(score)
            stext(f'your score is : {score}, achieved in {time_taken_to_score} seconds'.capitalize()
            ,yellow, 900/2-300+30, 600/2+100+30+20)
            stext(f'Appocity = {appocity if appocity is not None else "undefined"} {"apple" if appocity == 1 else "apples"}/second'.capitalize()
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
                            pygame.mixer.music.load("assets/a.mp3")
                            pygame.mixer.music.play(-1)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_o:
                        if not mute_music:
                            pygame.mixer.music.load("assets/b.mp3")
                            pygame.mixer.music.play(-1)
                        scr.clear()
                        gameloop()
                    elif event.key == pygame.K_HOME:
                        scr.clear()
                        hpage()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                        init_velocity += 2
                    elif event.key == pygame.K_c:
                        if init_velocity != 0 or init_velocity != 1:
                            init_velocity -= 2
                        else:
                            init_velocity = 0
                    elif event.key == pygame.K_o:
                        game_over = True
                        if time1 is not None:
                            time_taken_to_score = round(time.time() - time1, 2) - time_paused
                        else:
                            time_taken_to_score = 0
                        if not mute_music:
                            pygame.mixer.music.load("assets/a.mp3")
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
            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x-food_x) < collrate and abs(snake_y-food_y) < collrate:
                score += 10
                # print(s_lst)
                food_x = random.randint(40, 600)
                food_y = random.randint(40, 400)
                s_length += s_controler
            game_window.fill(white)
            game_window.blit(bk, (0, 0))

            stext('Score: ' + str(score)+ f' Highscore: {h_score}', green, 12, 30)
            if not pause_game:
                stext(ctime, green, 12+400, 30)

            ctime = time.localtime()
            ctime = time.strftime("%H-%M-%S")

            head = []
            head.append(snake_x)
            head.append(snake_y)
            s_lst.append(head)

            if len(s_lst) > s_length:
                del s_lst[0]

            if head in s_lst[:len(s_lst)-1]:
                game_over = True
                if time1 is not None:
                    time_taken_to_score = round(time.time() - time1, 2)
                else:
                    time_taken_to_score = 0

                if not mute_music:
                    pygame.mixer.music.load("assets/a.mp3")
                    pygame.mixer.music.play(-1)

            game_window.blit(apl, (food_x, food_y))
            
            if not is_independence_day:
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
                    pygame.mixer.music.load("assets/a.mp3")
                    pygame.mixer.music.play(-1)

                # pygame.mixer.music.play() if not mute_music else None

            plot_snake(game_window, blue, s_lst, snake)

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == '__main__':
    hpage()
