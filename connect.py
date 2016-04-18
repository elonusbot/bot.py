from time import sleep
import socket

network = "chat.freenode.net"
port = 6697
nick = "ElonusBot"
description = nick
nickServUsername = "elonusbot"
nickServPass = "gutta4197"

def connect(ircNetwork, ircPort, nick, nickServUsername, nickServPass):
    irc = socket.socket ( socket.AF_INET, socket.TCP_NODELAY )
    irc.connect( ( network, port) )
    data = data(irc.recv (4096) )
    print(data.getRawData())
    irc.send( ( "NICK " + nick + "\r\n").encode('utf-8') )
    irc.send( ( "USER " + nick + " " + nick + " " + nick + " :" + description + "\r\n").encode('utf-8') )
    sleep(2)
    irc.send( ( "PRIVMSG NickServ: identify " + nickServUsername + ' ' + nickServPass + '\r\n').encode('utf-8') )
    data = data(irc.recv (4096) )
