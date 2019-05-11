#-----------------------Imports-----------------------
import sys
import ctypes
import Tkinter as tk
import ttk
import main
import time
import new_room_gui
import tkMessageBox
import errno
import traceback
import socket
from select import select
import add_user_gui


#-----------------------Globals-----------------------
name = None
my_socket = None
users = []
hardcoded_colors = []
new_room_request = None
first = True
muted = {}


#----------------------Functions----------------------
def error():
    pass


def receive():
    global root, w, my_socket, users, new_room_request, first
    nextime = ''
    try:
        received = ''
        if not first:
            rlist, wlist, xlist = select([my_socket], [my_socket], [my_socket])
            if my_socket in rlist:
                received = nextime + my_socket.recv(1024)
                nextime = ''
                while received and received[::-1][:6] != '\r\n\r\n\r\n'[::-1]:
                    received += my_socket.recv(1024)
                    for x in received.split('\r\n\r\n\r\n'):
                        nextime = received.replace(received.split('\r\n\r\n\r\n')[0], '')
                    if nextime:
                        received = received.replace(nextime, '')
                        break
                for data in received.split('\r\n\r\n\r\n'):
                    if data:
                        #print data
                        index = 0
                        if get_parameter(data, 'To') != 'globally':
                            for room in w.notebook.tabs():
                                if get_parameter(data, 'To') == w.notebook.tab(room, option="text"):
                                    index = w.notebook.index(room)

                        func = get_parameter(data, 'Func')
                        if func == 'message':
                            w.output[index].config(state='normal')
                            who, said, when = get_parameter(data, "Name, Param, Time".split(", "))
                            when = "[" + when + "]"
                            w.output[index].insert('end-1c', who + ": ", str(hardcoded_colors.index(who) % 6))
                            w.output[index].insert('end-1c', said + '\n')
                            w.output[index].insert('end-1c', when + '\n\n', 'time')
                            w.output[index].config(state='disable')

                        elif func == 'joined':
                            w.output[index].config(state='normal')
                            msg = ''
                            if get_parameter(data, "To") == "globally":
                                msg = "%s has joined the chat.\n\n" % (get_parameter(data, "Name"))
                                if get_parameter(data, "Name") != 'You' and get_parameter(data, "Name") != name:
                                    users.append(get_parameter(data, "Name"))
                                    if get_parameter(data, "Name") not in hardcoded_colors:
                                        hardcoded_colors.append(get_parameter(data, "Name"))
                            elif get_parameter(data, "Name") == 'You' or get_parameter(data, "Name") == name:
                                new_room_request = data
                                root.event_generate("<<new_room>>")
                            else:
                                msg = "%s has joined the room - %s.\n\n" % (get_parameter(data, "Name"), get_parameter(data, "To"))
                            w.output[index].insert('end-1c', msg)
                            w.output[index].config(state='disable')
                            if get_parameter(data, "Name") != 'You' and get_parameter(data, "Name") != name:
                                w.members_list[index].insert('end', get_parameter(data, "Name"))
                            if get_parameter(data, "Name") not in users:
                                if get_parameter(data, "Name") != 'You' and get_parameter(data, "Name") != name:
                                    users.append(get_parameter(data, "Name"))
                                    if get_parameter(data, "Name") not in hardcoded_colors:
                                        hardcoded_colors.append(get_parameter(data, "Name"))

                        if func == 'view-participants':
                            if data.split('\r\n\r\n')[1]:
                                for user in data.split('\r\n\r\n')[1].split(', '):
                                    if user != name and user != 'You':
                                        if user not in w.members_list[index].get('0', 'end'):
                                            w.members_list[index].insert('end', user)
                                        if user not in users:
                                            if get_parameter(data, "Name") != 'You' and get_parameter(data, "Name") != name:
                                                users.append(user)
                                                if user not in hardcoded_colors:
                                                    hardcoded_colors.append(user)

                        if func == 'view-managers':
                            if data.split('\r\n\r\n')[1]:
                                for user in data.split('\r\n\r\n')[1].split(', '):
                                    if user != name:
                                        if user not in w.managers_list[index].get('0', 'end'):
                                            w.managers_list[index].insert('end', user)

                        elif func == 'exit':
                            w.output[index].config(state='normal')
                            if get_parameter(data, "To") == "globally":
                                msg = "%s has quit the chat.\n\n" % (get_parameter(data, "Name"))
                                w.output[index].insert('end-1c', msg)
                                w.output[index].config(state='disable')
                                for i in range(len(w.members_list[index].get('0', 'end'))):
                                    if w.members_list[index].get('0', 'end')[i] == get_parameter(data, "Name"):
                                        w.members_list[index].delete(i)
                                        break
                            else:
                                msg = "%s has quit the room - %s.\n\n" % (get_parameter(data, "Name"), get_parameter(data, "To"))
                                w.output[index].insert('end-1c', msg)
                                w.output[index].config(state='disable')
                                if get_parameter(data, "Name") in muted[get_parameter(data, 'To')]:
                                    muted[get_parameter(data, 'To')].remove(get_parameter(data, 'Name'))
                                for i in range(len(w.members_list[index].get('0', 'end'))):
                                    if w.members_list[index].get('0', 'end')[i] == get_parameter(data, "Name"):
                                        w.members_list[index].delete(i)
                                        break
                                for i in range(len(w.managers_list[index].get('0', 'end'))):
                                    if w.managers_list[index].get('0', 'end')[i] == get_parameter(data, "Name"):
                                        w.managers_list[index].delete(i)
                                        break

                        elif func == 'create':
                            if get_parameter(data, 'Params') == 'OK':
                                new_room_request = data
                                root.event_generate("<<new_room>>", when='now')
                            else:
                                tkMessageBox.showerror("Error!", "Room name is already taken!\nPlease choose a different one.")
                                new_room()

                        elif func == 'muted':
                            if get_parameter(data, 'Params') == 'You are muted in this room.':
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You are muted in this room so other people can't see your messages\n", 'tag-right')
                                w.output[index].config(state='disable')
                            elif get_parameter(data, 'Params') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You have been muted in this room by %s\n" % (get_parameter(data, "Name")), 'tag-right')
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].append(get_parameter(data, 'Params'))
                            elif get_parameter(data, 'Name') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You muted %s in this room\n" % (get_parameter(data, "Params")), 'tag-right')
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].append(get_parameter(data, 'Params'))
                            else:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "%s has muted %s in this room.\n\n" % (get_parameter(data, "Name"), get_parameter(data, 'Params')))
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].append(get_parameter(data, 'Params'))
                            root.after(50, real_members_click_because_tkinter_is_not_working_properly)

                        elif func == 'unmuted':
                            if get_parameter(data, 'Params') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You have been unmuted in this room by %s\n" % (get_parameter(data, "Name")), 'tag-right')
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].remove(get_parameter(data, 'Params'))
                            elif get_parameter(data, 'Name') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You unmuted %s in this room\n" % (get_parameter(data, "Params")), 'tag-right')
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].remove(get_parameter(data, 'Params'))
                            else:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "%s has unmuted %s in this room.\n\n" % (get_parameter(data, "Name"), get_parameter(data, 'Params')))
                                w.output[index].config(state='disable')
                                muted[w.notebook.tab(index, option="text")].remove(get_parameter(data, 'Params'))
                            root.after(50, real_members_click_because_tkinter_is_not_working_properly)

                        elif func == 'kick':
                            if get_parameter(data, 'Params') == name:
                                tkMessageBox.showinfo("Sorry", "You have been kicked from the room \"%s\" by %s" % (get_parameter(data, "To"), get_parameter(data, "Name")))
                                w.delete_room(index)
                            elif get_parameter(data, 'Name') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You kicked %s from this room\n" % (get_parameter(data, "Params")), 'tag-right')
                                w.output[index].config(state='disable')
                                for i in range(len(w.members_list[index].get('0', 'end'))):
                                    if w.members_list[index].get('0', 'end')[i] == get_parameter(data, "Params"):
                                        w.members_list[index].delete(i)
                                        break
                                for i in range(len(w.managers_list[index].get('0', 'end'))):
                                    if w.managers_list[index].get('0', 'end')[i] == get_parameter(data, "Params"):
                                        w.managers_list[index].delete(i)
                                        break
                            else:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "%s has kicked %s from this room.\n\n" % (get_parameter(data, "Name"), get_parameter(data, 'Params')))
                                w.output[index].config(state='disable')
                                for i in range(len(w.members_list[index].get('0', 'end'))):
                                        if w.members_list[index].get('0', 'end')[i] == get_parameter(data, "Params"):
                                            w.members_list[index].delete(i)
                                            break
                                for i in range(len(w.managers_list[index].get('0', 'end'))):
                                    if w.managers_list[index].get('0', 'end')[i] == get_parameter(data, "Params"):
                                        w.managers_list[index].delete(i)
                                        break
                            root.after(50, real_members_click_because_tkinter_is_not_working_properly)

                        elif func == 'appoint-manager':
                            if get_parameter(data, 'Params') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You have been promoted to manager in this room by %s\n" % (get_parameter(data, "Name")), 'tag-right')
                                w.output[index].config(state='disable')
                                w.make_manager(index)
                            elif get_parameter(data, 'Name') == name:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "You promoted %s to manager\n" % (get_parameter(data, "Params")), 'tag-right')
                                w.output[index].config(state='disable')
                                w.managers_list[index].insert('end', get_parameter(data, 'Params'))
                            else:
                                w.output[index].config(state='normal')
                                w.output[index].insert('end-1c', "%s has promoted %s to a manager in this room.\n\n" % (get_parameter(data, "Name"), get_parameter(data, 'Params')))
                                w.output[index].config(state='disable')
                                w.managers_list[index].insert('end', get_parameter(data, 'Params'))
                            root.after(50, real_members_click_because_tkinter_is_not_working_properly)

                if not received:
                    exit()
        else:
            first = False
            time.sleep(0.05)
            recap()

    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()

    finally:
        root.after(50, receive)
        sys.stdout.flush()


def new_room_creation(event):
    global new_room_request
    if new_room_request:
        if get_parameter(new_room_request, 'Params') == 'OK':
            w.add_room(get_parameter(new_room_request, 'To'), True)
            muted[get_parameter(new_room_request, 'To')] = []
        else:
            w.add_room(get_parameter(new_room_request, 'To'), False, get_parameter(new_room_request, 'Params'))
            muted[get_parameter(new_room_request, 'To')] = []
        recap(get_parameter(new_room_request, 'To'))
        get_managers(get_parameter(new_room_request, 'To'))
        new_room_request = None


def get_parameter(request, param):
    """
    extarcts out a single parameter from the client request
    :param request: the client request
    :param param: the needed parameter
    return: the needed parameter's value
    """
    try:
        if param == "Params":
            return request.split("\r\n\r\n")[1]
        if isinstance(param, type([])):
            return [request.split("\r\n\r\n")[1] if x == "Param" else request.split(x + ": ")[1].split("\r\n")[0] for x in param]
        if isinstance(param, type("")):
            return request.split(param + ": ")[1].split("\r\n")[0]
    except Exception:
        return None


def add_user():
    global users, name
    room = w.notebook.tab(w.notebook.select(), "text")
    user = add_user_gui.vp_start_gui([x for x in users if x != name and x not in w.members_list[w.notebook.index(w.notebook.select())].get('0', 'end')])
    if user:
        my_socket.send("Name: " + name + "\r\nFunc: add\r\nTo: " + room + "\r\n\r\n" + user + "\r\n\r\n\r\n")
    sys.stdout.flush()


def appoint_manager():
    try:
        global w, my_socket, name, muted
        selected = w.members_list[w.notebook.index(w.notebook.select())].get(w.members_list[w.notebook.index(w.notebook.select())].curselection())
        my_socket.send("Name: " + name + "\r\nFunc: appoint-manager\r\nTo: " + w.notebook.tab(w.notebook.select(), "text") + "\r\n\r\n" + selected + "\r\n\r\n\r\n")
        if selected in muted[w.notebook.tab(w.notebook.select(), "text")]:
            my_socket.send("Name: " + name + "\r\nFunc: unmute\r\nTo: " + w.notebook.tab(w.notebook.index(w.notebook.select()), option="text") + "\r\n\r\n" + selected + "\r\n\r\n\r\n")
            w.mute_button[w.notebook.index(w.notebook.select())].configure(text='Mute')
    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()
    sys.stdout.flush()


def kick():
    try:
        global w, my_socket, name, muted
        selected = w.members_list[w.notebook.index(w.notebook.select())].get(w.members_list[w.notebook.index(w.notebook.select())].curselection())
        if selected == name:
            if name in w.managers_list[w.notebook.index(w.notebook.select())].get('0', 'end') and len(w.managers_list[w.notebook.index(w.notebook.select())].get('0', 'end')) == 1:
                tkMessageBox.showerror("Error!", "You can't exit a room if you are the only manger of it!\nPlease appoint another manager before you can exit.")
            else:
                if tkMessageBox.askquestion('Exit Room', 'Are you sure you want to exit this room?', icon='warning') == 'yes':
                    my_socket.send("Name: " + name + "\r\nFunc: exit\r\nTo: " + w.notebook.tab(w.notebook.select(), "text") + "\r\n\r\nNone\r\n\r\n\r\n")
                    w.delete_room(w.notebook.index(w.notebook.select()))
        else:
            my_socket.send("Name: " + name + "\r\nFunc: kick\r\nTo: " + w.notebook.tab(w.notebook.select(), "text") + "\r\n\r\n" + selected + "\r\n\r\n\r\n")

    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()
    sys.stdout.flush()


def send_message(event=None):
    try:
        global w, my_socket
        if not event:
            shift = False
        else:
            # Manual way to get the modifiers
            c = event.keysym
            s = event.state
            ctrl = (s & 0x4) != 0
            alt = (s & 0x8) != 0 or (s & 0x80) != 0
            shift = (s & 0x1) != 0
        if not shift:
            msg = w.input[w.notebook.index(w.notebook.select())].get("1.0", 'end-1c')
            if msg:
                if event:
                    msg = msg[::-1][1:][::-1]
                while '\n\n' in msg or '\t' in msg or "\r" in msg or "  " in msg:
                    msg = msg.replace('\n\n', '\n').replace('\t', ' ').replace('\r', '\t').replace('  ', ' ')
                while msg[:2] == "\n" or msg[:2] == "\t" or msg[:2] == "\r":
                    msg = msg[2:]
                while msg[::-1][:2] == "\n" or msg[::-1][:2] == "\t" or msg[::-1][:2] == "\r":
                    msg = msg[::-1][1:][::-1]
                while msg[0] == ' ':
                    msg = msg[1:]
                while msg[::-1][0] == ' ':
                    msg = msg[::-1][1:][::-1]

                if w.notebook.tab(w.notebook.select(), "text") == 'Main':
                    my_socket.send("Name: " + name + "\r\nFunc: message\r\nTo: globally\r\n\r\n" + msg + '\r\n\r\n\r\n')
                else:
                    my_socket.send("Name: " + name + "\r\nFunc: message\r\nTo: " + w.notebook.tab(w.notebook.select(), "text") + "\r\n\r\n" + msg + '\r\n\r\n\r\n\r\n')

                w.output[w.notebook.index(w.notebook.select())].config(state='normal')
                w.output[w.notebook.index(w.notebook.select())].insert('end', msg + "\n", 'tag-right')
                w.output[w.notebook.index(w.notebook.select())].config(state='disable')
                w.input[w.notebook.index(w.notebook.select())].delete('1.0', 'end')

    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()
    sys.stdout.flush()


def members_click(event):
    global root
    root.after(50, real_members_click_because_tkinter_is_not_working_properly)



def real_members_click_because_tkinter_is_not_working_properly():
    """
    Sorry, but when you have a click event for a list the new selected item is not update until after the event.
    That's fucking stupid!
    So I made the click event that only adds to event queue this function.
    You can see in the name of this function how severe was the micro aggression I have developed...
    """
    global w, root, name
    try:
        selected = None
        try:
            selected = w.members_list[w.notebook.index(w.notebook.select())].get(w.members_list[w.notebook.index(w.notebook.select())].curselection())
        except Exception:
            pass

        if selected:
            if selected == name:
                w.kick_button[w.notebook.index(w.notebook.select())].configure(text='Exit')
                w.kick_button[w.notebook.index(w.notebook.select())].config(state='normal')
                w.mute_button[w.notebook.index(w.notebook.select())].config(state='disable')
                w.appoint_button[w.notebook.index(w.notebook.select())].config(state='disable')
            else:
                w.kick_button[w.notebook.index(w.notebook.select())].configure(text='Kick')
                if name not in w.managers_list[w.notebook.index(w.notebook.select())].get('0', 'end'):
                    w.kick_button[w.notebook.index(w.notebook.select())].config(state='disable')
                    w.mute_button[w.notebook.index(w.notebook.select())].config(state='disable')
                    w.appoint_button[w.notebook.index(w.notebook.select())].config(state='disable')
                else:
                    w.mute_button[w.notebook.index(w.notebook.select())].config(state='normal')
                    w.appoint_button[w.notebook.index(w.notebook.select())].config(state='normal')

            if selected in muted[w.notebook.tab(w.notebook.index(w.notebook.select()), option="text")]:
                w.mute_button[w.notebook.index(w.notebook.select())].configure(text='Unmute')
            else:
                w.mute_button[w.notebook.index(w.notebook.select())].configure(text='Mute')

            if selected in w.managers_list[w.notebook.index(w.notebook.select())].get('0', 'end'):
                w.appoint_button[w.notebook.index(w.notebook.select())].config(state='disable')
                w.mute_button[w.notebook.index(w.notebook.select())].config(state='disable')

    except Exception:
        error()


def recap(room='globally'):
    try:
        global my_socket, name, w, users
        my_socket.send("Name: " + name + "\r\nFunc: view-participants\r\nTo: " + room + "\r\n\r\nNone\r\n\r\n\r\n")
    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()


def get_managers(room):
    try:
        global my_socket, name, w, users
        my_socket.send("Name: " + name + "\r\nFunc: view-managers\r\nTo: " + room + "\r\n\r\nNone\r\n\r\n\r\n")
    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()


def un_mute():
    try:
        global w, my_socket, name, muted
        selected = w.members_list[w.notebook.index(w.notebook.select())].get(w.members_list[w.notebook.index(w.notebook.select())].curselection())
        if selected not in muted[w.notebook.tab(w.notebook.index(w.notebook.select()), option="text")]:
            my_socket.send("Name: " + name + "\r\nFunc: mute\r\nTo: " + w.notebook.tab(w.notebook.index(w.notebook.select()), option="text") + "\r\n\r\n" + selected + "\r\n\r\n\r\n")
            w.mute_button[w.notebook.index(w.notebook.select())].configure(text='Unmute')
        else:
            my_socket.send("Name: " + name + "\r\nFunc: unmute\r\nTo: " + w.notebook.tab(w.notebook.index(w.notebook.select()), option="text") + "\r\n\r\n" + selected + "\r\n\r\n\r\n")
            w.mute_button[w.notebook.index(w.notebook.select())].configure(text='Mute')
    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()
    sys.stdout.flush()


def new_room():
    try:
        global w, users, room_name
        #create new tab for the room
        room_name, room_users = new_room_gui.vp_start_gui(users, name)
        if room_name and room_users:
            my_socket.send("Name: " + name + "\r\nFunc: create\r\nTo: " + room_name + "\r\n\r\n" + room_users + "\r\n\r\n\r\n")
    except socket.error:
        tkMessageBox.showerror("Error!", "The server is down!\nThe client is about to self terminate.")
        exit()
    except Exception:
        error()
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root, name, my_socket
    w = gui
    top_level = top
    root = top
    name = main.name
    my_socket = main.socket



def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    main.vp_start_gui(name, my_socket)
