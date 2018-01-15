#!/usr/bin/env python3
"""Example/skeleton for using pexpect with tkinter.

"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg

import queue
import threading
import sys
import pexpect
import time
import io


class QueueIO(io.TextIOBase):
  def __init__(self, qname, *args, **kwargs):
    io.TextIOBase.__init__(self, *args, **kwargs)
    self.q = qname

  def write(self, b):
    length = len(b)
    self.q.put(b)
    return length

class TkPexpect():
  def __init__(self):
    # Create top-level window
    self.topwin = tk.Tk()

    self.q = queue.Queue()
    self.commands_to_expect = queue.Queue()

    self.num_coffees = tk.StringVar()

    # Title the app
    self.topwin.title("Tk/Pexpect demo")
    self.worker = threading.Thread(target=self.do_interaction,
                                   daemon=True)
    self.init_gui()

  def do_interaction(self):
    #logfile = QueueIO(self.q)
    child = pexpect.spawn("./printstuff.py", encoding='utf-8')
    #child.logfile_read = sys.stdout
    child.logfile_read = QueueIO(self.q)
    num_coffee = 0
    while True:
      index = child.expect([r'(?i)coffee', pexpect.TIMEOUT], timeout=0.1)
      #index = child.expect([r'(?i)coffee', ])
      if index == 0:
        num_coffee += 1
        self.num_coffees.set(f"cups: {num_coffee}")
        #self.q.put(f"Coffees = {num_coffee}\n")
      elif index == 1:
        try:
          cmd = self.commands_to_expect.get_nowait()
          if cmd:
            child.sendline(cmd)
        except queue.Empty:
          pass

  def update(self):
    try:
      while True:
        line = self.q.get_nowait()
        if line is None:
          self.logbox.delete(1.0, tk.END)
        else:
          self.logbox.insert(tk.END, line.replace("\r", ""))
          self.logbox.see(tk.END)

    except queue.Empty:
      pass

    self.logbox.after(100, self.update)

  def _quit(self):
    """Exit cleanly
    """
    self.topwin.quit()
    self.topwin.destroy()
    sys.exit(0)

  def _start(self):
    self.worker.start()

  def _slow(self):
    self.commands_to_expect.put('slow')

  def _fast(self):
    self.commands_to_expect.put('fast')

  def _pause(self):
    pass

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

    self.starttext = ttk.Button(appframe, text="Start", command=self._start)
    self.starttext.grid(column=0, row=1, pady=4)

    self.slowtext = ttk.Button(appframe, text="Slow", command=self._slow)
    self.slowtext.grid(column=1, row=1, pady=4)

    self.fasttext = ttk.Button(appframe, text="Fast", command=self._fast)
    self.fasttext.grid(column=2, row=1)

    self.coffee = tk.Label(appframe, textvariable=self.num_coffees)
    self.coffee.grid(column=3, row=1)

    self.logbox = scrolledtext.ScrolledText(appframe, width=70, height=20)
    self.logbox.grid(column=0, row=3, sticky='EW', columnspan=4)

    self.update()

  def run(self):
    self.topwin.mainloop()

if __name__ == "__main__":
  TkPexpect().run()
