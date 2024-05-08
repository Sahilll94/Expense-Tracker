from tkinter import *
from tkinter import messagebox
import ast
import os
import subprocess
import sqlite3


root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

'''
def signin():
    username=user.get()
    password=code.get()

    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()

##    print(r.keys())
##    print(r.values())

    if username in r.keys() and password==r[username]:
          # Close the current login window
        root.destroy()

        # Open main.py using subprocess
        subprocess.Popen(['python', 'main.py'])
        
    else:
        messagebox.showerror('Invalid','Invalid Username or Password')
'''

def signin():
    username = user.get()
    password = code.get()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if username exists and password matches
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    if result:
        root.destroy()

        # Open main.py using subprocess and pass username as command-line argument
        subprocess.Popen(['python', 'main.py', username])

    else:
        messagebox.showerror('Invalid', 'Invalid username or password')

    conn.close()
        

def signup_command():
    completed_process = subprocess.run(['python', "Sign Up program.py"], capture_output=True, text=True)
    if completed_process.returncode == 0:
        print(completed_process.stdout)

img = PhotoImage(file='Track Finance Logo.png')

label = Label(root, image=img, bg='white')
label.place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

        
user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


def on_enter(e):
    code.delete(0, 'end')
    code.config(show='*') #astrik

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')
        code.config(show='')#show blank while password only

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show='')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign In', bg='#57a1f8', fg='white', border=0,command=signin).place(x=35, y=204)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)

root.mainloop()
