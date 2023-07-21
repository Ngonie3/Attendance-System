from tkinter import *
from PIL import ImageTk
import pymysql
from tkinter import messagebox
from email.message import EmailMessage
import ssl
import smtplib


def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmPasswordEntry.delete(0, END)
    checkBtn.set(0)


def send_email():
    email_sender = 'ngonie3mav@gmail.com'
    email_password = 'enter_your_password'
    email_receiver = 'mafara.ngonidzashe@gmail.com'

    subject = 'Successful Registration'
    body = """
    You have created your account successfully. Enjoy our services!
    
    Best Regards
    
    Ngonidzashe Mafara
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def connect_database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' \
            or confirmPasswordEntry.get() == '':
        messagebox.showerror('Error!', 'Please fill in all fields')
    elif passwordEntry.get() != confirmPasswordEntry.get():
        messagebox.showerror('Error!', 'Your passwords do not match, please try again')
    elif checkBtn.get() == 0:
        messagebox.showerror('Error!', 'Please accept Terms & Conditions')
    else:
        try:
            connection = pymysql.connect(host='localhost', user='root', password='enter_your_password',
                                         database='register_user')
            myCursor = connection.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity issue, Please try again')
            return
        selectQuery = 'SELECT * FROM user_data WHERE username = %s'
        myCursor.execute(selectQuery, (usernameEntry.get()))
        row = myCursor.fetchone()
        if row is not None:
            messagebox.showerror('Error', 'Username already exists!')
        else:
            query = 'INSERT INTO user_data(email_address, username, password) VALUES(%s, %s, %s)'
            myCursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo('Success', 'Sign up successful. Please check your email')
            send_email()
            clear()


def login_page():
    signUpWindow.destroy()
    import Login


def on_passwordEnter(event):
    passwordEntry.config(show='*')


def on_confirmPasswordEnter(event):
    confirmPasswordEntry.config(show='*')


def revealPassword():
    closeEye.config(file='Images/openeye.png')
    passwordEntry.config(show='')
    confirmPasswordEntry.config(show='')
    eyeButton.config(command=hidePassword)


def hidePassword():
    closeEye.config(file='Images/closeye.png')
    passwordEntry.config(show='*')
    confirmPasswordEntry.config(show='*')
    eyeButton.config(command=revealPassword)


signUpWindow = Tk()
signUpWindow.title('Sign Up')
signUpWindow.resizable(0, 0)
backgroundImage = ImageTk.PhotoImage(file='Images/bg.jpg')
backgroundLabel = Label(signUpWindow, image=backgroundImage)
backgroundLabel.grid()

frame = Frame(signUpWindow, bg='white')
frame.place(x=554, y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 18, 'bold'),
                bg='white', fg='black')
heading.grid(row=0, column=0, padx=10, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                   fg='black')
emailLabel.grid(row=1, column=0, sticky='w', padx=25)
emailEntry = Entry(frame, width=26, font=('Open Sans', 12))
emailEntry.grid(row=2, column=0, sticky='w', padx=25)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                      fg='black')
usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))
usernameEntry = Entry(frame, width=25, font=('Open Sans', 12))
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                      fg='black')
passwordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(12, 0))
passwordEntry = Entry(frame, width=25, font=('Open Sans', 12))
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)
passwordEntry.bind('<FocusIn>', on_passwordEnter)

closeEye = PhotoImage(file="Images/closeye.png")
openEye = PhotoImage(file='Images/openeye.png')
confirmPasswordLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 12, 'bold'),
                             bg='white', fg='black')
confirmPasswordLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(12, 0))
confirmPasswordEntry = Entry(frame, width=25, font=('Open Sans', 12))
confirmPasswordEntry.grid(row=8, column=0, sticky='w', padx=25)
confirmPasswordEntry.bind('<FocusIn>', on_confirmPasswordEnter)
eyeButton = Button(frame, image=closeEye, bd=0, bg='White', activebackground='White',
                   cursor='hand2', command=revealPassword)
eyeButton.grid(row=8, column=0, sticky='e')

checkBtn = IntVar()
termsAndConditions = Checkbutton(frame, text="I agree to the Terms & Conditions", font=("Open Sans", 11),
                                 bg="white", activebackground="white", cursor='hand2', variable=checkBtn)
termsAndConditions.grid(row=9, column=0, pady=(10, 0))

signUpButton = Button(frame, text='Sign Up', font=('Microsoft Yahei UI Light', 16, 'bold'), bd=0,
                      bg='black', width=19, activebackground='black', fg='white', command=connect_database,
                      cursor='hand2')
signUpButton.grid(row=10, column=0, pady=(10, 0))

loginLabel = Label(frame, text='Already have an account?', font=('Open Sans', 10, 'bold'),
                   fg='firebrick1', bg='white')
loginLabel.grid(row=11, column=0, sticky='w', padx=25, pady=(20, 0))
loginButton = Button(frame, text='Login', font=('Open Sans', 12,
                                                'bold underline'), fg='blue', bg='white', activeforeground='blue',
                     activebackground='white', cursor='hand2', bd=0, command=login_page)
loginButton.grid(row=11, column=0, pady=(20, 0), sticky='e', padx=35)
signUpWindow.mainloop()
