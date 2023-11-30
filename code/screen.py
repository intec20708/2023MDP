from tkinter import *

w = Tk()
w.title("MDP")
w.geometry("1260x891")

photo = PhotoImage(file="C:/Users/user/Desktop/학교/MDP/image.png")
pLabel = Label(w, image=photo)
pLabel.pack(expand=1, anchor=CENTER)

w.mainloop()
