#Project imports
from tkinter import *
import random
from webbrowser import open_new_tab

#Password Managing - Definition
def genpass(length, use_uppercase, use_numbers, use_special):
    characters = "abcdefghijklmnopqrstuvwxyz"
    if use_uppercase == True:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers == True:
        characters += "0123456789"
    if use_special == True:
        characters += "!@#$%^&*()_+-=[]}{|;':,./<>?"

    password = "".join(random.choice(characters) for _ in range(length))
    return password


#Window Managing
#Initialise the root window
root = Tk()
root.title("Password Generator")
root.geometry("400x300+300+200")
root.configure(bg="#000000")
root.minsize(400, 300)
root.maxsize(400, 300)

#Widgets
#Variables for the checkbuttons to work with the genpass function
genpassuse_uppercase_buttonvariable = BooleanVar(value=True)
genpassuse_numbers_buttonvariable = BooleanVar(value=True)
genpassuse_special_buttonvariable = BooleanVar(value=True)
#Label for the password to be printed on
password_label = Label(root, text="", bg="#000000", fg="#00FF00", font=("Comic Sans MS", 14))
password_label.place(relx=0.5, rely=0.7, anchor=CENTER)
#Length slider for the password length
genpasslengthslider = Scale(root, from_=1, to=32, orient=HORIZONTAL, label="Password Length:", bg="#000000", fg="#00FF00", font=("Comic Sans MS", 6), highlightbackground="#000000", sliderlength=20, length=300)
genpasslengthslider.place(relx=0.5, rely=0.1, anchor=CENTER)
#Uppercase ask for the password
genpassuppercasecheckbox = Checkbutton(root, text="Include Uppercase Letters?", variable=genpassuse_uppercase_buttonvariable, bg="#000000", fg="#00FF00", font=("Comic Sans MS", 6))
genpassuppercasecheckbox.place(relx=0.5, rely=0.2, anchor=CENTER)
#Numbers ask for the password
genpassnumberscheckbox = Checkbutton(root, text="Include Numbers?", variable=genpassuse_numbers_buttonvariable, bg="#000000", fg="#00FF00", font=("Comic Sans MS", 6))
genpassnumberscheckbox.place(relx=0.5, rely=0.3, anchor=CENTER)
#Special characters ask for the password
genpassspecialcheckbox = Checkbutton(root, text="Include Special Characters?", variable=genpassuse_special_buttonvariable, bg="#000000", fg="#00FF00", font=("Comic Sans MS", 6))
genpassspecialcheckbox.place(relx=0.5, rely=0.4, anchor=CENTER)
#Generate password button
genpassbutton = Button(root, text="Generate Password!", command=lambda: password_label.config(text=genpass(genpasslengthslider.get(), genpassuse_uppercase_buttonvariable.get(), genpassuse_numbers_buttonvariable.get(), genpassuse_special_buttonvariable.get())), bg="#000000", fg="#00FF00", font=("Comic Sans MS", 12), activebackground="#00FF00", activeforeground="#000000")
genpassbutton.place(relx=0.5, rely=0.5, anchor=CENTER)







#Opening a popup window
def openpopup():
    popup = Toplevel(root)
    popup.title("Popup")
    popup.geometry("200x100+350+250")
    popup.configure(bg="#000000")
    popup.minsize(200, 100)
    popup.maxsize(200, 100)
    popup_label = Label(popup, text="This is a popup window!", bg="#000000", fg="#00FF00", font=("Comic Sans MS", 12))
    popup_label.place(relx=0.5, rely=0.5, anchor=CENTER)

#Menus
menu = Menu(root)
root.config(menu=menu)

#Options menu
optionmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Options", menu=optionmenu)
optionmenu.add_command(label="Save Configuration")
optionmenu.add_command(label="Open Configuration")
optionmenu.add_separator()
optionmenu.add_command(label="Popup", command=openpopup)
optionmenu.add_command(label="Exit", command=root.quit)

#Help menu
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About the Project", command=lambda: open_new_tab("https://github.com/kavim/python-random-password-generator"))
helpmenu.add_command(label="Contact Me", command=lambda: open_new_tab("mailto:kavi@mistrypi.dev"))

#Initialise the root window (mainloop)
root.mainloop()
