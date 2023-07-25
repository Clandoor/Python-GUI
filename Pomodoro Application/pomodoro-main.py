import math
from tkinter import *

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = ""


def reset_timer():
    """
    Resets the check marks, stops the timer and resets everything when 'Reset' button is pressed.
    :return: None
    """
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


def start_timer():
    """
    Calls the count_down function when the button 'Start' is pressed.
    :return: None
    """

    global reps
    reps += 1

    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_seconds)
        title_label.config(text="Break", fg=RED)

    elif reps % 2 == 0:
        count_down(short_break_seconds)
        title_label.config(text="Break", fg=PINK)

    else:
        count_down(work_seconds)
        title_label.config(text="Work", fg=GREEN)


def count_down(count):
    """
    This function is responsible for counting down from a specific value. It utilizes itemconfig()
    method passing the canvas text and count variable which will be decremented.
    :param count: The value from which countdown will start.
    :return: None
    """

    count_minutes = math.floor(count / 60)
    count_seconds = count % 60
    display_text = f"{count_minutes}:{count_seconds}"

    if count_seconds < 10:
        display_text = f"{count_minutes}:0{count_seconds}"

    canvas.itemconfig(timer_text, text=display_text)

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        check_mark = ""

        # math.floor(reps / 2) is number of work session/s.
        for _ in range(math.floor(reps / 2)):
            check_mark += "✔"

        check_marks.config(text=check_mark)


"""
Setting up the User Interface of the Program.
"""
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=YELLOW)
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

tomato_photo = PhotoImage(file="tomato.png")

# To make it align on center.
canvas.create_image(100, 112, image=tomato_photo)

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(row=3, column=1)

window.mainloop()
