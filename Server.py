#---------------Imports-------------------
import socket
from select import select
import datetime
import thread
import traceback
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection
import time


#---------------Globals-------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()
messages_to_send = []
open_client_sockets = []
rooms = {'globally':
        {
         'users': {},
         'admins': {},
         'muted': {}
         }
         }  # rooms[room_name] = {participants: {client: socket}, admins: {client: socket}, muted: {client: socket}}


#---------------Functions----------------
def send_waiting_messages(wlist):
    """
    Sends waiting messages that are queued to be sent, but only if the client is writable
    :param wlist: a list of all the writable client sockets
    :return: None
    """
    global messages_to_send
    for message in messages_to_send:
        client_socket, data = message
        if client_socket in wlist:
            client_socket.send(data + '\r\n\r\n\r\n')
            messages_to_send.remove(message)


def error():
    print '\33[31m' + traceback.format_exc() + '\033[0m'


def broadcast_message_append(message, exclude, room='globally'):
    """
    Appends a message to all of the connected client except the excluded list
    :param message: The messages to broadcast
    :param exclude: A list of clients which should be excluded out of this broadcast
    :return: None
    """
    global messages_to_send, open_client_sockets, rooms
    for user in rooms[room]['users'].values():
        if user not in exclude:
            messages_to_send.append((user, message))


def get_parameter(request, param):
    """
    extracts out a single parameter from the client request. can either accept a specific parameter as str or a list of parameters.
    :param request: the client request
    :param param: the needed parameter/s
    :return: the needed parameter/s value. list of values if param is a list, and str is param is str
             note - When using param as a list the list values which the function returns
             is organized at the same order the parameters where organized in side of param and at the correct way for the protocol.
    """
    if param == "Params":
        return request.split("\r\n\r\n")[1]
    if isinstance(param, type([])):
        if len(param) <= 4:
            return [request.split("\r\n\r\n")[1] if x == "Param" else request.split(x + ": ")[1].split("\r\n")[0] for x in param]
        if len(param) == 5 and "Time_Get" in param:
            return [request.split(x + ": ")[1].split("\r\n")[0] for x in param[0:3]] + [current_time()] + [get_parameter(request, "Params")]
    if isinstance(param, type("")):
        return request.split(param + ": ")[1].split("\r\n")[0]


def current_time():
    """
    Get current local time in a hh:mm format
    :return: current time
    """
    return ':'.join(str(datetime.datetime.now().time()).split(':')[0:2])


def craft_respond(name=None, func=None, to=None, time=None, param=None, params_dump=None):
    """
    Crafts a respond once all the parameters are known, can either accept one of the parameters stated as arguments or a list of them IN THE CORRECT ORDER
    :param name: The user which preformed the function
    :param func: what have he done
    :param to: who was his victim
    :param time: when?
    :param param: function parameters
    :param params_dump: all the arguments of the functuin but in a list instead, it becomes very useful for preforming long one liners
    :return: A proper respond the my chat protocol works
    """
    if params_dump:
        return "Name: %s\r\nFunc: %s\r\nTo: %s\r\nTime: %s\r\n\r\n%s" % tuple(["" if not x else x for x in params_dump])
    if not time:
        time = current_time()
    return "Name: %s\r\nFunc: %s\r\nTo: %s\r\nTime: %s\r\n\r\n%s" % (name, func, to, time, param)


def handle_client_request(client_socket, request):
    """
    Appends a proper respond to the clients request
    :param client_socket: the user's socket
    :param request: what was received from the user
    :return: none
    """
    global rooms, messages_to_send, open_client_sockets
    function, destination = get_parameter(request, ["Func", "To"])
    if get_parameter(request, "Name") not in rooms['globally']['users']:
        #If user is not recognised, append it to the users dictionary
        rooms['globally']['users'][get_parameter(request, "Name")] = client_socket
        broadcast_message_append(craft_respond(get_parameter(request, "Name"), "joined", "globally", current_time(), "None"), [client_socket])
        messages_to_send.append((client_socket, "Name: " + get_parameter(request, "Name") + "\r\nFunc: None\r\nTo: None\r\nTime: None\r\n\r\nOK"))
    elif rooms['globally']['users'][get_parameter(request, "Name")] != client_socket:
            if function == 'None':
                messages_to_send.append((client_socket, "Name: " + get_parameter(request, "Name") + "\r\nFunc: None\r\nTo: None\r\nTime: None\r\n\r\nTAKEN"))
            else:
                exit_func("Name: " + get_parameter(request, "Name") + "\r\nFunc: exit\r\nTo: globally\r\n\r\n", 'globally', None)
                broadcast_message_append(craft_respond(get_parameter(request, "Name"), "joined", "globally", current_time(), "None"), [client_socket])
                messages_to_send.append((client_socket, "Name: " + get_parameter(request, "Name") + "\r\nFunc: None\r\nTo: None\r\nTime: None\r\n\r\nOK"))

    elif destination != 'globally' and destination in rooms and get_parameter(request, "Name") not in rooms[destination]['users']:
        rooms[destination]['users'][get_parameter(request, "Name")] = client_socket
        broadcast_message_append(craft_respond(get_parameter(request, "Name"), "joined", destination, current_time(), "None"), [client_socket], destination)

    elif function == "message":
        message_func(request, destination, client_socket)

    elif function == "exit":
        exit_func(request, destination, client_socket)

    elif function == 'mute':
        mute_func(request, destination, False)

    elif function == 'unmute':
        mute_func(request, destination, True)

    elif function == 'add':
        add_func(request, destination)

    elif function == 'kick':
        kick_func(request, destination)

    elif function == 'view-managers':
        messages_to_send.append((client_socket, craft_respond(None, 'view-managers', destination, current_time(), ", ".join(rooms[destination]['admins'].keys()))))

    elif function == 'view-participants':
        messages_to_send.append((client_socket, craft_respond(params_dump=[None, 'view-participants', destination, current_time(), ", ".join(rooms[destination]['users'].keys())])))

    elif function == 'create':
        create_group(request, destination, client_socket)

    elif function == 'appoint-manager':
        appoint_manager(request, destination)


def message_func(request, destination, client_socket):
    global rooms, messages_to_send
    if not rooms[destination]['muted'] or get_parameter(request, "Name") not in rooms[destination]['muted']:
        if destination == "globally":
            broadcast_message_append(craft_respond(params_dump=get_parameter(request, "Name, Func, To, Time_Get, Params".split(", "))), [client_socket])
        elif destination in rooms['globally']['users']:
            messages_to_send.append((rooms['globally']['users'][destination], craft_respond(params_dump=get_parameter(request, "Name, Func, To, Time_Get, Params".split(", ")))))
        elif destination in rooms:
            broadcast_message_append(craft_respond(params_dump=get_parameter(request, "Name, Func, To, Time_Get, Params".split(", "))), [client_socket], destination)

    else:
        messages_to_send.append((rooms['globally']['users'][get_parameter(request, "Name")], craft_respond(params_dump=[get_parameter(request, "Name"), "muted", get_parameter(request, "To"), None, "You are muted in this room."])))


def exit_func(request, destination, client_socket):
    if destination == "globally":
        for room in rooms:
            if room != 'globally' and get_parameter(request, 'Name') in rooms[room]['users']:
                exit_func(request.replace('globally', room), room, client_socket)
        if client_socket:
            try:
                open_client_sockets.remove(client_socket)
            except Exception:
                pass
        rooms['globally']['users'].pop(get_parameter(request, 'Name'), None)
        print "Connection with client closed."
        broadcast_message_append(craft_respond(params_dump=get_parameter(request, "Name, Func, To, Time_Get, Params".split(", "))), [])

    elif destination in rooms:
        rooms[destination]['users'].pop(get_parameter(request, 'Name'), None)
        rooms[destination]['admins'].pop(get_parameter(request, 'Name'), None)
        rooms[destination]['muted'].pop(get_parameter(request, 'Name'), None)
        broadcast_message_append(craft_respond(params_dump=get_parameter(request, "Name, Func, To, Time_Get, Params".split(", "))), [], destination)


def mute_func(request, destination, unmute):
    if unmute:
        if destination in rooms:
            rooms[destination]['muted'].pop(get_parameter(request, 'Params'), None)
            broadcast_message_append(craft_respond(get_parameter(request, 'Name'), "unmuted", destination, None, get_parameter(request, 'Params')), [], destination)
    else:
        if destination in rooms:
            rooms[destination]['muted'][get_parameter(request, 'Params')] = rooms[destination]['users'][get_parameter(request, 'Params')]
            broadcast_message_append(craft_respond(get_parameter(request, 'Name'), "muted", destination, None, get_parameter(request, 'Params')), [], destination)


def add_func(request, destination):
    if destination in rooms:
        rooms[destination]['users'][get_parameter(request, 'Params')] = rooms['globally']['users'][get_parameter(request, 'Params')]
        broadcast_message_append(craft_respond(get_parameter(request, "Params"), "joined", destination, current_time(), get_parameter(request, "Name")), [], destination)


def kick_func(request, destination):
    if destination in rooms:
        broadcast_message_append(craft_respond(get_parameter(request, "Name"), "kick", destination, current_time(), get_parameter(request, "Params")), [], destination)
        rooms[destination]['users'].pop(get_parameter(request, 'Params'), None)
        rooms[destination]['admins'].pop(get_parameter(request, 'Params'), None)
        rooms[destination]['muted'].pop(get_parameter(request, 'Params'), None)

def create_group(request, destination, client_socket):
    try:
        if destination not in rooms:
            rooms[destination] = {'users': {x: rooms['globally']['users'][x] for x in get_parameter(request, "Params").split(", ") + [get_parameter(request, 'Name')]}, 'admins': {get_parameter(request, 'Name'): rooms['globally']['users'][get_parameter(request, 'Name')]},  'muted': {}}
            messages_to_send.append((client_socket, "Name: " + get_parameter(request, "Name") + "\r\nFunc: create\r\nTo: " + destination + "\r\nTime: None\r\n\r\nOK"))
            broadcast_message_append(craft_respond("You", "joined", destination, current_time(), get_parameter(request, "Name")), [client_socket], destination)
        else:
            messages_to_send.append((client_socket, "Name: " + get_parameter(request, "Name") + "\r\nFunc: create\r\nTo: " + destination + "\r\nTime: None\r\n\r\nTAKEN"))
    except Exception:
        error()


def appoint_manager(request, destination):
    if destination in rooms:
        rooms[destination]['admins'][get_parameter(request, 'Params')] = rooms['globally']['users'][get_parameter(request, 'Params')]
        broadcast_message_append(craft_respond(get_parameter(request, "Name"), "appoint-manager", destination, current_time(), get_parameter(request, "Params")), [], destination)


def single_user(client_socket, server_socket):
    """
    Messages a single client
    :param client_socket: the user's socket
    :return: none
    """
    if client_socket is server_socket:
                new_socket, address = server_socket.accept()
                open_client_sockets.append(new_socket)
                print "Connected with client."
    else:
        try:
            data = client_socket.recv(1024)
            while data and data[::-1][:6] != '\r\n\r\n\r\n'[::-1]:
                data += client_socket.recv(1024)
                for x in data.split('\r\n\r\n\r\n'):
                    if len(data.split('\r\n\r\n\r\n')) == 1:
                        continue
                    handle_client_request(client_socket, x)
            if data:
                handle_client_request(client_socket, data.replace('\r\n\r\n\r\n', ''))
            else:
                open_client_sockets.remove(client_socket)
                try:
                    exit_func("Name: " + [x for x in rooms['globally']['users'].keys() if rooms['globally']['users'][x] == client_socket][0] + "\r\nFunc: exit\r\nTo: globally\r\n\r\n", 'globally', client_socket)
                except Exception:
                    pass
                print "Connection with client closed."
        except socket.error:
            open_client_sockets.remove(client_socket)


def manage_users(server_socket):
    """
    Manages all the server's clients
    :param server_socket: the  server socket
    :return: none
    """
    while True:

        for room in rooms:
            if room != 'globally' and not rooms[room]['users']:
                rooms.pop(room, None)
                break

        rlist, wlist, xlist = select([server_socket] + open_client_sockets, open_client_sockets, open_client_sockets)
        for current_socket in rlist:
            single_user(current_socket, server_socket)
        for current_socket in xlist:
            open_client_sockets.remove(current_socket)
            exit_func("Name: " + [x for x in rooms['globally']['users'].keys() if rooms['globally']['users'][x] == current_socket][0] + "\r\nFunc: exit\r\nTo: globally\r\n\r\n", 'globally', current_socket)
        send_waiting_messages(wlist)


def priinter(debug):
    if debug:
        while True:
            print rooms
            time.sleep(4)


#---------------Main--------------
def main():
    """
    Multiclient server
    """
    print "Running..."
    thread.start_new_thread(ServerDitection.server_emitter, ())
    thread.start_new_thread(priinter, (False,))
    server_socket = socket.socket()
    server_socket.bind((IP, 23))
    server_socket.listen(5)
    manage_users(server_socket)


if __name__ == '__main__':
    main()
