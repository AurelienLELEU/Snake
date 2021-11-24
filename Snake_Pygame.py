import random
import pygame
import tkinter as tk

height = width = 0
speed = 15


def menu():
    main_window = tk.Tk()
    main_window.title("Main Menu")

    global height, width, speed
    label = tk.Label(main_window, text="")

    height = tk.IntVar()
    width = tk.IntVar()
    speed = tk.IntVar()

    labelheight = tk.Label(main_window, text="Height ?")
    entryheight = tk.Entry(main_window, textvariable=height)
    labelwidth = tk.Label(main_window, text="Width ?")
    entrywidth = tk.Entry(main_window, textvariable=width)
    labelspeed = tk.Label(main_window, text="Speed ?")
    entryspeed = tk.Entry(main_window, textvariable=speed)

    def go():
        main_window.destroy()
        jeu()

    play_button = tk.Button(main_window, text="Play", command=go)

    labelwidth.grid(row=1, column=0)
    entrywidth.grid(row=1, column=1)
    labelheight.grid(row=2, column=0)
    entryheight.grid(row=2, column=1)
    labelspeed.grid(row=3, column=0)
    entryspeed.grid(row=3, column=1)

    label.grid(row=4)

    play_button.grid(row=5, column=0, columnspan=2)

    tk.mainloop()


def jeu():
    pygame.init()

    dis_width = 640
    dis_height = 420

    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (100, 185, 230)

    if int(width.get()) >= dis_width and int(height.get()) >= dis_height:
        dis_width = int(width.get())
        dis_height = int(height.get())

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    snake_block = 10

    font_style = pygame.font.SysFont("times new roman", 25)
    score_font = pygame.font.SysFont("times new roman", 35)

    def your_score(score):
        value = score_font.render("Your Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def our_snake(s_b, snake_list):
        for x in snake_list:
            pygame.draw.ellipse(dis, blue, [x[0], x[1], s_b, s_b])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    def gameloop(snk_speed):
        key = 0
        snake_speed = init_speed = snk_speed
        snake_list = []

        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close:
                dis.fill(black)
                message("You Lost! Press C to Play Again or Q to Quit", red)
                your_score(snake_speed - init_speed)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameloop(speed.get())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if key != 2:
                            x1_change = -snake_block
                            y1_change = 0
                            key = 1
                    elif event.key == pygame.K_RIGHT:
                        if key != 1:
                            x1_change = snake_block
                            y1_change = 0
                            key = 2
                    elif event.key == pygame.K_UP:
                        if key != 4:
                            y1_change = -snake_block
                            x1_change = 0
                            key = 3
                    elif event.key == pygame.K_DOWN:
                        if key != 3:
                            y1_change = snake_block
                            x1_change = 0
                            key = 4

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            dis.fill(black)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_head = [x1, y1]
            snake_list.append(snake_head)

            if len(snake_list) > (snake_speed - init_speed + 1):
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            our_snake(12, snake_list)
            your_score(snake_speed - init_speed)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                snake_speed += 1

            clock.tick(snake_speed)

        pygame.quit()
        quit()

    if speed.get() > 14:
        gameloop(speed.get())
    else:
        speed.set(15)
        gameloop(speed.get())


menu()
