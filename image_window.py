import tkinter
from PIL import Image
from PIL import ImageTk
from tkinter import *


class ImageWindow:
    def __init__(self, image):
        self._captcha_text = None

        self.root = Tk()

        img = ImageTk.PhotoImage(image)
        panel = Label(self.root, image=img)
        panel.pack(side="top", fill="both", expand="yes")

        self.e = Entry(width=20)
        b = Button(text="Отправить")
        b.bind('<Button-1>', self.send_captcha)

        self.e.pack()
        b.pack()
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def send_captcha(self, event):
        self._captcha_text = self.e.get()
        self.quit()

    def get_captcha_text(self):
        return self._captcha_text
