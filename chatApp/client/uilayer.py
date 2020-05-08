import tkinter

#This class is responsible for handling the user interface.

class UILayer:
        def __init__(self, callback):
            self.callback = callback
            self.first_message = True
            self.join_channel = False
            self.name = ""
            self.channel = ""
            self.top = tkinter.Tk()
            self.START_TITLE = "Chatter"
            self.top.title(self.START_TITLE)
            messages_frame = tkinter.Frame(self.top)
            self.my_msg = tkinter.StringVar()  # For the messages to be sent.
            self.my_msg.set("")
            scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
            # Following will contain the messages.
            self.msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
            self.msg_list.pack()
            self.msg_list.insert(tkinter.END, "Welcome! Please type your name and press enter!")
            messages_frame.pack()

            entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
            entry_field.bind("<Return>", self.__send)
            entry_field.pack()
            send_button = tkinter.Button(self.top, text="Send", command=self.__send)
            send_button.pack()
            self.top.protocol("WM_DELETE_WINDOW", self.__on_closing)

# Starts GUI execution.
        def start(self):
            tkinter.mainloop()
#sends the messages
        def __send(self, event=None):  # event is passed by binders.
            """Handles sending of messages."""
            msg = self.my_msg.get()
            # Get name in first message.
            if self.first_message == True:
                self.name = msg
                self.top.title(self.START_TITLE + ": " + self.name)
                self.first_message = False
            # Get channel in second message.
            elif self.join_channel == False:
                self.channel = msg
                self.__setChannel()
                self.join_channel = True
#checks if client wants to switch channel
            elif msg.startswith("{channel}"):
                tmp = msg.split(" ")
                if len(tmp) != 2:
                    self.my_msg.set("Invalid input. Please insert {channel} NewChannelName")
                    return
                else:
                    self.channel = tmp[1]
                    self.__setChannel()
            if self.callback(msg) == False:
                self.top.quit()
            self.my_msg.set("")  # Clears input field.
#If quit socket, closes the client
        def __on_closing(self, event=None):
            self.__send("{quit}")
#sets the title according to the channel
        def __setChannel(self):
            self.top.title(self.START_TITLE + ": " + self.name + " -> " + self.channel)
#displays the message
        def setMessage(self, msg):
            self.msg_list.insert(tkinter.END, msg)