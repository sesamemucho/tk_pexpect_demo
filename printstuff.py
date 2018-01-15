#!/usr/bin/env python3
"""Prints stuff.

"""

import select
import sys
import time

TEXT_FILE = "coffee.txt"

class DoPrint():
  def __init__(self):
    self.chartime = 10
    self.mode = 'print'
    with open(TEXT_FILE, "r") as fi:
      self.text = fi.read()

  def run(self):
    fdo = sys.stdout.fileno()
    fdi = sys.stdin.fileno()

    poll = select.poll()
    poll.register(fdi, select.POLLIN)

    charindex = 0
    maxchar = len(self.text)
    while True:
      results = poll.poll(self.chartime)
      if results:
        cmd = sys.stdin.readline().strip()
        if cmd.startswith('slow'):
          self.chartime = 100
          self.mode = 'print'
        elif cmd.startswith('fast'):
          self.chartime = 10
          self.mode = 'print'
        elif cmd.startswith('pause'):
          self.mode = 'pause'
        elif cmd.startswith('print'):
          self.mode = 'print'
        elif cmd.startswith('quit'):
          return
      else:
        if self.mode == 'print':
          print(self.text[charindex], end='', flush=True)
          charindex += 1
          if charindex >= maxchar:
            charindex = 0

if __name__ == "__main__":
  DoPrint().run()


