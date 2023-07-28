from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

COLOR_ONE = "#78C1F3"


def find_password():
    """
    This function gets executed when 'Search' button is pressed. It will search the keys inside the .json
    file and return the data as a pop-up when the key is found otherwise 'not found' pop-up.
    :return: None
    """

    search_entry_text = website_entry.get()
    if search_entry_text == "":
        messagebox.showerror(title="Error", message="Please enter a valid search.")
        return

    try:
        with open("data.json", "r") as file_pointer:
            file_data = json.load(file_pointer)

            try:
                messagebox.askokcancel(title="Result", message=f"Email: {file_data[search_entry_text]['email']}\n"
                                                                   f"Password: {file_data[search_entry_text]['password']}")

            except KeyError:
                messagebox.showinfo(title="Error", message=f"Data associated with '{search_entry_text}' doesn't exist.")

    except FileNotFoundError as error_message:
        messagebox.showerror(title="File not Found", message=str(error_message))


def generate_password():
    """
    Generates a password using an algorithm when "Generate Password" button is pressed displaying it
    in the password entry field on GUI.
    :return: None
    """

    # Incase user clicks on button multiple times, this will clear the previously generated password.
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    final_password = password_letters + password_symbols + password_numbers

    # Shuffling the password.
    random.shuffle(final_password)

    password = ''.join(final_password)
    password_entry.insert(0, string=password)

    # Copies the password in the clip board.
    pyperclip.copy(password)


def clear_entries():
    """
    This function will clear all the entries from the text fields once the data has successfully been
    added inside the .txt file after the "Add" button is pressed.
    :return: None
    """

    website_entry.delete(0, "end")
    email_entry.delete(0, "end")
    password_entry.delete(0, "end")


def save_data(website, unique_iden, passw):
    """
    This function saves the data in a .txt file once the 'Add' button is pressed and handles
    exceptional cases.
    :return: None
    """

    new_data = {
        website: {
            "email": unique_iden,
            "password": passw
        }
    }
    
    try:
        with open("data.json", "r") as file_pointer:

            # Reading the old data from the .json file.
            data = json.load(file_pointer)

    except FileNotFoundError:

        # If file is not found, we simply create a new one and add the data in it.
        with open("data.json", "w") as file_pointer:

            # Adding the updated data back in the .json file.
            json.dump(new_data, file_pointer, indent=4)

    except json.decoder.JSONDecodeError:

        """Incase the file exists and is entirely empty, it won't be able to create a dictionary in python, so we 
        catch this exception, open the file in write mode and add the data directly which the user entered."""
        with open("data.json", "w") as file_pointer:
            json.dump(new_data, file_pointer, indent=4)

    else:
        # Updating the old data with the new data.
        try:
            data.update(new_data)

        except AttributeError:

            # If there are any other existing characters in .json file, this will deal with them.
            with open("data.json", "w") as file_pointer:
                json.dump(new_data, file_pointer, indent=4)

        else:
            with open("data.json", "w") as file_pointer:

                # Saving updated data.
                json.dump(data, file_pointer, indent=4)


def add_button_pressed():
    """
    This function is triggered when the 'Add' button is pressed. It will clear all the data inside
    the fields and store the data inside the text file.
    :return: None
    """

    website_name = website_entry.get()
    unique_user_identifier = email_entry.get()
    password = password_entry.get()

    if len(password) == 0 or len(website_name) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty.")

    else:
        is_all_good = messagebox.askokcancel(title=website_name, message=f"These are the details entered.\n"
                           f"Email: {unique_user_identifier}\nPassword: {password} \n"
                            "Is it okay to save?")

        if is_all_good:
            save_data(website=website_name, unique_iden=unique_user_identifier, passw=password)
            clear_entries()


# Setting up the entire User Interface

main_window = Tk()
main_window.title("Password Generator")
main_window.config(padx=50, pady=50, bg=COLOR_ONE)

canvas = Canvas(height=200, width=200, bg=COLOR_ONE, highlightthickness=0)
password_logo = PhotoImage(file="logo.png")

# The tuple is the (x, y) coordinate of the position where the image will be placed on screen.
canvas.create_image((100, 100), image=password_logo)
canvas.grid(column=1, row=0)

# Creating labels for text and positioning them appropriately.
website_label = Label(text="Website:", pady=2, padx=2, bg=COLOR_ONE)
website_label.grid(row=1, column=0)

unique_ID_label = Label(text="Email / Username:", pady=2, padx=2, bg=COLOR_ONE)
unique_ID_label.grid(row=2, column=0)

password_label = Label(text="Password:", pady=2, padx=2, bg=COLOR_ONE)
password_label.grid(row=3, column=0)

# Creating text input fields and positioning them appropriately.
website_entry = Entry(width=35, highlightthickness=1 , highlightbackground="black")
website_entry.grid(column=1, row=1, columnspan=1)

# Puts the cursor in this specific text field.
website_entry.focus()

email_entry = Entry(width=55, highlightthickness=1, highlightbackground="black")
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, string="test@gmail.com")

password_entry = Entry(width=35, highlightthickness=1, highlightbackground="black")
password_entry.grid(column=1, row=3)

# Creating buttons and positioning them appropriately.
generate_button = Button(text="Generate Password", width=15, pady=2, padx=2, command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=46, pady=2, padx=2, command=add_button_pressed)
add_button.grid(row=4, column=1, columnspan=3)

search_button = Button(text="Search", width=15, pady=2, padx=2, command=find_password)
search_button.grid(row=1, column=2)

main_window.mainloop()
