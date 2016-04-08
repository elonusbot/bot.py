#! /usr/bin/env python

import socket
from time import sleep
import json
import os
import sys
import inspect

acceptedArgs = ["sender", "target", "message", "command", "argument", "server"]  #List over aguments that functions are allowed to use. See comments in the data class for information on what each of them are

class data(object): #A class for the raw data from IRC servers
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def getSender(self):
        return self.raw_data.split("!", 1)[0].strip(":")  #Returns the nick of the person who sent the IRC message

    def getTarget(self):
        return self.raw_data.split()[2]  #Returns who the message was sent to, either a channel or a private message to the bot

    def isPrivate(self):
        return self.getTarget(self)[0] != "#"  #Returns True if the message was sent in a private message to the bot, otherwise returns False

    def getMessage(self):
        return self.raw_data.split(None, 3)[3][1:]  #Returns message that was sent, the text otherwise displayed in a normal IRC client

    def getHostname():
        return self.raw_data.split("!", 1)[1].split(None, 1)[0].split("@", 1)[1]    #Returns the hostname of the person who sent the message

    def isCommand(self):
        return self.getMessage(self)[0] == "."  #Returns True if the message starts with "." and is therefore a command to the bot. Returns False otherwise

    def getCommand(self):
        return self.getMessage(self).split(None, 1)[0]  #Returns the command passed to the bot. For example .math

    def isArgument(self):  #Checks if the message provided an argument to the command. If it did it returns True otherwise it returns False
        try:
            self.getMEssage(self).split(None, 1)[1]
        except IndexError:
            return False
        else:
            return True

    def getArgument(self):
        try:
            return self.getMessage(self).split(None, 1)[1]   #Returns the argument that was sent in addition to the command if any. For example the math expression after .math
        except IndexError:
            return "Command requires an argument"


    def getServer(self):  #Is used for ping. Returns the name of the server who send the ping
        return self.raw_data.split(":", 1)[1]

def functionInspect(function):
    arguments = signature(function)  #Creates a tuple with the names of the arguments the function accepts

    for arg in arguments:
        if arg not in acceptedArgs or "*" in arg:  #Checks if the argument names in the function are ones in the accepted list or checks if the argument is not a normal one
            return "Function uses invalid arguments"

    argsToPass = {}  #Dictionary of the argument and value pairs to pass to the function

    if "sender" in arguments:  #Provides the function the information it asks for
        argsToPass["sender"] = data.getSender()  

    if "target" in arguments:
        argsToPass["target"] = data.getTarget()

    if "message" in arguments:
        argsToPass["message"] = data.getMessage()

    if "command" in arguments:
        argsToPass["command"] = data.getCommand()

    if "argument" in arguments:
        argsToPass["argument"] = data.getArgument()

    if "server" in argument:
        argsToPass["server"] = data.getServer()

    return function(**argsToPass)  #Calls the function with the argument and value pairs earlier defined

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

def save_load_config():
    global config
    if save_config(config, 'config.json') == False:
        send(data, "Warning! Config was not saved, so next time the bot starts the action will not be remembered")
    temp = load_config('config.json')
    if temp == False:
        send(data, "Warning! Config file could not be loaded, the old config will still be used")
    else:
        config = temp


