#! /usr/bin/env python

import socket
from time import sleep
import json
import os
import sys

def load_config(__file):
    __local_config = False
    try:
        with open(__file) as f:
            __local_config = json.load(f)
    except Exception as e:
        print (e)
    return __local_config

def save_config(__obj, __file):
    try:
        with open(__file, 'w') as f:
            json.dump(__obj, f, indent=2, sort_keys=True)
            # write a newline at end of file
            f.write('\n')
    except Exception as e:
        print (e)
        return False
    return True

def stop():
    global config
    if save_config(config, 'config.json') == False:
        print ("error saving config! any changes will not be saved!")
    quit()

def ping():
    global irc
    irc.send(( "PONG " + data.split() [ 1 ] + "\r\n" ).encode('utf-8'))

def argument():
    arg = ""
    for i in data.split(":")[2].split()[1:]:
        arg += i

    return(arg)


def send(data, message):
    """
    sends message to channel or user depending on where it is from
    """
    destination = data.split()[2]

    if destination[0] == "#":
        irc.send( ( "PRIVMSG " + destination + " :" + message + "\r\n").encode('utf-8') )

    else:
        irc.send( "PRIVMSG " + sender + " :" + message + "\r\n")


def hello():
    answer = "Hello " + sender + "!"
    send(data, answer)


def arithmetic():

    expression = argument()
    condition = "0123456789+-/*.() "
    newexpression = ""
    for i in expression:
        if i in condition:
            newexpression += str(i)
        else:
            send (data, "Error! Invalid input")
            return

    if ("**" in newexpression):
        answer = "You tried to use a power. Unfortunately I do not have that functionnality at the moment."
    if (len(newexpression) > 15):
        answer = "Your expression was too long. I only accept expressions up to 15 characters long."

    else:
        try:
            __eval_return = eval("1.0 * " + newexpression)
            answer = "The answer to " + expression + " is: " + str(__eval_return)
        except ZeroDivisionError:
            answer = "Error! You tried to divide by zero"
        except SyntaxError:
            answer = "Error! Invalid input"
        except Exception as e:
            __error = str(e)
            answer = "Error! " + __error

    send(data, answer)


def join_channel():
    global config
    message = data.split(":")[2]
    channel_name = message.split()[1]
    if channel_name in config['channels']:
        send(data, "I am already in " + channel_name)
    else:
        irc.send("JOIN " + channel_name + "\r\n")
        send(data, "I have joined " + channel_name)
        config['channels'].append(channel_name)

def update():
    os.system('git pull')

def part_channel():
    global config
    message = data.split(":")[2]
    channel_name = message.split()[1]
    if channel_name not in config['channels']:
        send(data, "I am not in " + channel_name)
    else:
        irc.send("PART " + channel_name + "\r\n")
        send(data, "I have left " + channel_name)
        config['channels'].remove(channel_name)

def add_admin(data):
    global config
    message = data.split(":")[2]
    add_name = message.split()[1]
    config['admins'].append(add_name)
    send(data, add_name + " has been added to the admin list")

def list_admins():
    global config
    adminList = ""
    for i in config['admins']:
        if len(adminList) == 0:
            adminList += i

        else:
            adminList += ", " + i

    send(data, "This is a list of the current admins: " + adminList)

def help_commands():
    command_list = ""
    for i in functions:
        command_list += " " + i

    send(data, "This is a list of the available commands:" + command_list)

def source():
    print("source called!")
    send( data, ("The source is available at https://github.com/elonusbot/bot.py .  Fork and improve!") )

functions = { ".math" : {"argument": True, "function": arithmetic, "require_admin" : False}
             , ".hello" : {"argument" : False, "function" : hello, "require_admin" : False}
             , ".join" : {"argument" : True, "function" : join_channel, "require_admin" : True}
             , ".part" : {"argument" : True, "function" : part_channel, "require_admin" : True}
             , ".addadmin" : {"argument" : True, "function" : add_admin, "require_admin" : True}
             , ".listadmins" : {"argument" : False, "function" : list_admins, "require_admin" : False}
             , ".help" : {"argument": False, "function": help_commands, "require_admin" : False}
             , ".stop" : {"argument": False, "function": stop, "require_admin": True}
             , ".update" : {"argument": False, "function": update, "require_admin": False}
             , ".source" : {"argument": False, "function": source, "require_admin": False}
             , ".update" : {"argument": False, "function": update, "require_admin": False}}

# TODO : use args library here
__args = sys.argv
if __args[0] == __file__:
    __args.pop(0)
if (len(__args)):
    if __args[0] == "blank_test":
        quit()

config = load_config('config.json')
if config == False:
    quit()

network = "irc.freenode.net"
port = 6667
irc = socket.socket (socket.AF_INET, socket.TCP_NODELAY)
irc.connect ( ( network, port ) )
data = irc.recv ( 4096 )


print(data)

irc.send (( "NICK ElonusBot2\r\n" ).encode('utf-8'))
irc.send (( "USER ElonusBot2 ElonusBot2 ElonusBot2 :Elonus testbot\r\n" ).encode('utf-8'))
sleep(2)
irc.send (( "PRIVMSG NickServ: identify elonusbot gutta4197\r\n" ).encode('utf-8'))

data = irc.recv(4096)

for i in config['channels']:
    irc.send (( "JOIN " + i + "\r\n" ).encode('utf-8'))
    irc.send (("PRIVMSG " + i + " :Hello, I am ElonusBot and I love pancakes!\r\n").encode('utf-8'))
    sleep(0.5)

sleep(1)

while True:
    data = irc.recv(4096).decode('utf-8').strip("\r\n");
    print(data)

    if data.find("PING") != -1:
        ping()
        continue

    elif data.find("PRIVMSG") != -1:
        message = data.split(":")[2:]
        if type(message) == list:
            new_message = ""
            for i in message:
                new_message += i
            message = new_message

        codeword = message.split()[0]
        codeword = codeword.lower()
        sender = data.split("!")[0].strip(":")

        if codeword in functions:

            if (sender not in config['admins']) and functions[codeword]["require_admin"]:
                send(data, codeword + " requires admin access")

            else:
                if functions[codeword]["argument"]:
                    try:
                        message.split()[1]

                    except IndexError:
                        send(data, codeword + " expects an argument")

                    else:
                        functions[codeword]["function"]()

                else:
                    functions[codeword]["function"]()
