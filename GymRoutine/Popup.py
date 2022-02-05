"""
References:
https://tkinter.com/
https://www.tutorialspoint.com/python/python_gui_programming.htm
"""
from datetime import datetime
import random
import sqlite3
import tkinter as tk
from tkinter import ttk
from AutocompleteCombobox import AutocompleteCombobox
from Library import Library
from Database import Database
from User import User

class Popup:
    """ New screen to edit routine for selected date """
    def __init__(self, library, date, user, dashboard):
        self.top = tk.Toplevel()
        self.top.title('Editing a Routine')
        self.top.resizable(0,0)
        self.bg = '#fff7e8'
        self.top.config(background=self.bg)
        self.library = library.__dict__()
        self.categories = library.categories
        self.dashboard = dashboard
        self.date = date
        self.user = user
        self.user_id = self.user.id
        self.addFrame()


    def addFrame(self):
        """ Draws widgets for popup frame """
        # Add Some Style
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        self.style.configure("LabelFrame", background = self.bg)
        # configure Treeview style
        self.style.configure("Treeview",
                        	background = "#D3D3D3",
                        	foreground = "black",
                        	rowheight = 25,
                        	fieldbackground = "#D3D3D3")
        self.style.map('Treeview',
        	background = [('selected', "#347083")])
        # create treeview frame
        tree_frame = tk.Frame(self.top)
        tree_frame.grid(pady = 10, padx = 10)
        # Create a Treeview Scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side = 'right', fill = 'y')
        # Create The Treeview
        self.my_tree = ttk.Treeview(tree_frame,
                                    yscrollcommand = tree_scroll.set,
                                    selectmode = "extended")
        self.my_tree.pack()
        # configure scrollbar
        tree_scroll.config(command = self.my_tree.yview)
        # find day name of a date and add to heading
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        day = day_name[datetime.strptime(self.date, '%Y-%m-%d').weekday()]
        mainColName = day + '\t' + self.date
        self.my_tree['columns'] = (mainColName,"ID", "Date")
        self.my_tree.column("#0", width = 0, stretch = 'NO')
        self.my_tree.column("ID", anchor = 'w', width = 0, stretch = 'NO')
        self.my_tree.column("Date", anchor = 'w', width = 0, stretch = 'NO')
        self.my_tree.column(mainColName, anchor = 'w', width = 250)
        self.my_tree.heading(mainColName, text = mainColName, anchor = 'w')
        # table striped rows
        self.my_tree.tag_configure('oddrow', background = "white")
        self.my_tree.tag_configure('evenrow', background = "lightblue")
        # query user tasks for selected date
        self.query_database()
        # add record entry boxes
        self.data_frame = tk.LabelFrame(self.top, text = "Record")
        self.data_frame.grid(column = 1, row = 0, sticky = 'n', pady = 20, padx = 20)
        # filter task selection by category
        self.task_filter = ttk.Combobox(self.data_frame,
                                        values = ['All Categories'] + list(self.categories),
                                        width = 10,
                                        state = 'readonly')
        self.task_filter.grid(row = 0, column = 0, pady = 10)
        self.task_filter.current(0)
        # combobox to type, search, and select task
        # lists categories for task in combobox
        self.task_listbox_var = tk.StringVar()
        self.task_listbox = tk.Listbox(self.data_frame,
                                    listvariable = self.task_listbox_var,
                                    height = 10, width = 30)
        self.task_listbox.grid(row = 1, column = 1, pady = 20)

        self.task_entry = AutocompleteCombobox(self.data_frame, self.library,
                                                self.task_listbox_var)
        self.task_entry.grid(row = 0, column = 1, pady = 10)
        self.task_entry.focus_set()
        self.task_entry.config(width = 30)
        # Recommend a task
        rec_button = tk.Button(self.data_frame, text = "Autogenerate Task",
                            command = lambda: self.recommend(self.task_filter.get()))
        rec_button.grid(row=0, column=2, pady=10)
        # commands frame
        button_frame = tk.LabelFrame(self.top, text = "Commands")
        button_frame.grid(column = 0, row = 1, columnspan = 2,
                        sticky = 'ew', pady = 20, padx = 20)
        # update task
        update_button = tk.Button(button_frame, text = "Update Record",
                                command = lambda: self.update_record())
        update_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        # add task
        add_button = tk.Button(button_frame, text = "Add Record",
                            command = lambda: self.add_record())
        add_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        # remove all tasks
        remove_all_button = tk.Button(button_frame, text = "Remove All Records",
                                    command = lambda: self.remove_all())
        remove_all_button.grid(row = 0, column = 2, padx = 10, pady = 10)
        # # remove a task
        remove_one_button = tk.Button(button_frame, text = "Remove One Selected",
                                    command = lambda: self.remove_one())
        remove_one_button.grid(row = 0, column = 3, padx = 10, pady = 10)
        # remove mutliple selected
        remove_many_button = tk.Button(button_frame, text = "Remove All Selected",
                                    command = lambda: self.remove_many())
        remove_many_button.grid(row = 0, column = 4, padx = 10, pady = 10)

        select_record_button = tk.Button(button_frame, text = "Clear Entry Boxes",
                                        command = lambda: self.clear_entries())
        select_record_button.grid(row=0, column=7, padx=10, pady=10)

        # bind treeview selection
        self.my_tree.bind("<ButtonRelease-1>",
                        lambda event: self.select_record(event))
        # bind filter
        self.task_filter.bind("<<ComboboxSelected>>",
                        lambda event: self.filter_task_entry(event))

        self.task_entry.bind("<<ComboboxSelected>>", self.task_categories())

    def remove_one(self):
        """ Remove one record """
        try:
            x = self.my_tree.selection()[0]
            self.my_tree.delete(x)
            # Grab record Number
            self.user.delete_task(self.values[1])
            self.dashboard.draw_pie()
        except IndexError:
            pass


    def remove_many(self):
        """ Remove Many records """
        x = self.my_tree.selection()
        for record in x:
            values = self.my_tree.item(record, 'values')
            self.my_tree.delete(record)
            self.user.delete_task(values[1])
            self.dashboard.draw_pie()


    def remove_all(self):
        """ Remove all records """
        for record in self.my_tree.get_children():
            values = self.my_tree.item(record, 'values')
            self.user.delete_task(values[1])
            self.my_tree.delete(record)
            self.dashboard.draw_pie()


    def clear_entries(self):
        """ Clear entry boxes """
        self.task_entry.delete(0, tk.END)
        self.task_listbox_var.set([])

    # Select Record
    def select_record(self, event):
        """ Select Record transferred to entry box """
        try:
            # Clear entry boxes
            self.task_entry.delete(0, tk.END)
            # Grab record Number
            self.selected = self.my_tree.focus()
        	# Grab record values
            self.values = self.my_tree.item(self.selected, 'values')
            # outpus to entry box
            self.task_entry.insert(0, self.values[0])
            self.task_filter.current(0)
            self.task_categories()
        except IndexError:
            pass


    def update_record(self):
        """ after record selected, you can change task """
        try:
            # Grab the record number
            self.selected = self.my_tree.focus()
            oldValues = self.my_tree.item(self.selected, 'values')
            (plan, plan_id, date) = (self.task_entry.get(), oldValues[1], oldValues[2])
            # Update record
            self.my_tree.item(self.selected, text='', values=(plan, plan_id, date))
            self.user.update_task(plan, plan_id)
            # Clear entry box
            self.task_entry.delete(0, tk.END)
            self.dashboard.draw_pie()
        except IndexError:
            pass


    def add_record(self):
        """ add new record """
        if self.in_library():
            # Grab entry values
            task = self.task_entry.get()
            self.user.create_task(self.date, task)
            # Run to pull data from database on start
            self.query_database()
            self.dashboard.draw_pie()


    def query_database(self):
        """ queries user plan and add tasks for that date in treeview """
    	# Clear The Treeview Table
        self.my_tree.delete(*self.my_tree.get_children())
        self.data = Database()
        # User data
        self.user = User(self.data, self.user_id)
        # Add our data to the screen
        count = 0
        for record in self.user.plan:
            if self.date in record:
                if count % 2 == 0:
                    self.my_tree.insert(parent='', index='end',
                                iid=count, text='',
                                values=(record[2], record[0], record[1]),tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='', index='end',
                                iid=count, text='',
                                values=(record[2], record[0], record[1]),tags=('oddrow',))
                count += 1


    def in_library(self):
        """ Checks that entered task is in the library """
        if self.task_entry.get() not in self.library:
            error_frame = tk.Toplevel(self.top)
            error_frame.title("Error Message")
            error_frame.resizable(0,0)
            error_label = tk.Label(error_frame, text="Task not found in exercise data!")
            error_label.pack(ipadx=10, ipady=10)
            return False
        else: return True


    def recommend(self, category='All Categories'):
        in_category = False
        if category == 'All Categories':
            category = min(self.user.pie, key=self.user.pie.get)
        while not in_category:
            rec = random.choice(list(self.library.items()))
            if category == 'All categories' or category in rec[1]:
                in_category = True
        # ('One Arm Incline Push', ['Chest'])
        self.task_entry.set(rec[0])
        self.task_categories()
        return rec


    def filter_task_entry(self, event):
        """ clears entry box and filters dropdown options """
        self.task_entry.handle_filter(self.library, self.task_filter.get())
        self.clear_entries()
        self.task_entry.focus_set()
        self.task_categories()


    def task_categories(self):
        """ display categories associated with task in listbox """
        try:
            self.task_listbox_var.set(self.library[self.task_entry.get()])
        except KeyError:
            self.task_listbox_var.set([])
