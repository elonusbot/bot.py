#! /usr/bin/env python

import socket
from time import sleep
import json
import os
import sys
import inspect

acceptedArgs = ["sender", "target", "message", "command", "argument"]

class data(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def getSender(self):
        return self.raw_data.split("!", 1)[0].strip(":")

    def getTarget(self):
        return self.raw_data.split()[2]

    def isPrivate(self):
        return self.getTarget(self)[0] != "#"

    def getMessage(self):
        return self.raw_data.split(":", 2)[2]

    def getCommand(self):
        return self.getMessage(self).split(None, 1)[0]

    def getArgument(self):
        return self.getMessage(self).split(None, 1)[1]
    

def functionInspect(function):
    arguments = signature(function)

    for arg in arguments:
        if arg not in acceptedArgs or "*" in arg:
            return "Function uses invalid arguments"

    argsToPass = {}

    if "sender" in arguments:
        argsToPass["sender"] = data.getSender()

    if "target" in arguments:
        argsToPass["target"] = data.getTarget()

    if "message" in arguments:
        argsToPass["message"] = data.getMessage()

    if "command" in arguments:
        argsToPass["command"] = data.getCommand()

    if "argument" in arguments:
        argsToPass["argument"] = data.getArgument()

    return function(**argsToPass)


    
