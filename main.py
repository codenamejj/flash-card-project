import random
from tkinter import *
import pandas
import random

# ----------------------READ FROM CSV - Next Card------------------------------#

to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")

else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    if len(to_learn) > 0:
        current_card = random.choice(to_learn)
        canvas.after_cancel(flip_timer)
        canvas.itemconfig(word_text, text=current_card['French'], fill="black")
        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(canvas_image, image=front_image)
        flip_timer = window.after(3000, func=flip_card)
    else:
        canvas.itemconfig(word_text, text="Congratulations!", fill="black")
        canvas.itemconfig(title_text, font=20)
        canvas.itemconfig(title_text, text="You have completed a Milestone!", fill="black")


def remove_word():
    global current_card
    if len(to_learn) > 0:
        to_learn.remove(current_card)
        current_data = pandas.DataFrame(to_learn)
        current_data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    else:
        canvas.itemconfig(word_text, text="Congratulations!", fill="black")
        canvas.itemconfig(title_text, font=20)
        canvas.itemconfig(title_text, text="You have completed a Milestone!", fill="black")


def flip_card():
    global current_card
    if len(to_learn) > 0:
        canvas.itemconfig(canvas_image, image=back_image)
        canvas.itemconfig(word_text, text=current_card["English"], fill="white")
        canvas.itemconfig(title_text, text="English", fill="white")


# ----------------------UI------------------------------#
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")

right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

canvas = Canvas()
canvas.config(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 268, image=front_image)
canvas.grid(columnspan=2, column=0, row=0)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(columnspan=2, column=0, row=0)

# Buttons
wrong_button = Button(image=wrong_image)
clicked_wrong_button = wrong_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)
right_button = Button(image=right_image)
clicked_right_button = right_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, command=remove_word)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
