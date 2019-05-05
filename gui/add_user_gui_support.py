#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    May 02, 2019 12:49:09 AM +0300  platform: Windows NT

import sys

index = None

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def set_Tk_var():
    global combobox
    combobox = tk.StringVar()
    combobox.set("................................Select User................................")


def defocus(event):
    event.widget.master.focus_set()


def finished():
    global index
    if w.users_list.current() != -1:
        index = w.users_list.current()
        destroy_window()
        sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.eval('::ttk::CancelRepeat')
    root.quit()
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import add_user_gui
    add_user_gui.vp_start_gui()