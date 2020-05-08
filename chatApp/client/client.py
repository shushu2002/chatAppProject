from chatcommunication import ChatCommunication
from uilayer import UILayer
import sys

#the callback function of the ui. The callback is used to connect between the ui and chatcommunication.
def uiCallback(msg):
    global chatcommunication
    if chatcommunication:
        return chatcommunication.send(msg)

#the callback function of the chatcommunication. The callback is used to connect between the ui and chatcommunication.
def chatCommunicationCallback(line):
    global uilayer
    if uilayer:
        uilayer.setMessage(line)

chatcommunication = None
uilayer = None
if len(sys.argv) != 2 or sys.argv[1] != "-d":
    host = input("Enter Host ip: ")
    chatcommunication = ChatCommunication(chatCommunicationCallback, host)
else:
    chatcommunication = ChatCommunication(chatCommunicationCallback)
uilayer = UILayer(uiCallback)
uilayer.start()