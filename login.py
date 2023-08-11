from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import subprocess
import re

root = Tk()
root.title("Login and Register Page")
root.resizable(False, False)
root.geometry("400x500")
connection = mysql.connector.connect(host='localhost', user='root', password='', database='py_1')
c = connection.cursor()

# Custom encryption method
def enc(password):
    encrypted_password = ""
    for char in password:
        encrypted_char = chr(ord(char) + 3)  # Shift each character by 3 positions
        encrypted_password += encrypted_char
    return encrypted_password

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Encrypt the entered password
    encrypted_password = enc(password)

    # Execute an SQL query to retrieve the stored encrypted password for the entered username
    c.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = c.fetchone()

    if result:
        stored_password = result[0]  # Extract the stored encrypted password
        if encrypted_password == stored_password:
            messagebox.showinfo("Login", "Login successful")
            # Open another Python file after successful login
            
            root.destroy()  # Close the login window
            import maain
        else:
            messagebox.showerror("Login Error", "Invalid password")
    else:
        messagebox.showerror("Login Error", "Invalid username")

def register():
    fullname = fullname_entry.get().strip()
    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()
    phone = phone_entry_rg.get().strip()
    gender = gender_var.get()  # Get the selected gender value

    if not fullname:
        messagebox.showerror("Error", "Please enter your full name")
    elif not username:
        messagebox.showerror("Error", "Please enter a username")
    elif not password:
        messagebox.showerror("Error", "Please enter a password")
    elif not confirm_password:
        messagebox.showerror("Error", "Please confirm the password")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
    elif not phone:
        messagebox.showerror("Error", "Please enter your phone number")
    elif len(phone) != 10 or not phone.isdigit():
        messagebox.showerror("Error", "Please enter a valid 10-digit phone number")
    elif not gender:
        messagebox.showerror("Error", "Please select a gender")
    elif len(password) < 8 or not re.search("[!@#]", password):
        messagebox.showerror("Error", "Password must be at least 8 characters long and contain a special character (!@#)")
    else:
        # Encrypt the password before storing it in the database
        encrypted_password = enc(password)

        # Check if the username already exists in the database
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = c.fetchone()
        if result:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            # Execute an SQL query to insert the user's information into the database
            c.execute("INSERT INTO users (fullname, username, password, phone, gender) VALUES (%s, %s, %s, %s, %s)",
                      (fullname, username, encrypted_password, phone, gender))
            connection.commit()
            messagebox.showinfo("Register", "Registration successful")

# Create gradient background
background_frame = Frame(root, bg="#183E63", bd=0)  # Change background color to a darker blue
background_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create Login Frame
login_frame = Frame(root, bg="#1E88E5", bd=0)  # Change background color to a slightly darker blue
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

login_label = Label(login_frame, text="Login", font=("Arial", 18), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
login_label.grid(row=0, column=0, pady=10, columnspan=2)

username_label = Label(login_frame, text="Username:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
username_label.grid(row=1, column=0, pady=5)

password_label = Label(login_frame, text="Password:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
password_label.grid(row=2, column=0, pady=5)

style = ttk.Style()
style.configure("RoundedEntry.TEntry", borderwidth=0, fieldbackground="#AFEEEE", relief="flat", foreground="black", font=("Arial", 12))  # Change field background color to turquoise

username_entry = ttk.Entry(login_frame, font=("Arial", 12), style="RoundedEntry.TEntry")
username_entry.grid(row=1, column=1, pady=5)

password_entry = ttk.Entry(login_frame, show="*", font=("Arial", 12), style="RoundedEntry.TEntry")
password_entry.grid(row=2, column=1, pady=5)

login_button = Button(login_frame, text="Login", command=login, font=("Arial", 12, "bold"), fg="white", bg="#4CAF50", activebackground="#45a049")  # Change button color to green and active background color to a darker shade of green
login_button.grid(row=3, column=0, columnspan=2, pady=10)

register_link = Label(login_frame, text="Don't have an account yet? Click here", fg="red", cursor="hand2", font=("Arial", 10, "underline"), bg="#1E88E5")  # Change text color to red and background color to a slightly darker blue
register_link.grid(row=4, column=0, columnspan=2, pady=5)

# Create Register Frame
register_frame = Frame(root, bg="#1E88E5", bd=0)  # Change background color to a slightly darker blue
register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

register_label = Label(register_frame, text="Register", font=("Arial", 18), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
register_label.grid(row=0, column=0, pady=10, columnspan=2)

fullname_label = Label(register_frame, text="Full Name:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
fullname_label.grid(row=1, column=0, pady=5)

username_label_rg = Label(register_frame, text="Username:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
username_label_rg.grid(row=2, column=0, pady=5)

password_label_rg = Label(register_frame, text="Password:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
password_label_rg.grid(row=3, column=0, pady=5)

confirmpass_label_rg = Label(register_frame, text="Confirm Password:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
confirmpass_label_rg.grid(row=4, column=0, pady=5)

phone_label_rg = Label(register_frame, text="Phone:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
phone_label_rg.grid(row=5, column=0, pady=5)

gender_label_rg = Label(register_frame, text="Gender:", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
gender_label_rg.grid(row=6, column=0, pady=5)

style.configure("RoundedEntry.TEntry", borderwidth=0, fieldbackground="#AFEEEE", relief="flat", foreground="black", font=("Arial", 12))  # Change field background color to turquoise

fullname_entry = ttk.Entry(register_frame, font=("Arial", 12), style="RoundedEntry.TEntry")
fullname_entry.grid(row=1, column=1, pady=5)

username_entry_rg = ttk.Entry(register_frame, font=("Arial", 12), style="RoundedEntry.TEntry")
username_entry_rg.grid(row=2, column=1, pady=5)

password_entry_rg = ttk.Entry(register_frame, show="*", font=("Arial", 12), style="RoundedEntry.TEntry")
password_entry_rg.grid(row=3, column=1, pady=5)

confirmpass_entry_rg = ttk.Entry(register_frame, show="*", font=("Arial", 12), style="RoundedEntry.TEntry")
confirmpass_entry_rg.grid(row=4, column=1, pady=5)

phone_entry_rg = ttk.Entry(register_frame, font=("Arial", 12), style="RoundedEntry.TEntry")
phone_entry_rg.grid(row=5, column=1, pady=5)

gender_var = StringVar()  # Variable to store the selected gender
gender_radiobutton1 = Radiobutton(register_frame, text="Male", variable=gender_var, value="Male", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
gender_radiobutton1.grid(row=6, column=1, pady=5, sticky="W")
gender_radiobutton2 = Radiobutton(register_frame, text="Female", variable=gender_var, value="Female", font=("Arial", 12), fg="black", bg="#1E88E5")  # Change background color to a slightly darker blue
gender_radiobutton2.grid(row=6, column=1, pady=5, sticky="E")

register_button = Button(register_frame, text="Register", command=register, font=("Arial", 12, "bold"), fg="white", bg="#4CAF50", activebackground="#45a049")  # Change button color to green and active background color to a darker shade of green
register_button.grid(row=7, column=0, columnspan=2, pady=10)

login_link = Label(register_frame, text="Already have an account? Click here", fg="red", cursor="hand2", font=("Arial", 10, "underline"), bg="#1E88E5")  # Change text color to red and background color to a slightly darker blue
login_link.grid(row=8, column=0, columnspan=2, pady=5)

# Switch to the login frame initially
register_frame.place_forget()

# Create the "users" table if it doesn't exist
c.execute("""
     CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(255),
        username VARCHAR(255),
        password VARCHAR(255),
        phone VARCHAR(10),
        gender VARCHAR(10)
    )
""")

def show_register_frame(event):
    login_frame.place_forget()
    register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

def show_login_frame(event):
    register_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Bind the click events to the link labels
register_link.bind("<Button-1>", show_register_frame)
login_link.bind("<Button-1>", show_login_frame)

root.mainloop()
