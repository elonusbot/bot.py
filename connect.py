network = "chat.freenode.net"
port = 6697

def connect(ircNetwork, ircPort):
    irc = socket.socket ( socket.AF_INET, socket.TCP_NODELAY )
    irc.connect( ( network, port) )
    data = data(irc.recv (4096) )
    print(data.getRawData())
