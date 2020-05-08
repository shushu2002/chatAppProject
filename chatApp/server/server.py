from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from chatmanager import ChatManager
from historystore import HistoryStore

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
#Receive client name
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    client.send(bytes("Please insert the Channel to join.", "utf8"))
#Receive channel to join
    channel = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Welcome to Channel %s." % channel, "utf8"))
# Add user to channel.
    _chatManager.addToChannel(channel, name, client)
#Send welcome message to the channel
    broadcast(name + " has joined the chat!", channel)
#Send history to client
    sendHistory(channel, client)
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if msg == "{quit}":
            quitUser(client, channel, name)
            break
        elif msg == "{delete}":
            deleteMessage(channel, name)
        elif msg.startswith("{channel}"):
            tmp = msg.split(" ")
            if len(tmp) != 2:
                client.send(bytes("Invalid input. Please insert {channel} NewChannelName", "utf8"))
            else:
#Send leave message
                broadcast(name + " has left the chat!", channel)
#change to the new channel
                changeChannel(channel, tmp[1], client, name)
                channel = tmp[1]
                broadcast(name + " has joined the chat!", channel)
#Load history
                sendHistory(channel, client)
        else:
            broadcast(msg, channel, name)
            _historyStore.storeChannelMessage(channel, msg, name)

#Broadcasts a message to all the users in the channel
def broadcast(msg, channel, prefix = ""):  # prefix is for name identification.
    """Broadcasts a message to all channel."""
    to_send = bytes(formatMessage(prefix, msg), "utf8")
    for sock in _chatManager.getChannel(channel).values():
        sock.send(to_send)

#If a user wants to quit, removes him from the channel
def quitUser(client, channel, name):
    try:
        client.send(bytes("{quit}", "utf8"))
        client.close()
    except:
        print(name + " left the chat")
    finally:
        _chatManager.removeFromChannel(channel, name)
        broadcast("%s has left the chat." % name, channel)

#Deletes the last message a user sent in the channel
def deleteMessage(channel, user):
    _historyStore.deleteLastMessage(channel, user)

#Changes the channel of a user
def changeChannel(oldChannel, newChannel, client, name):
    _chatManager.removeFromChannel(oldChannel, name)
    _chatManager.addToChannel(newChannel, name, client)

#Sends the history of the channel
def sendHistory(channel, client):
    # Send history to client
    data = _historyStore.readChannelHistory(channel)
    for (message, user) in data:
        client.send(bytes(formatMessage(user, message), "utf8"))

#Formats the message the way we want it
def formatMessage(name, msg):
    if name:
        return name + ": " + msg
    return msg

HOST = ''
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
_chatManager = ChatManager()
_historyStore = HistoryStore()
#_chatCommunication
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

