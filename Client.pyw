#-----------------------Imports-----------------------
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection
sys.path.insert(0, os.getcwd() + '/gui')
import login
import main
import main_support
import tkMessageBox
import traceback
import socket


#-----------------------Globals-----------------------
IP = ServerDitection.server_scout().split("Here Be Server: ")[1]
my_socket = socket.socket()
my_socket.connect((IP, 23))
name = login.vp_start_gui(my_socket)
if not name:
    my_socket.close()
    exit()
close = False


#----------------------Functions----------------------
def error():
    print '\33[31m' + traceback.format_exc() + '\033[0m'


#-------------------------Main-------------------------
def run():
    try:
        global my_socket, name
        print name
        main.vp_start_gui(name, my_socket)
        my_socket.send("Name: " + name + "\r\nFunc: exit\r\nTo: globally\r\n\r\nNone\r\n\r\n\r\n")
    except Exception:
        error()
    finally:
        my_socket.close()


if __name__ == '__main__':
    run()
