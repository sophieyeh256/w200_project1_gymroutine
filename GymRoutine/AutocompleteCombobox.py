"""
References:
https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.html
https://docs.python.org/3/howto/sorting.html
https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html
"""
import copy
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk


class AutocompleteCombobox(ttk.Combobox):
    """ Combobox for task entry that searches and autocompletes """
    def __init__(self, frame, completion_list, listbox_var):
        super().__init__(frame)
        self.completion_list = sorted(completion_list, key=str.lower)
        self.hits = []
        self.hits_index = 0
        self.position = 0
        self.listbox_var = listbox_var
        self.library = completion_list
        self.bind('<KeyRelease>', lambda event: self.key_release(event))
        self['values'] = self.completion_list

    def generate_list(self, completion_list):
        self.completion_list = sorted(completion_list, key=str.lower)
        self.hits = []
        self.hits_index = 0
        self.position = 0
        self['values'] = self.completion_list


    def auto(self):
        """ Autocomplete feature """
        hits = []
        # find hits
        for element in self.completion_list:
            if element.lower().startswith(self.get().lower()):
                hits.append(element)
        # new hit list
        if hits != self.hits:
            self.hits_index = 0
            self.hits = hits
        if hits == self.hits and self.hits:
            self.hits_index = (self.hits_index) % len(self.hits)
        # add seleciton range
        if self.hits:
            self.delete(0, tk.END)
            self.insert(0, self.hits[self.hits_index])
            self.select_range(self.position+1, tk.END)
            self.listbox_var.set(self.library[self.hits[self.hits_index]])


    def key_release(self, event):
        """ event handler for the keyrelease event on this widget """
        # delete
        if event.keysym == "BackSpace":
                self.position = self.index(tk.END)
        # delete selected and move cursor left
        elif event.keysym == "Left":
            if self.hits:
                # go back to typing position after auto
                self.delete(self.position+1, tk.END)
                self.position = self.position +1
            else:
                # shift cursor back
                self.position = self.position - 1
        elif event.keysym == "Right":
                self.position = self.index(tk.END) # go to end (no selection)
        else:
            self.position = self.index(tk.END) -1
        # auto complete while typing
        if len(event.keysym) == 1 or event.keysym == 'space':
            self.auto()

    def handle_filter(self, completion_list, filter='All Categories'):
        """ narrow down selection based on filter """
        if filter != 'All Categories':
            new_lst = copy.deepcopy(completion_list)
            for item in completion_list.keys():
                if filter not in completion_list[item]:
                    new_lst.pop(item)
        else:
            new_lst = completion_list
        self.generate_list(new_lst)
        self.auto()

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.grid()
#
#     list = {"CB Belt Flx Neck with belt": ["Neck"],
#         "CB Neck Rotation (with belt) Belt": ["Neck"],
#         "CB Lateral Neck Flexion (with belt) Ltr Flx Belt": ["Neck"],
#         "LV Neck Flexion H": ["Neck"],
#         "LV Lateral Neck Flexion H": ["Neck"],
#         "LV Neck Flexion Flx": ["Neck"]}
#
#     box = AutocompleteCombobox(list)
#     box.grid()
#     root.mainloop()
