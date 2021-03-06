#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    Apr 18, 2019 05:47:09 PM +0300  platform: Windows NT

import sys
import new_room_gui

room_name = None
users = None

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

def check_name(event):
    global w
    try:
        if any(x in w.input.get("1.0", 'end-1c') for x in ['\r', '\n', '\t']):
            temp = w.input.get("1.0", 'end-1c').replace('\n', '').replace('\t', '').replace('\r', '')
            w.input.delete("1.0", 'end-1c')
            w.input.insert("end", temp)
        if not w.input.get("1.0", 'end-1c') or any(x in w.input.get("1.0", 'end-1c') for x in ['\r', '\n', '\t']) or w.input.get("1.0", 'end-1c') == 'globally' or w.input.get("1.0", 'end-1c') == 'Main' or '@' in w.input.get("1.0", 'end-1c'):
            w.done.config(state='disable')
        else:
            w.done.config(state='normal')
    except Exception:
        pass


def get_parameter(request, param):
    """
    extarcts out a single parameter from the client request
    :param request: the client request
    :param param: the needed parameter
    return: the needed parameter's value
    """
    if param == "Params":
        return request.split("\r\n\r\n")[1]
    if isinstance(param, type([])):
        return [request.split("\r\n\r\n")[1] if x == "Param" else request.split(x + ": ")[1].split("\r\n")[0] for x in param]
    if isinstance(param, type("")):
        return request.split(param + ": ")[1].split("\r\n")[0]


def add():
    try:
        w.members.insert('0', w.users.get(w.users.curselection()))
        for i in range(len(w.users.get('0', 'end'))):
            if w.users.get('0', 'end')[i] == w.users.get(w.users.curselection()):
                w.users.delete(i)
                break
        sys.stdout.flush()
    except Exception:
        pass


def done():
    global room_name, users
    temp = w.input.get("1.0", 'end-1c').replace('\n', '').replace('\t', '').replace('\r', '')
    room_name = temp
    users = ", ".join(w.members.get('0', 'end'))
    destroy_window()
    sys.stdout.flush()


def remove():
    try:
        w.users.insert('0', w.members.get(w.members.curselection()))
        for i in range(len(w.members.get('0', 'end'))):
            if w.members.get('0', 'end')[i] == w.members.get(w.members.curselection()):
                w.members.delete(i)
                break
        sys.stdout.flush()
    except Exception:
        pass


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level, root
    root.quit()
    top_level.destroy()
    top_level = None
