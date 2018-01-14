#!/usr/bin/env python3
"""Example/skeleton for using pexpect with tkinter.

"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg

import sys
import pexpect

class TkPexpect():
  def __init__(self):
    # Create top-level window
    self.topwin = tk.Tk()

    # Title the app
    self.topwin.title("Tk/Pepexct demo")
    self.init_gui()


  def _quit(self):
    """Exit cleanly
    """
    self.topwin.quit()
    self.topwin.destroy()
    sys.exit(0)

  def init_gui(self):
    appframe = ttk.LabelFrame(self.topwin, text="TkPexpect")
    appframe.grid(column=0, row=0, padx=8, pady=6)
    appframe.pack(expand=1, fill="both")
    # # Add a menu bar
    menu_bar = Menu(self.topwin)
    self.topwin.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=self._quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

  def run(self):
    self.topwin.mainloop()

if __name__ == "__main__":
  TkPexpect().run()
