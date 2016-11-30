import pygame
from pygame.locals import *

from threading import Thread
from time import sleep
from sys import exit
from random import randint

from algorithm import core
from global_var import global_var as gv
from view import sc

def nop():
    pass

def main():

    global_init()

    btn_start = sc.Button(gv.g_btn_start_imgloc, gv.g_size_btn, gv.g_pos_btn_start)
    btn_about = sc.Button(gv.g_btn_about_imgloc, gv.g_size_btn, gv.g_pos_btn_about)

    surface_game()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        gv.g_screen.blit(gv.g_home_img, (0, 0))

        btn_start.update(surface_game)
        btn_about.update(surface_about)

        pygame.display.update()
        gv.g_clock.tick(30)

def global_init():

    pygame.init()

    # load icon and title
    pygame.display.set_icon(pygame.image.load(gv.g_icon_fileloc))
    pygame.display.set_caption(gv.g_wintitle)

    gv.g_screen = pygame.display.set_mode(gv.g_size_win)
    gv.g_clock = pygame.time.Clock()

    gv.g_home_img = sc.load_img(gv.g_home_img_fileloc, gv.g_size_win)

    # Load font
    gv.g_font = pygame.font.Font("other_res/ncsj.ttf", 18)
    gv.g_txt_w_thinking = gv.g_font.render("Thinking…",True, gv.g_white)
    gv.g_txt_b_thinking = gv.g_font.render("Thinking…",True, gv.g_black)

    # Move font
    default_font  = "other_res/ncsj.ttf"

    max_txt = pygame.font.Font(default_font,24)
    mid_txt = pygame.font.Font(default_font,22)
    min_txt = pygame.font.Font(default_font,20)
    for i in range(10):
        gv.g_num_tab += [max_txt.render(str(i),True, (180,180,180))]
    for i in range(10,100):
        gv.g_num_tab += [mid_txt.render(str(i),True, (180,180,180))]
    for i in range(100,256):
        gv.g_num_tab += [min_txt.render(str(i),True, (180,180,180))]

def surface_about():
    btn_back = sc.Button(gv.g_btn_back_imgloc, gv.g_size_btn, gv.g_pos_btn_back)

    about_bkgimg = sc.load_img(gv.g_surfaceback_img_fileloc, gv.g_size_win)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        gv.g_screen.blit(about_bkgimg, (-1, -1))
        if btn_back.update(nop) == 1:
            break
        pygame.display.update()
        gv.g_clock.tick(30)


def surface_game():
    grid_img = sc.load_img("img_res/grid.png", gv.g_size_win)
    w_img = sc.load_img("img_res/round_white.png", (24, 24))
    b_img = sc.load_img("img_res/round_black.png", (24, 24))
    think_img = sc.load_img("img_res/think.png", (120, 60))

    back_btn = sc.Button(gv.g_btn_gameback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_gameback)
    goback_btn = sc.Button(gv.g_btn_goback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goback)
    goahead_btn = sc.Button(gv.g_btn_goahead_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goahead)

    computer_pgsbar = sc.ProgressBar("img_res/round_white.png", (12, 12), (675, 50), 40)
    player_pgsbar = sc.ProgressBar("img_res/round_black.png", (12, 12), (720, 440), 40)

    gomoku_core = core.Core()
    input_info = sc.GetInput();


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        # Draw the backgroudn
        gv.g_screen.blit(grid_img, (0, 0))

        # Draw the piece
        sc.draw_table(gomoku_core, w_img, b_img)

        # Win/Lose is decided
        if gomoku_core.who_win != 0:
            one_more_img = sc.load_img("img_res/one_more_time.jpg", (100, 80))
            if gomoku_core.who_win == 1:
                win_img = sc.load_img("img_res/win.jpg", (130, 45))
            else:
                win_img = sc.load_img("img_res/win_2.png", (130, 45))
            gv.g_screen.blit(win_img, (300, 495))
            gv.g_screen.blit(one_more_img, (20, 420))

        # Win/lose is not decided
        else:
            # Computer
            if gomoku_core.busy == 1:

                gv.g_screen.blit(gv.g_txt_w_thinking, (670, 27))
                computer_pgsbar.draw()

            # Player
            else:
                input_status = input_info.scan()
                if input_status[0] == 1:
                    tab_pos = sc.pixpos_to_table((input_status[1], input_status[2]))
                    gomoku_core.player_take(tab_pos)

                gv.g_screen.blit(think_img, (680, 420))
                player_pgsbar.draw()

        if gomoku_core.busy == 0 and gomoku_core.index > 1:
            goback_btn.update(gomoku_core.go_back)
            goahead_btn.update(gomoku_core.go_ahead)

        if back_btn.update(nop) == 1:
            break
        pygame.display.update()
        gv.g_clock.tick(15)



if __name__ == "__main__":
    main()






















