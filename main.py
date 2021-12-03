import tkinter
import csv
import random

BACKGROUND_COLOR = "#B1DDC6"
new_word = ""
number_of_views = 0
score = 0
timer = None
# ---------------------------- CONVERTING CSV DATA TO LIST ------------------------------- #

with open("./data/french_words.csv") as file:
    raw_data = csv.reader(file)
    data = list(raw_data)


# ---------------------------- FUNCTIONS ------------------------------- #

def draw_words():
    target = random.choice(data)
    return target


def draw_new_word_right():
    global new_word
    global score
    new_word = draw_words()
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(language_selection, text="French", fill="black")
    canvas.itemconfig(language_text, text=new_word[0], fill="black")
    button_right.config(state=tkinter.DISABLED)
    button_left.config(state=tkinter.DISABLED)
    timer_start(5)
    increase_score()
    window.after(5000, show_english)


def draw_new_word_wrong():
    global new_word
    new_word = draw_words()
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(language_selection, text="French", fill="black")
    canvas.itemconfig(language_text, text=new_word[0], fill="black")
    button_right.config(state=tkinter.DISABLED)
    button_left.config(state=tkinter.DISABLED)
    timer_start(5)
    window.after(5000, show_english)


def update_text_below():
    canvas.itemconfig(text_below_word_1, text="Did you get it right ? ", fill="white")
    canvas.itemconfig(text_below_word_2, text="", fill=BACKGROUND_COLOR)


def show_english():
    global number_of_views
    canvas.itemconfig(text_below_word_2, text="")
    button_right.config(state = tkinter.NORMAL)
    button_left.config(state = tkinter.NORMAL)

    if number_of_views == 0:
        canvas.itemconfig(card, image=card_back_img)
        canvas.itemconfig(language_selection, text="English", fill="white")
        canvas.itemconfig(language_text, text=target_words[1], fill="white")
        update_text_below()
        number_of_views += 1
    else:
        canvas.itemconfig(card, image=card_back_img)
        canvas.itemconfig(language_selection, text="English", fill="white")
        canvas.itemconfig(language_text, text=new_word[1], fill="white")
        update_text_below()


def timer_start(remaining):
    global timer
    canvas.itemconfig(text_below_word_1, text="showing answer in", fill="black")
    canvas.itemconfig(text_below_word_2, text=f"{remaining}", fill="black")
    timer = window.after(1000, timer_start, remaining - 1)
    if remaining == 1:
        window.after_cancel(timer)


def increase_score():
    global score, highscore
    score += 1
    score_label.config(text=f"Score: {score}")
    if score > highscore:
        highscore = score
        highscore_label.config(text=f"Highscore : {score}")
        with open("./data/highscore.txt", mode="w") as data_file:
            data_file.write(str(highscore))


# ---------------------------- HIGHSCORE IMPORT ------------------------------- #
try:
    with open("./data/highscore.txt") as file:
        highscore = int(file.read())


except FileNotFoundError:
    with open("./data/highscore.txt", mode="w") as file:
        highscore = str(0)
        file.write(highscore)
# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Flashy")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR,height = 700 , width = 900)

# ---------------------------- SCOREBOARD SETUP SETUP ------------------------------- #
score_label = tkinter.Label(text=f"Score : {score} ", font="Ariel 30 italic", bg=BACKGROUND_COLOR)
score_label.grid(column=0, row=0)

highscore_label = tkinter.Label(text=f"Highscore : {highscore} ", font="Ariel 30 italic", bg=BACKGROUND_COLOR)
highscore_label.grid(column=1, row=0)

# ---------------------------- CANVAS SETUP ------------------------------- #
target_words = draw_words()

canvas = tkinter.Canvas(width=800, height=525, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = tkinter.PhotoImage(file="./images/card_front.png")
card_back_img = tkinter.PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 262, image=card_front_img)

language_selection = canvas.create_text(400, 130, text="French", font="Ariel 40 italic")
language_text = canvas.create_text(400, 250, text=target_words[0], font="Ariel 60 italic")
text_below_word_1 = canvas.create_text(400, 350, text=f"showing answer in", font="Ariel 30 italic")
text_below_word_2 = canvas.create_text(400, 400, text=5, font="Ariel 30 italic")

canvas.grid(column=0, row=1, columnspan=2)
timer_start(5)
window.after(5000, show_english)
# ---------------------------- BUTTON SETUP ------------------------------- #
button_right_img = tkinter.PhotoImage(file="./images/right.png", )
button_right = tkinter.Button(image = button_right_img , highlightthickness=0,command = draw_new_word_right,
                              state = tkinter.DISABLED)
button_right.grid(column=1, row=2)

button_left_img = tkinter.PhotoImage(file="./images/wrong.png")
button_left = tkinter.Button(image = button_left_img ,highlightthickness=0, command = draw_new_word_wrong,
                             state = tkinter.DISABLED)
button_left.grid(column=0, row=2)

window.mainloop()
