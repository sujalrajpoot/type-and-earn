import os
import time
import random
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox

# Database setup
def init_db():
    """Initialize the database. Creates a new database if it doesn't exist
    and sets up a default user with a given name and initial balance and level."""
    if not os.path.exists('./game_data.db'):
        name = simpledialog.askstring("Enter Name", "Please enter your name:")
        if not name:
            name = "Guest Player"  # Default name if the user cancels
        conn = sqlite3.connect('./game_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE user_data (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        balance INTEGER,
                        level INTEGER)''')
        c.execute('INSERT INTO user_data (id, name, balance, level) VALUES (1, ?, 0, 1)', (name,))
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect('./game_data.db')
        conn.close()

def load_user_data():
    """Load user data from the database. If no data is found, return default values."""
    conn = sqlite3.connect('./game_data.db')
    c = conn.cursor()
    c.execute('SELECT name, balance, level FROM user_data WHERE id = 1')
    data = c.fetchone()
    conn.close()
    
    if data is None:
        return ("Guest Player", 0, 1)  # Default values if no data is found
    return data  # This will return (name, balance, level)

def save_user_data(name, balance, level):
    """Save user data to the database."""
    conn = sqlite3.connect('./game_data.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO user_data (id, name, balance, level) VALUES (1, ?, ?, ?)', (name, balance, level))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Load user data
user_name, user_balance, game_level = load_user_data()

# Game logic variables
game_started = False
current_word = ""
start_time = 0
countdown_interval = 1000

def update_game_level_label():
    """Update the displayed game level label."""
    level_label.config(text='Level: ' + str(game_level))

def update_balance_label():
    """Update the displayed user balance label."""
    balance_label.config(text='Balance: ₹' + str(user_balance))

def update_name_label():
    """Update the displayed user name label."""
    name_label.config(text='Welcome, ' + user_name)

def generate_random_word():
    """Generate a random word based on the current game level."""
    if game_level == 1 or game_level == 2:
        Words = ['Unque', 'Dispr', 'Accom', 'Incom', 'Unbel', 'Extra', 'Incon', 'Incom', 'Indis', 'Respo']
    elif game_level == 3 or game_level == 4:
        Words = ['Unques', 'Dispro', 'Accomp', 'Incomp', 'Unbeli', 'Extrao', 'Incons', 'Incomp', 'Indist', 'Respon']
    elif game_level == 5 or game_level == 6:
        Words = ['Unquest', 'Disprop', 'Accompl', 'Incompr', 'Unbelie', 'Extraor', 'Inconsp', 'Incompr', 'Indisti', 'Respons']
    elif game_level == 7 or game_level == 8:
        Words = ['Unquesti', 'Dispropo', 'Accompli', 'Incompre', 'Unbeliev', 'Extraord', 'Inconspi', 'Incompre', 'Indistin', 'Responsi']
    elif game_level == 9 or game_level == 10:
        Words = ['Unquestio', 'Dispropor', 'Accomplis', 'Incompreh', 'Unbelieva', 'Extraordi', 'Inconspic', 'Incompreh', 'Indisting', 'Responsib']
    else:
        Words = ['Unquestionably', 'Disproportionate', 'Accomplishment', 'Incomprehensible', 'Unbelievability', 'Extraordinarily', 'Inconspicuousness', 'Incomprehensibility', 'Indistinguishable', 'Responsibility']
    
    random_word = random.choice(Words)
    return random_word

def timer_limit():
    """Return the time limit for the current game level."""
    if game_level == 1: return 5
    elif game_level == 2: return 6
    elif game_level == 3: return 7
    elif game_level == 4: return 8
    elif game_level == 5: return 9
    elif game_level == 6: return 10
    elif game_level == 7: return 11
    elif game_level == 8: return 12
    elif game_level == 9: return 13
    elif game_level == 10: return 14
    else: return 15

def update_countdown_timer():
    """Update the countdown timer label and check if time is up."""
    global start_time
    input_timer_limit = timer_limit()
    remaining_time = input_timer_limit - int(time.time() - start_time)
    countdown_label.config(text=f"Time Left: {remaining_time} Seconds")

    if remaining_time <= 0:
        check_word()
        start_new_game()
    else:
        app.after(countdown_interval, update_countdown_timer)

win_count = 0

def check_word():
    """Check if the user's input matches the current word within the time limit."""
    global game_started, current_word, start_time, user_balance, win_count, game_level
    input_timer_limit = timer_limit()

    if not game_started:
        message_label.config(text='Please start the game', fg='red', font=('Arial', 12))
        return

    user_word = user_entry.get()

    if not user_word:
        result_label.config(text='Please Enter Something', fg='red')
        return

    if user_word.lower() == current_word.lower() and (time.time() - start_time) <= input_timer_limit:
        user_balance += 5
        save_user_data(user_name, user_balance, game_level)
        update_balance_label()
        win_count += 1

        if win_count >= 10:
            win_count = 0
            game_level += 1
            save_user_data(user_name, user_balance, game_level)
            update_game_level_label()

        start_new_game()
    else:
        user_balance = max(0, user_balance - 5)
        save_user_data(user_name, user_balance, game_level)
        update_balance_label()
        start_new_game()

def start_new_game():
    """Start a new game by generating a new word and resetting the timer."""
    global current_word, start_time, game_started
    game_started = True
    current_word = generate_random_word()
    current_word = ''.join(random.choice((str.upper, str.lower))(c) for c in current_word)
    word_label.config(text='Word: ' + current_word)
    start_time = time.time()
    result_label.config(text='')
    user_entry.delete(0, tk.END)
    message_label.config(text='', font=('Arial', 12))
    update_countdown_timer()

def start_game():
    """Start the game if the user has sufficient balance."""
    if user_balance >= 30:
        start_new_game()
    else:
        messagebox.showerror("Warning", "Your balance must be at least ₹30.")

def withdraw_balance():
    """Allow the user to withdraw a specified amount from their balance."""
    global user_balance
    if user_name == "Guest Player":
        messagebox.showerror("Warning", "Being a Guest Player You Cannot Withdraw Money.")
        return
    elif game_level == 1 and user_balance > 30:
        messagebox.showerror("Warning", "Your Level Must be greater than 1. So You Cannot Withdraw Money.")
        return
    elif user_balance > 30:
        withdraw_amount = simpledialog.askinteger("Withdraw Balance", "Enter the amount to withdraw:")
        if withdraw_amount is None: return
        elif user_balance < withdraw_amount:
            messagebox.showerror("Warning", "Insufficient Balance")
        else:
            user_balance -= withdraw_amount
            save_user_data(user_name, user_balance, game_level)
            update_balance_label()
            messagebox.showinfo("Withdraw Successful", f"₹{withdraw_amount} Withdraw Successfully.")
    else:
        messagebox.showerror("Warning", "Your balance must be more than ₹30")

def add_money():
    """Allow the user to add a specified amount to their balance."""
    global user_balance
    add_amount = simpledialog.askinteger("Add Money", "Enter the amount to add:")
    if add_amount is not None:
        user_balance += add_amount
        save_user_data(user_name, user_balance, game_level)
        update_balance_label()
        messagebox.showinfo("Money Added Successful", f"₹{add_amount} Added Successfully.")

def quit_game():
    """Save user data and exit the game."""
    save_user_data(user_name, user_balance, game_level)
    app.quit()

# Set up the GUI
app = tk.Tk()
app.title('Type and Earn')

app.iconbitmap('./icon.ico')

name_label = tk.Label(app, text='', font=('Arial', 14))
name_label.pack()

word_label = tk.Label(app, text='', font=('Arial', 11))
word_label.pack(pady=10)

user_entry = tk.Entry(app, font=('Arial', 14))
user_entry.pack()

check_button = tk.Button(app, text='Check', command=check_word, font=('Arial', 14))
check_button.pack(pady=10)

result_label = tk.Label(app, text='', font=('Arial', 16))
result_label.pack(pady=10)

balance_label = tk.Label(app, text='Balance: ₹0', font=('Arial', 14))
balance_label.pack()

message_label = tk.Label(app, text='', font=('Arial', 12))
message_label.pack(pady=10)

start_game_button = tk.Button(app, text='Start New Game', command=start_game, font=('Arial', 14))
start_game_button.pack()

quit_button = tk.Button(app, text='Quit Game', command=quit_game, font=('Arial', 14))
quit_button.pack()

withdraw_button = tk.Button(app, text='Withdraw', command=withdraw_balance, font=('Arial', 14))
withdraw_button.pack()

add_money_button = tk.Button(app, text='Add Money', command=add_money, font=('Arial', 14))
add_money_button.pack()

countdown_label = tk.Label(app, text='', font=('Arial', 12))
countdown_label.pack()

level_label = tk.Label(app, text='', font=('Arial', 14))
level_label.pack()

# Update labels for user name, balance, and level
update_name_label()
update_game_level_label()
update_balance_label()

app.mainloop()