from chatcommunication import ChatCommunication
import time
import random
import os

#This file creates a random user to test the communication channel by sending random mesages, deleting messages and switching channels.

def chatCommunicationCallback(line):
    print(line)
#sends the message
def sendMsg(msg):
    chatcommunication.send(msg)
    time.sleep(2)
#gets a randomized message
def getMessage():
    messages = ["Without deep reflection one knows from daily life that one exists for other people.",
            "The secret of your success is determined by your daily agenda.",
            "Creation is a miracle of daily recurrence. 'A miracle a minute' would not be a bad slogan for God.",
            "Let everyone try and find that as a result of daily prayer he adds something new to his life, something with which nothing can be compared.",
            "All major religious traditions carry basically the same message, that is love, compassion and forgiveness the important thing is they should be part of our daily lives.",
            "Peace is a daily, a weekly, a monthly process, gradually changing opinions, slowly eroding old barriers, quietly building new structures.",
            "Of our relation to all creation we can never know anything whatsoever. All is immensity and chaos. But, since all this knowledge of our limitations cannot possibly be of any value to us, it is better to ignore it in our daily conduct of life.",
            "The wide world is all about you: you can fence yourselves in, but you cannot forever fence it out.",
            "Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen.",
            "There is nothing noble in being superior to your fellow men. True nobility lies in being superior to your former self."
    ]
    return messages[random.randint(1, 10) - 1]
def userAction():
    sendMsg(getMessage())
    sendMsg(getMessage())
    sendMsg(getMessage())
    sendMsg("{delete}")

chatcommunication = ChatCommunication(chatCommunicationCallback)
random.seed()
num = str(random.randint(1, 10))
name = "User" + num
channel = "channel" + num
sendMsg(name)
sendMsg(channel)
userAction()
print("Deleted Last Message from History")
channel = "channel" + str(random.randint(1, 10))
sendMsg("{channel} " + channel)
userAction()
print("Deleted Last Message from History")
sendMsg("{quit}")
print("Press any key to Quit")
input()