from tkinter import *
import tkinter.messagebox as messagebox
import re


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLable = Label(self, text="Hello World!")
        self.helloLable.pack()
        self.username = Entry(self)
        self.username.pack()
        self.alertButton = Button(self, text="Hello", command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.username.get() or "world"
        r = re.match(r'^(\d{3,4})-(\d{7,11})', name)
        messagebox.showinfo("Message", r.groups())
        print(r.groups())

if __name__ == "__main__":
    """
    app = Application()
    app.master.title("Hello World")
    app.mainloop()
    """
    r = re.match(r'^(\d+?)(0*)$', "102300")
    print(r.groups())
