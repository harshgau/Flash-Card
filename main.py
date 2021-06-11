from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("./data/words_to_learn.csv.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_words = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_words, fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")
    canvas.config(bg="white", highlightthickness=0)
    canvas.itemconfig(card_background, image=card_back_image)
    window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 268, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 24, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 54, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
my_image_right = PhotoImage(file="images/right.png")
my_image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=my_image_wrong, highlightthickness=0, command=next_card)
button_wrong.grid(row=1, column=0)
button_right = Button(image=my_image_right, highlightthickness=0, command=is_known)
button_right.grid(row=1, column=1)
next_card()
window.mainloop()
