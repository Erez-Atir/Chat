#-----------------------Imports-----------------------
import sys
import platform
import Tkinter as tk
import ttk
import main_support


#-----------------------Globals-----------------------
name = None
socket = None


#----------------------Functions----------------------
def vp_start_gui(namepass, socketpass):
    """Starting point when module is the main routine."""
    global val, w, root, name, socket
    name = namepass
    socket = socketpass
    root = tk.Tk()
    root.resizable(False, False)
    root.after(400, main_support.receive)
    root.bind("<<new_room>>", main_support.new_room_creation)
    root.bind('<Return>', main_support.send_message)
    top = top_level(root)
    main_support.init(root, top)
    root.mainloop()

w = None
def create_top_level(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    top = top_level(w)
    main_support.init(w, top, *args, **kwargs)
    return w, top


def destroy_top_level():
    global w
    w.destroy()
    w = None


#-----------------------Classes-----------------------
class top_level:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("784x533+476+183")
        top.title("Cyber End of Year Project - " + name)
        top.configure(background="#d9d9d9")

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=[('selected', _compcolor), ('active', _ana2color)])
        self.notebook = ttk.Notebook(top)
        self.notebook.place(relx=0.0, rely=0.0, relheight=1.006, relwidth=1.0)
        self.notebook.configure(width=784)
        self.notebook.configure(takefocus="")

        self.notebook_tabs = []
        self.notebook_tabs.append(tk.Frame(self.notebook))
        self.notebook.add(self.notebook_tabs[0], padding=3)
        self.notebook.tab(0, text="Main", compound="left", underline="-1",)
        self.notebook_tabs[0].configure(background="#d9d9d9")
        self.notebook_tabs[0].configure(highlightbackground="#d9d9d9")
        self.notebook_tabs[0].configure(highlightcolor="black")

        self.output = []
        self.output.append(ScrolledText(self.notebook_tabs[0]))
        self.output[0].place(relx=0.0, rely=0.0, relheight=0.845, relwidth=0.706)
        self.output[0].configure(background="white")
        self.output[0].configure(state="disabled")
        self.output[0].configure(font="-family {Segoe UI} -size 9")
        self.output[0].configure(foreground="black")
        self.output[0].configure(highlightbackground="#d9d9d9")
        self.output[0].configure(highlightcolor="black")
        self.output[0].configure(insertbackground="black")
        self.output[0].configure(insertborderwidth="3")
        self.output[0].configure(selectbackground="#c4c4c4")
        self.output[0].configure(selectforeground="black")
        self.output[0].configure(width=10)
        self.output[0].configure(wrap="none")
        self.output[0].tag_configure('tag-right', justify='right')
        self.output[0].tag_configure('time', foreground='#808080')
        self.output[0].tag_configure("0", foreground="red")
        self.output[0].tag_configure("1", foreground="green")
        self.output[0].tag_configure("2", foreground="blue")
        self.output[0].tag_configure("3", foreground="cyan")
        self.output[0].tag_configure("4", foreground="yellow")
        self.output[0].tag_configure("5", foreground="magenta")

        self.input = []
        self.input.append(ScrolledText(self.notebook_tabs[0]))
        self.input[0].place(relx=0.0, rely=0.853, relheight=0.12, relwidth=0.706)
        self.input[0].configure(background="white")
        self.input[0].configure(font="-family {Segoe UI} -size 9")
        self.input[0].configure(foreground="black")
        self.input[0].configure(highlightbackground="#d9d9d9")
        self.input[0].configure(highlightcolor="black")
        self.input[0].configure(insertbackground="black")
        self.input[0].configure(insertborderwidth="3")
        self.input[0].configure(selectbackground="#c4c4c4")
        self.input[0].configure(selectforeground="black")
        self.input[0].configure(width=10)
        self.input[0].configure(wrap="none")

        self.send_button = []
        self.send_button.append(tk.Button(self.notebook_tabs[0]))
        self.send_button[0].place(relx=0.712, rely=0.853, height=64, relwidth=0.271)
        self.send_button[0].configure(activebackground="#ececec")
        self.send_button[0].configure(activeforeground="#000000")
        self.send_button[0].configure(background="#d9d9d9")
        self.send_button[0].configure(command=main_support.send_message)
        self.send_button[0].configure(disabledforeground="#a3a3a3")
        self.send_button[0].configure(font="-family {Segoe UI} -size 22")
        self.send_button[0].configure(foreground="#000000")
        self.send_button[0].configure(highlightbackground="#d9d9d9")
        self.send_button[0].configure(highlightcolor="black")
        self.send_button[0].configure(pady="0")
        self.send_button[0].configure(text="""Send""")
        self.send_button[0].configure(width=117)

        self.members_label = []
        self.members_label.append(tk.Label(self.notebook_tabs[0]))
        self.members_label[0].place(relx=0.705, rely=-0.003, height=38, width=112)
        self.members_label[0].configure(background="#d9d9d9")
        self.members_label[0].configure(disabledforeground="#a3a3a3")
        self.members_label[0].configure(font="-family {Segoe UI} -size 18")
        self.members_label[0].configure(foreground="#000000")
        self.members_label[0].configure(text="""Members:""")

        self.members_list = []
        self.members_list.append(ScrolledListBox(self.notebook_tabs[0]))
        self.members_list[0].place(relx=0.712, rely=0.069, relheight=0.776, relwidth=0.271)
        self.members_list[0].insert('end', name)
        self.members_list[0].configure(background="white")
        self.members_list[0].configure(disabledforeground="#a3a3a3")
        self.members_list[0].configure(font="-family {Courier New} -size 10")
        self.members_list[0].configure(foreground="black")
        self.members_list[0].configure(highlightbackground="#d9d9d9")
        self.members_list[0].configure(highlightcolor="#d9d9d9")
        self.members_list[0].configure(selectbackground="#c4c4c4")
        self.members_list[0].configure(selectforeground="black")
        self.members_list[0].configure(width=10)

        self.managers_list = [None]
        self.mangaers_label = [None]
        self.mute_button = [None]
        self.kick_button = [None]
        self.appoint_button = [None]
        self.add_button = [None]

        self.new_room_button = tk.Button(top)
        self.new_room_button.place(relx=0.899, rely=0.0, height=22, width=80)
        self.new_room_button.configure(activebackground="#ececec")
        self.new_room_button.configure(activeforeground="#000000")
        self.new_room_button.configure(background="#d9d9d9")
        self.new_room_button.configure(command=main_support.new_room)
        self.new_room_button.configure(disabledforeground="#a3a3a3")
        self.new_room_button.configure(foreground="#000000")
        self.new_room_button.configure(highlightbackground="#d9d9d9")
        self.new_room_button.configure(highlightcolor="black")
        self.new_room_button.configure(pady="0")
        self.new_room_button.configure(text="New Room")
        self.new_room_button.configure(width=19)

    def add_room(self, room_name, you_manager=False, manager_name=None):
        print room_name
        self.notebook_tabs.append(tk.Frame(self.notebook))
        self.notebook.add(self.notebook_tabs[len(self.notebook_tabs)-1], padding=3)
        self.notebook.tab(len(self.notebook_tabs)-1, text=room_name, compound="right", underline="-1",)
        self.notebook_tabs[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.notebook_tabs[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.notebook_tabs[len(self.notebook_tabs)-1].configure(highlightcolor="black")

        self.output.append(ScrolledText(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.output[len(self.notebook_tabs)-1].place(relx=0.0, rely=0.0, relheight=0.845, relwidth=0.706)
        self.output[len(self.notebook_tabs)-1].configure(background="white")
        self.output[len(self.notebook_tabs)-1].configure(state="disabled")
        self.output[len(self.notebook_tabs)-1].configure(font="-family {Segoe UI} -size 9")
        self.output[len(self.notebook_tabs)-1].configure(foreground="black")
        self.output[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.output[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.output[len(self.notebook_tabs)-1].configure(insertbackground="black")
        self.output[len(self.notebook_tabs)-1].configure(insertborderwidth="3")
        self.output[len(self.notebook_tabs)-1].configure(selectbackground="#c4c4c4")
        self.output[len(self.notebook_tabs)-1].configure(selectforeground="black")
        self.output[len(self.notebook_tabs)-1].configure(width=10)
        self.output[len(self.notebook_tabs)-1].configure(wrap="none")
        self.output[len(self.notebook_tabs)-1].tag_configure('tag-right', justify='right')
        self.output[len(self.notebook_tabs)-1].tag_configure('time', foreground='#808080')
        self.output[len(self.notebook_tabs)-1].tag_configure("0", foreground="red")
        self.output[len(self.notebook_tabs)-1].tag_configure("1", foreground="green")
        self.output[len(self.notebook_tabs)-1].tag_configure("2", foreground="blue")
        self.output[len(self.notebook_tabs)-1].tag_configure("3", foreground="cyan")
        self.output[len(self.notebook_tabs)-1].tag_configure("4", foreground="yellow")
        self.output[len(self.notebook_tabs)-1].tag_configure("5", foreground="magenta")

        self.input.append(ScrolledText(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.input[len(self.notebook_tabs)-1].place(relx=0.0, rely=0.853, relheight=0.12, relwidth=0.553)
        self.input[len(self.notebook_tabs)-1].configure(background="white")
        self.input[len(self.notebook_tabs)-1].configure(font="-family {Segoe UI} -size 9")
        self.input[len(self.notebook_tabs)-1].configure(foreground="black")
        self.input[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.input[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.input[len(self.notebook_tabs)-1].configure(insertbackground="black")
        self.input[len(self.notebook_tabs)-1].configure(insertborderwidth="3")
        self.input[len(self.notebook_tabs)-1].configure(selectbackground="#c4c4c4")
        self.input[len(self.notebook_tabs)-1].configure(selectforeground="black")
        self.input[len(self.notebook_tabs)-1].configure(width=10)
        self.input[len(self.notebook_tabs)-1].configure(wrap="none")

        self.send_button.append(tk.Button(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.send_button[len(self.notebook_tabs)-1].place(relx=0.558, rely=0.853, height=64, width=117)
        self.send_button[len(self.notebook_tabs)-1].configure(activebackground="#ececec")
        self.send_button[len(self.notebook_tabs)-1].configure(activeforeground="#000000")
        self.send_button[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.send_button[len(self.notebook_tabs)-1].configure(command=main_support.send_message)
        self.send_button[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.send_button[len(self.notebook_tabs)-1].configure(font="-family {Segoe UI} -size 22")
        self.send_button[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.send_button[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.send_button[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.send_button[len(self.notebook_tabs)-1].configure(pady="0")
        self.send_button[len(self.notebook_tabs)-1].configure(text="""Send""")
        self.send_button[len(self.notebook_tabs)-1].configure(width=117)

        self.managers_list.append(ScrolledListBox(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.managers_list[len(self.notebook_tabs)-1].place(relx=0.712, rely=0.069, relheight=0.304, relwidth=0.271)
        self.managers_list[len(self.notebook_tabs)-1].configure(background="white")
        self.managers_list[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.managers_list[len(self.notebook_tabs)-1].configure(font="-family {Courier New} -size 10")
        self.managers_list[len(self.notebook_tabs)-1].configure(foreground="black")
        self.managers_list[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.managers_list[len(self.notebook_tabs)-1].configure(highlightcolor="#d9d9d9")
        self.managers_list[len(self.notebook_tabs)-1].configure(selectbackground="#c4c4c4")
        self.managers_list[len(self.notebook_tabs)-1].configure(selectforeground="black")
        self.managers_list[len(self.notebook_tabs)-1].configure(width=10)
        if you_manager:
            self.managers_list[len(self.notebook_tabs)-1].insert('end', name)
        else:
            self.managers_list[len(self.notebook_tabs)-1].insert('end', manager_name)

        self.mangaers_label.append(tk.Label(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.mangaers_label[len(self.notebook_tabs)-1].place(relx=0.705, rely=-0.003, height=38, width=116)
        self.mangaers_label[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.mangaers_label[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.mangaers_label[len(self.notebook_tabs)-1].configure(font="-family {Segoe UI} -size 18")
        self.mangaers_label[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.mangaers_label[len(self.notebook_tabs)-1].configure(text="""Managers:""")

        self.members_label.append(tk.Label(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.members_label[len(self.notebook_tabs)-1].place(relx=0.705, rely=0.373, height=38, width=112)
        self.members_label[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.members_label[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.members_label[len(self.notebook_tabs)-1].configure(font="-family {Segoe UI} -size 18")
        self.members_label[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.members_label[len(self.notebook_tabs)-1].configure(text="""Members:""")

        self.members_list.append(ScrolledListBox(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.members_list[len(self.notebook_tabs)-1].place(relx=0.712, rely=0.441, relheight=0.402, relwidth=0.271)
        self.members_list[len(self.notebook_tabs)-1].configure(background="white")
        self.members_list[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.members_list[len(self.notebook_tabs)-1].configure(font="-family {Courier New} -size 10")
        self.members_list[len(self.notebook_tabs)-1].configure(foreground="black")
        self.members_list[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.members_list[len(self.notebook_tabs)-1].configure(highlightcolor="#d9d9d9")
        self.members_list[len(self.notebook_tabs)-1].configure(selectbackground="#c4c4c4")
        self.members_list[len(self.notebook_tabs)-1].configure(selectforeground="black")
        self.members_list[len(self.notebook_tabs)-1].configure(width=10)
        self.members_list[len(self.notebook_tabs)-1].insert('end', name)
        self.members_list[len(self.notebook_tabs)-1].bind('<Button-1>', main_support.members_click)

        self.mute_button.append(tk.Button(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.mute_button[len(self.notebook_tabs)-1].place(relx=0.718, rely=0.853, height=24, width=97)
        self.mute_button[len(self.notebook_tabs)-1].configure(activebackground="#ececec")
        self.mute_button[len(self.notebook_tabs)-1].configure(activeforeground="#000000")
        self.mute_button[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.mute_button[len(self.notebook_tabs)-1].configure(command=main_support.un_mute)
        self.mute_button[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.mute_button[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.mute_button[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.mute_button[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.mute_button[len(self.notebook_tabs)-1].configure(pady="0")
        self.mute_button[len(self.notebook_tabs)-1].configure(text="""Mute""")
        self.mute_button[len(self.notebook_tabs)-1].configure(width=97)
        if not you_manager:
            self.mute_button[len(self.notebook_tabs)-1].config(state='disable')

        self.kick_button.append(tk.Button(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.kick_button[len(self.notebook_tabs)-1].place(relx=0.853, rely=0.853, height=24, width=97)
        self.kick_button[len(self.notebook_tabs)-1].configure(activebackground="#ececec")
        self.kick_button[len(self.notebook_tabs)-1].configure(activeforeground="#000000")
        self.kick_button[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.kick_button[len(self.notebook_tabs)-1].configure(command=main_support.kick)
        self.kick_button[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.kick_button[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.kick_button[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.kick_button[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.kick_button[len(self.notebook_tabs)-1].configure(pady="0")
        self.kick_button[len(self.notebook_tabs)-1].configure(text="""Kick""")
        self.kick_button[len(self.notebook_tabs)-1].configure(width=97)
        if not you_manager:
            self.kick_button[len(self.notebook_tabs)-1].config(state='disable')

        self.appoint_button.append(tk.Button(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.appoint_button[len(self.notebook_tabs)-1].place(relx=0.718, rely=0.922, height=24, width=97)
        self.appoint_button[len(self.notebook_tabs)-1].configure(activebackground="#ececec")
        self.appoint_button[len(self.notebook_tabs)-1].configure(activeforeground="#000000")
        self.appoint_button[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.appoint_button[len(self.notebook_tabs)-1].configure(command=main_support.appoint_manager)
        self.appoint_button[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.appoint_button[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.appoint_button[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.appoint_button[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.appoint_button[len(self.notebook_tabs)-1].configure(pady="0")
        self.appoint_button[len(self.notebook_tabs)-1].configure(text="""Make Manager""")
        self.appoint_button[len(self.notebook_tabs)-1].configure(width=97)
        if not you_manager:
            self.appoint_button[len(self.notebook_tabs)-1].config(state='disable')

        self.add_button.append(tk.Button(self.notebook_tabs[len(self.notebook_tabs)-1]))
        self.add_button[len(self.notebook_tabs)-1].place(relx=0.853, rely=0.922, height=24, width=97)
        self.add_button[len(self.notebook_tabs)-1].configure(activebackground="#ececec")
        self.add_button[len(self.notebook_tabs)-1].configure(activeforeground="#000000")
        self.add_button[len(self.notebook_tabs)-1].configure(background="#d9d9d9")
        self.add_button[len(self.notebook_tabs)-1].configure(command=main_support.add_user)
        self.add_button[len(self.notebook_tabs)-1].configure(disabledforeground="#a3a3a3")
        self.add_button[len(self.notebook_tabs)-1].configure(foreground="#000000")
        self.add_button[len(self.notebook_tabs)-1].configure(highlightbackground="#d9d9d9")
        self.add_button[len(self.notebook_tabs)-1].configure(highlightcolor="black")
        self.add_button[len(self.notebook_tabs)-1].configure(pady="0")
        self.add_button[len(self.notebook_tabs)-1].configure(text="""Add User""")
        self.add_button[len(self.notebook_tabs)-1].configure(width=97)
        if not you_manager:
            self.add_button[len(self.notebook_tabs)-1].config(state='disable')

    def delete_room(self, index):
        self.notebook.forget(self.notebook_tabs[index])
        self.notebook_tabs.remove(self.notebook_tabs[index])
        self.output.remove(self.output[index])
        self.input.remove(self.input[index])
        self.send_button.remove(self.send_button[index])
        self.managers_list.remove(self.managers_list[index])
        self.mangaers_label.remove(self.mangaers_label[index])
        self.members_label.remove(self.members_label[index])
        self.members_list.remove(self.members_list[index])
        self.mute_button.remove(self.mute_button[index])
        self.kick_button.remove(self.kick_button[index])
        self.appoint_button.remove(self.appoint_button[index])
        self.add_button.remove(self.add_button[index])

    def make_manager(self, index):
        self.managers_list[index].insert('end', name)
        self.mute_button[index].config(state='normal')
        self.kick_button[index].config(state='normal')
        self.appoint_button[index].config(state='normal')
        self.add_button[index].config(state='normal')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


#----------------------Functions----------------------
def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


#-----------------------Classes-----------------------
class ScrolledText(AutoScroll, tk.Text):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledListBox(AutoScroll, tk.Listbox):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


#----------------------Functions----------------------
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui(None, None)
