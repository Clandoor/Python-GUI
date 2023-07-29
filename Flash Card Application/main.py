from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_TOP = ("Arial", 40, "italic")
FONT_BOTTOM = ("Ariel", 60, "bold")
current_card = {}
dictionary = {}


def switch_to_next_card():
    """
    This function changes the characteristics of the canvas image by changing the background image and
    texts.
    :return: None
    """

    # Selecting a random entry from the dictionary.
    global current_card, flip_timer
    main_window.after_cancel(flip_timer)
    current_card = random.choice(dictionary)

    # Getting a hold of specific canvas item and modifying it.
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = main_window.after(3000, func=flip_card)


def known_word():
    """
    This function removes the current word from the dictionary since the user already knows that word.
    It is called when the user clicks on the check mark button.
    :return: None
    """

    dictionary.remove(current_card)
    print(len(dictionary))

    words_learnt = pandas.DataFrame(dictionary)

    # Doesn't add the index numbers if 'index' parameter is set to 'False'.
    words_learnt.to_csv("data/words_to_learn.csv", index=False)
    switch_to_next_card()


def flip_card():
    """
    This function changes the background and the texts written on the canvas.
    :return: None
    """

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


# Importing the data from .csv files.
try:
    data_frame = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dictionary = original_data.to_dict(orient="records")

else:
    # Orient parameter - How do we want to orient this table.
    dictionary = data_frame.to_dict(orient='records')


# Setting up the User Interface.
main_window = Tk()
main_window.title("Flashy")
main_window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = main_window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
canvas.grid(row=0, column=0)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)

# Setting up the images to use.
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
check_mark_image = PhotoImage(file="images/right.png")
cross_image = PhotoImage(file="images/wrong.png")

# Assigning images to their respective elements.
check_mark_button = Button(image=check_mark_image, relief="flat", borderwidth=0, command=known_word)
cross_mark_button = Button(image=cross_image, relief="flat", borderwidth=0, command=switch_to_next_card)
back = canvas.create_image((400, 263), image=card_back_image)
card_background = canvas.create_image((400, 263), image=card_front_image)


# Positioning the elements on the canvas.
canvas.grid(row=0, column=0, columnspan=2)
check_mark_button.grid(row=1, column=0)
cross_mark_button.grid(row=1, column=1)

# Generating texts inside the canvas.
card_title = canvas.create_text(400, 150, text="", font=FONT_TOP)
card_word = canvas.create_text(400, 263, text="", font=FONT_BOTTOM)

switch_to_next_card()

main_window.mainloop()
