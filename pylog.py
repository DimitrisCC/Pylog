#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from logic import *


class MainGUI(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.ndbfile = None

        self.parent.wm_title("Pylog")
        self.menu = tk.Menu(self.parent)
        self.parent.geometry("850x600")
        self.parent.config(menu=self.menu)

        self.sub_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.sub_menu)
        self.sub_menu.add_command(label='Save...', command=MainGUI.lol)
        self.sub_menu.add_command(label='Load...', command=MainGUI.lol)

        self.ndb_button = tk.Button(self.parent, text='Load Knowledge Base...', command=self.get_file)
        self.ndb_button.grid(row=0, column=0)

        self.input = tk.scrolledtext.ScrolledText(self.parent, undo=True, height=10, width=10)
        self.input.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S, pady=5)
        self.output = tk.scrolledtext.ScrolledText(self.parent, width=50, undo=True)
        self.output.grid(row=2, column=0)
        self.ndbbox = tk.scrolledtext.ScrolledText(self.parent, width=50, undo=True)

        self.ndbbox.grid(row=2, column=1, columnspan=1)

        self.input.insert(tk.INSERT, ">>>")

    @staticmethod
    def lol():
        print("lolen")

    def get_file(self):
        filename = tk.filedialog.askopenfilename(parent=self.parent, title='Choose a knowledge db file', filetypes = [('Prolog files', '.pl')] )
        if filename is not None:
            file = open(filename, 'r')
            self.ndbfile = file.read
            file.close()
            kb = createKB(filename)
        if self.ndbfile is not None:
            self.ndbbox.configure(state = tk.NORMAL)
            self.ndbbox.delete(1.0, tk.END)
            self.ndbbox.insert(tk.INSERT, self.ndbfile)  # DEBUG
            self.ndbbox.configure(state = tk.DISABLED)
if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
