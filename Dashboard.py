"""
References:
https://tkinter.com/
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
https://docs.python.org/3/library/tk.html
https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
"""
import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# classes
from Database import Database
from Popup import Popup
from User import User

class Dashboard(tk.Frame):
    """ creates Dashboard, main page of the application """
    def __init__(self, root):
        self.db = Database() # Database() instance
        self.library = self.db.library # Library() instance
        self.user = None # current user
        self.user_lst = self.db.get_users() # list of users from database
        self.bg = '#fff7e8' # frame background cream color
        # create parent frame and configurations
        super().__init__(root)
        self.config(bg=self.bg)
        self.grid(sticky='NWSE')
        self.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        # Add Some Style
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        # draw widgets
        self.create_widgets()

    def create_widgets(self):
        """ creates all widgets on Dashboard"""
        # User ID dropdown selection
        self.user_label = tk.Label(self,
                                text="Select User ID: ",
                                background=self.bg)
        self.user_label.config(bg='#fff7e8')
        self.user_label.grid(column=1, row=0, sticky='E', pady=10, rowspan=2)

        self.user_entry_var = tk.StringVar()
        self.user_entry = ttk.Combobox(self,
                            textvariable=self.user_entry_var,
                            background=self.bg,
                            state='readonly')
        self.user_entry['values']=self.user_lst +['New User']
        self.user_entry.grid(column=2, row=0, sticky='W', pady=10, rowspan=2)
        # calendar
        self.cal = Calendar(self,
                            selectmode='day',
                            showweeknumbers=False,
                            firstweekday='sunday',
                            selectforeground='#FF5733',
                            headersbackground='#FF5733',
                            foreground='#FF5733')
        self.cal.grid(column=4, row=2, sticky='NWSE', padx=10, pady=10)
        # 'View & Edit Routine' Button. Creates Popup when clicked.
        self.calendar_button = tk.Button(self,
                                        text="View & Edit Routine",
                                        command=lambda: self.getDate())
        self.calendar_button.grid(column=4, row=3)
        # displays message to select User ID
        # if 'View & Edit Routine' clicked but no user ID
        self.calendar_label = tk.Label(self, text="", background=self.bg)
        self.calendar_label.grid(column=4, row=3, sticky="S", pady=10)
        # 'Instructions' button to view instructions
        self.instructions_button = tk.Button(self,
                                            text="Instructions",
                                            command=lambda: self.instructions())
        self.instructions_button.grid(column=1, row=5, sticky='W')
        # draw pie chart
        self.draw_pie()

    def draw_pie(self):
        """ Draws pie chart for Monthly Muslce Distrbution"""
        # create a figure
        self.figure = Figure(figsize=(6,3), dpi=90)
        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().grid(column=1, row=2,
                                                pady=10, padx=10,
                                                columnspan=2, rowspan=2,
                                                sticky='NWSE')
        # makes sure pie chart is drawn when user is selected
        if self.user != None:
            # update user tasks and pie chart
            self.user.update(self.cal.get_displayed_month())
            data = self.user.pie
            muscles = list(data.keys())
            usage = list(data.values())
            if set(usage) == set([0]):
                usage = []
            # create pie plot
            axes = self.figure.add_subplot(anchor="W")
            axes.pie(usage, normalize=True)
            axes.set_title('Monthly Muscle Distribution')
            axes.legend(muscles,
                        loc='center right',
                        bbox_to_anchor=(1.5, 0.5),
                        borderaxespad=0.)

    ############################################################################
    ########################### EVENTS #########################################
    ############################################################################
    def mouse_pressed(self, event):
        """ Refreshes user information based on Dashboard actions """
        # Queries user information when user selected
        if str(event.widget) == ".!dashboard.!combobox":
            self.updateUserLst(self.user)
        # updates user pie chart when calendar selected
        elif self.user != None and str(event.widget) == ".!dashboard.!calendar":
            self.user.update(self.cal.get_displayed_month())
        # refreshes pie chart on window
        self.draw_pie()

    ############################################################################
    ########################### SHARED METHODS #################################
    ############################################################################
    def updateUserLst(self, id):
        """ Takes User ID selection and initalizes User instances """
        # Make 'Select User ID' message disappear
        self.calendar_label.config(text = "")
        id = self.user_entry.get() # combobox selection
        # queries existing user or new user
        self.user = User(self.db, self.user_entry.get())
        # Combobox selection becomes new user id
        if id == 'New User':
            self.user_lst = self.db.get_users()
            self.user_entry['values'] = self.user_lst +['New User']
            self.user_entry_var.set(self.user.id)

    def getDate(self):
        """ Popup window if user is selected else displays msg """
        date = self.cal.get_date()
        date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')
        if self.user != None:
            Popup(self.library, date, self.user, self)
        else:
            self.calendar_label.config(text = "Select a User ID!")

    def instructions(self):
        """ creates Instructions popup window """
        # extract textfile containing instructions string
        with open('instructions.txt', 'r') as f:
            instructions = f.read()
        instructions_frame = tk.Toplevel(self)
        instructions_frame.title("App Instructions")
        instructions_label = tk.Label(instructions_frame, text=instructions)
        instructions_label.pack(ipadx=10, ipady=10)
