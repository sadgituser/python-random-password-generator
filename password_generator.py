from tkinter import *
import random
from webbrowser import open_new_tab

root = Tk()
root.title("Password Generator")
root.geometry("400x300+300+200")
root.configure(bg="#000000")
root.minsize(400, 300)
root.maxsize(400, 300)

def openpopup():
    popup = Toplevel(root)
    popup.title("Popup")
    popup.geometry("200x100+350+250")
    popup.configure(bg="#000000")
    popup.minsize(200, 100)
    popup.maxsize(200, 100)
    popup_label = Label(popup, text="This is a popup window!", bg="#000000", fg="#FFFFFF", font=("Comic Sans MS", 12))
    popup_label.place(relx=0.5, rely=0.5, anchor=CENTER)

menu = Menu(root)
root.config(menu=menu)

optionmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Options", menu=optionmenu)
optionmenu.add_command(label="Save Configuration")
optionmenu.add_command(label="Open Configuration")
optionmenu.add_separator()
optionmenu.add_command(label="Popup", command=openpopup)
optionmenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About the Project", command=lambda: open_new_tab("https://github.com/kavim/python-random-password-generator"))
helpmenu.add_command(label="Contact Me", command=lambda: open_new_tab("mailto:kavi@mistrypi.dev"))



root.mainloop()
