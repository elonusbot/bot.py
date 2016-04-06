#! /usr/bin/env python

import socket
from time import sleep
import json
import os
import sys
import inspect

acceptedArgs = ["sender", "target", "message", "command", "argument"]  #List over aguments that functions are allowed to use

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
        return self.raw_data.split(":", 2)[2]  #Returns message that was sent, the text otherwise displayed in a normal IRC client

    def getCommand(self):
        return self.getMessage(self).split(None, 1)[0]  #Returns the command passed to the bot. For example .math

    def getArgument(self):
        return self.getMessage(self).split(None, 1)[1]   #Returns the argument that was sent in addition to the command if any. For example the math expression after .math
    

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

    return function(**argsToPass)  #Calls the function with the argument and value pairs earlier defined


    
