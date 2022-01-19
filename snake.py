from tkinter import *
import random
from time import sleep

#----Window1---------------------
name_c_p = ''
def click_button():
    global name_c_p
    name_c_p = entr1.get()
    wn1.destroy()
    print(f"Player name: {name_c_p}")

wn1 = Tk()
wn1.title('Name')
wn1.geometry("250x150")
wn1.resizable(0,0)

lb1 = Label(wn1, text="Enter player name:")
lb1.place(relx=0.5, rely=0.25, anchor="c")
entr1 = Entry(wn1, width='30')
entr1.place(relx=0.5, rely=0.4, anchor="c")
btn = Button(text="Start", relief = "groove", command=click_button)
btn.place(relx=.5, rely=.65, anchor="c")
wn1.mainloop()

#----Window2---------------------


wn2 = Tk()
wn2.title('Use arrows to move')
wn2.resizable(0,0) # Незмінне
wn2.wm_attributes("-topmost",1) # Поверх усіх вікон
snake_sec = 20
canvas = Canvas(wn2, width=500, height=500, bd=0, bg="#2b2b2b", highlightthickness=0)
canvas.pack()
wn2.update()

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
Game_Running = True

err = 0 # Перевірка на помилковий напрям під час руху


def create_core(canvas, core): # Малювання ядра
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

    core_id = canvas.create_oval(dig1*snake_sec, dig2*snake_sec,
                                dig1*snake_sec+snake_sec,dig2*snake_sec+snake_sec, fill='#8f936c')
    core.append([dig1, dig2, core_id])

def painting(canvas, x, y): # Малювання фрагментів змійки
    global snake_list
    sec_id = canvas.create_rectangle(x*snake_sec, y*snake_sec, x*snake_sec+snake_sec, y*snake_sec+snake_sec, fill='#909090')
    snake_list.append([x, y, sec_id])


def check_core(): # Функція перевірки чи є на шляху ядро
    global core, head_y, head_x, length, cursor, score
    for j in range(len(core)):
        if core[j][0] == head_x and core[j][1] == head_y:
            canvas.delete(core[j][2])
            length += 1
            score += 150
            wn2.title("Score: {}".format(score))
            cursor = core.pop(j)
            create_core(canvas, core)




def move(event): # Функція руху
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


def del_func(): # Функція видалення змійки
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
    global Game_Running
    Game_Running = False
    print("Game over!")

def check_if_borders():
    if head_x >= 25 or head_x < 0 or head_y >= 25 or head_y < 0:
        game_over()

def check_we_touch_self(f_x, f_y):
    global Game_Running
    if not (nav_x == 0 and nav_y == 0):
        for i in range(len(snake_list)):
            if snake_list[i][0] == f_x and snake_list[i][1] == f_y:
                Game_Running = False

while Game_Running:
    del_func()
    check_we_touch_self(head_x + nav_x, head_y + nav_y)
    head_x += nav_x
    head_y += nav_y
    painting(canvas, head_x, head_y)
    check_if_borders()

    check_core()
    wn2.update_idletasks()
    wn2.update()
    sleep(0.13)
    if (Game_Running == False):
       wn2.destroy()


wn2.mainloop()

#----Window3---------------------

wn3 = Tk()
wn3.title('Game over')
wn3.geometry("250x150")
wn3.resizable(0,0)

lb3 = Label(wn3, text="Game over\n{}, your score is\n{} points".format(name_c_p, score))
lb3.place(relx=0.5, rely=0.5, anchor="c")

wn3.mainloop()
