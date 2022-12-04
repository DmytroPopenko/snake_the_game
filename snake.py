from tkinter import *
from time import sleep
import random


# Window 1
window_1 = Tk()
window_1.title('Name')
window_1.geometry("250x150")
window_1.resizable(0,0)

player_name = ''
def button_click():
    global player_name
    player_name = entry_1.get()
    if player_name:
        window_1.destroy()
        print(f"Player name: {player_name}")


label_name = Label(window_1, text="Enter player name:")
label_name.place(relx=0.5, rely=0.25, anchor="c")
entry_1 = Entry(window_1, width='30')
entry_1.place(relx=0.5, rely=0.4, anchor="c")
start_button = Button(text="Start", relief = "groove", command=button_click)
start_button.place(relx=.5, rely=.65, anchor="c")
window_1.mainloop()


# Window 2
window_2 = Tk()
window_2.title('Use arrows to move')
window_2.resizable(0,0) # Незмінне
window_2.wm_attributes("-topmost", 1) # Поверх усіх вікон
snake_sec = 20
canvas = Canvas(window_2, width=500, height=500, bd=0, bg="#2b2b2b", highlightthickness=0)
canvas.pack()
window_2.update()

# Координати голови
head_x = 12
head_y = 12
core = [] # координати ядра
snake_list = [] # Список з кординатами кожного сигменту
length = 5 # Довжина змійки
score = 0 # Рахунок

# Змінні для ругу/навігації
nav_x = 0
nav_y = 0
game_running = True
err = 0 # Перевірка на помилковий напрям під час руху


def create_core(canvas, core):
    # Малювання ядра
    global snake_list
    exx = True
    while exx:
        count = 0
        dig1 = random.randrange(25)
        dig2 = random.randrange(25)
        exx = False
        for i in range(len(snake_list)):
            if snake_list[i][0] == dig1 and snake_list[i][1] == dig2:
                exx = True

    core_id = canvas.create_oval(
        dig1*snake_sec, dig2*snake_sec,
        dig1*snake_sec+snake_sec,
        dig2*snake_sec+snake_sec,
        fill='#8f936c'
        )
    core.append([dig1, dig2, core_id])


def painting(canvas, x, y):
    # Малювання фрагментів змійки
    global snake_list
    sec_id = canvas.create_rectangle(x*snake_sec, y*snake_sec, x*snake_sec+snake_sec, y*snake_sec+snake_sec, fill='#909090')
    snake_list.append([x, y, sec_id])


def check_core():
    # Функція перевірки чи є на шляху ядро
    global core, head_y, head_x, length, cursor, score
    for j in range(len(core)):
        if core[j][0] == head_x and core[j][1] == head_y:
            canvas.delete(core[j][2])
            length += 1
            score += 150
            window_2.title("Score: {}".format(score))
            cursor = core.pop(j)
            create_core(canvas, core)



def move(event):
    # Функція руху
    global nav_x, nav_y, head_y, head_x, err
    err = 0
    if event.keysym == "Up" and nav_y != 1:
        nav_x = 0
        nav_y = -1
        del_func()
    elif event.keysym == "Down"  and nav_y != -1:
        nav_x = 0
        nav_y = 1
        del_func()
    elif event.keysym == "Left"  and nav_x != 1:
        nav_x = -1
        nav_y = 0
        del_func()
    elif event.keysym == "Right" and nav_x != -1:
        nav_x = 1
        nav_y = 0
        del_func()
    else:
        err += 1
    if err == 0:
        head_x += nav_x
        head_y += nav_y
        painting(canvas, head_x, head_y)
        del_func()
    check_core()


def del_func():
    # Функція видалення змійки
    if len(snake_list) >= length:
        cursor = snake_list.pop(0)
        canvas.delete(cursor[2])


canvas.bind_all("<KeyPress-Left>", move)
canvas.bind_all("<KeyPress-Right>", move)
canvas.bind_all("<KeyPress-Up>", move)
canvas.bind_all("<KeyPress-Down>", move)
painting(canvas, head_x, head_y) # Початкові координати
create_core(canvas, core)


def game_over():
    global game_running
    game_running = False
    print("Game over!")


def check_if_borders():
    if head_x >= 25 or head_x < 0 or head_y >= 25 or head_y < 0:
        game_over()


def check_we_touch_self(f_x, f_y):
    global game_running
    if not (nav_x == 0 and nav_y == 0):
        for i in range(len(snake_list)):
            if snake_list[i][0] == f_x and snake_list[i][1] == f_y:
                game_running = False


while game_running:
    del_func()
    check_we_touch_self(head_x + nav_x, head_y + nav_y)
    head_x += nav_x
    head_y += nav_y
    painting(canvas, head_x, head_y)
    check_if_borders()

    check_core()
    window_2.update_idletasks()
    window_2.update()
    sleep(0.13)
    if (game_running == False):
       window_2.destroy()


window_2.mainloop()


# Window 3
window_3 = Tk()
window_3.title('Game over')
window_3.geometry("250x150")
window_3.resizable(0,0)

label_3 = Label(window_3, text="Game over\n{}, your score is\n{} points".format(player_name, score))
label_3.place(relx=0.5, rely=0.5, anchor="c")
window_3.mainloop()
