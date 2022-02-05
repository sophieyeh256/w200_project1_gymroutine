"""
Run this file to create and start the program!
Lines of code: 623
Reference:
https://www.tutorialspoint.com/python/python_gui_programming.htm
"""
# packages
import tkinter as tk
# classes
from Dashboard import Dashboard
from Database import Database
from Library import Library
from User import User

class App(tk.Tk):
    """ Creates root frame and initializes program """
    def __init__(self, width=700, height=400):
        # create root frame and configure
        super().__init__()
        self.title('My Gym Routine')
        self.iconbitmap('gym.ico') # mini icon
        self.geometry("900x600") # window dimensions

        # Allow window resizing
        self.resizable(1,1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create instance of Dashboard Frame inside root
        self.mode = Dashboard(self)

        # when a user is selected or created, user database and pie chart updates.
        self.bind("<<ComboboxSelected>>", lambda event:
                                            self.mode.mouse_pressed(event))

        # updates pie chart when you calendar month/year changes
        self.bind("<<CalendarSelected>>", lambda event:
                                            self.mode.mouse_pressed(event))

if __name__ == "__main__":
    app = App()
    app.bind('<q>', lambda event=None: app.destroy())
    app.mainloop()
    print("bye!")
