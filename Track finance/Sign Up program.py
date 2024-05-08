from tkinter import *
from tkinter import messagebox
import ast
import subprocess
import sqlite3


window = Tk()
window.title("SignUp")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False, False)


'''
def signup():
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    if password == confirm_password:
        try:
            file = open('datasheet.txt', 'r+')
            d = file.read()
            r = ast.literal_eval(d)

            dict2 = {username: password}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file = open('datasheet.txt', 'w')
            w = file.write(str(r))

            messagebox.showinfo('Sign Up', 'Successfully Signed Up')

        except:
            file = open('datasheet.txt', 'w')
            pp = str({'Username': 'password'})
            file.write(pp)
            file.close()

    else:
        messagebox.showerror('Invalid', 'Both passwords should match')
'''

def signup():
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    if password == confirm_password:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Create users table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        """)

        # Check if username already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            messagebox.showinfo('Sign Up', 'Username already exists')
            return False

        # Insert new user
        c.execute("INSERT INTO users VALUES (?,?)", (username, password))

        # Save (commit) the changes
        conn.commit()

        # Close the connection
        conn.close()

        messagebox.showinfo('Sign Up', 'Successfully Signed Up')
    else:
        messagebox.showerror('Invalid', 'Both passwords should match')

def sign():
    window.destroy()
    subprocess.Popen(["python", "Sign In program.py"])

img = PhotoImage(file='Track Finance Sign Up Logo.png')
Label(window, image=img, border=0, bg='white').place(x=50, y=90)

frame = Frame(window, width=350, height=390, bg='#fff')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign up', fg="#57a1f8", bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    if user.get() == 'Username':
        user.delete(0, 'end')
        user.config(fg='black')

def on_leave(e):
    if user.get() == '':
        user.insert(0, 'Username')
        user.config(fg='black')

user = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Helvetica', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show='*')
        code.config(fg='black')

def on_leave(e):
    if code.get() == '':
        code.insert(0, 'Password')
        code.config(show='')
        code.config(fg='black')

code = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

def on_enter(e):
    if confirm_code.get() == 'Confirm Password':
        confirm_code.delete(0, 'end')
        confirm_code.config(show='*')
        confirm_code.config(fg='black')

def on_leave(e):
    if confirm_code.get() == '':
        confirm_code.insert(0, 'Confirm Password')
        confirm_code.config(show='')
        confirm_code.config(fg='gray')

confirm_code = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='')
confirm_code.place(x=30, y=220)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind("<FocusIn>", on_enter)
confirm_code.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

Button(frame, width=39, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280)
label = Label(frame, text='Already Signed Up?', fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=90, y=340)

signin = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=sign)
signin.place(x=200, y=340)

window.mainloop()
