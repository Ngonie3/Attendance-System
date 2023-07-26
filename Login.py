from tkinter import *
from PIL import ImageTk
import pymysql
from tkinter import messagebox


def goToMain():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='enter_your_password',
                                     database='register_user')
        myCursor = connection.cursor()
    except:
        messagebox.showerror('Error!', ' Data connectivity issue, please try again')
        return
    selectQuery = 'SELECT username  FROM user_data WHERE username = %s'
    myCursor.execute(selectQuery, (usernameEntry.get()))
    row = myCursor.fetchone()
    myQuery = 'SELECT password FROM user_data WHERE password = %s'
    myCursor.execute(myQuery, (passwordEntry.get()))
    myRow = myCursor.fetchone()

    if row is None and myRow is None or usernameEntry.get() == '' and passwordEntry.get() == '':
        Frame(loginWindow, width=250, height=2, bg='firebrick1').place(x=580, y=222)
        Frame(loginWindow, width=250, height=2, bg='firebrick1').place(x=580, y=322)
        usernameEntry.config(fg='firebrick1')
        passwordEntry.config(fg='firebrick1')
        messagebox.showerror('Error!', 'Username and password fields cannot be empty!')

    elif row is None or usernameEntry.get() == '':
        Frame(loginWindow, width=250, height=2, bg='firebrick1').place(x=580, y=222)
        usernameEntry.config(fg='firebrick1')
        messagebox.showerror('Error!', 'Wrong username. Please try again')

    elif myRow is None or passwordEntry.get() == '':
        Frame(loginWindow, width=250, height=2, bg='firebrick1').place(x=580, y=322)
        passwordEntry.config(fg='firebrick1')
        messagebox.showerror('Error!', 'Wrong password. Please try again')
    else:
        loginWindow.destroy()
        import main


def signup_page():
    loginWindow.destroy()
    import SignUp


def on_usernameEnter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)
        usernameEntry.config(fg='black')


def on_passwordEnter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)
        passwordEntry.config(show='*', fg='black')


def reveal():
    closeEye.config(file='Images/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def hide():
    closeEye.config(file='Images/closeye.png')
    if passwordEntry.get() == 'Password':
        pass
    else:
        passwordEntry.config(show='*')
        eyeButton.config(command=reveal)


def changeOnHover(button, colorOnHover, colorOnLeave, textColorOnHover, textColorOnLeavingHover):
    loginButton.bind("<Enter>", func=lambda e: loginButton.config(background=colorOnHover, fg=textColorOnHover))
    loginButton.bind("<Leave>", func=lambda e: loginButton.config(background=colorOnLeave, fg=textColorOnLeavingHover))


loginWindow = Tk()
loginWindow.resizable(0, 0)
loginWindow.title('Login Page')

bgImage = ImageTk.PhotoImage(file='Images/bg.jpg')
bgLabel = Label(loginWindow, image=bgImage)
bgLabel.grid(row=0, column=0)
heading = Label(loginWindow, text="ADMIN LOGIN", font=('Microsoft Yahei UI Light', 23, 'bold'),
                bg='white', fg='black')
heading.place(x=605, y=120)

usernameEntry = Entry(loginWindow, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'),
                      bd=0, fg='black')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', on_usernameEnter)
Frame(loginWindow, width=250, height=2, bg='black').place(x=580, y=222)

passwordEntry = Entry(loginWindow, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'),
                      bd=0, fg='black')
passwordEntry.place(x=580, y=290)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', on_passwordEnter)
Frame(loginWindow, width=250, height=2, bg='black').place(x=580, y=322)

closeEye = PhotoImage(file="Images/closeye.png")
openEye = PhotoImage(file='Images/openeye.png')
eyeButton = Button(loginWindow, image=closeEye, bd=0, bg='White', activebackground='White',
                   cursor='hand2', command=reveal)
eyeButton.place(x=810, y=295)

loginButton = Button(loginWindow, text='Login', font=('Open Sans', 16, 'bold'),
                     fg='white', bg='black', activeforeground='white',
                     activebackground='black', cursor='hand2', bd=0, width=19, command=goToMain)
loginButton.place(x=578, y=400)
changeOnHover(loginButton, "white", "black", "black", "white")

signupLabel = Label(loginWindow, text="Don't have an account?", font=('Open Sans', 9, 'bold'),
                    fg='firebrick1', bg='white')
signupLabel.place(x=590, y=500)

newAccountButton = Button(loginWindow, text='Create a new one', font=('Open Sans', 9,
                        'bold underline'), fg='blue', bg='white', activeforeground='blue',
                          activebackground='white', cursor='hand2', bd=0, command=signup_page)
newAccountButton.place(x=727, y=500)

loginWindow.mainloop()
