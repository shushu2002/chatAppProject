from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#this class is responsible for remote communication using sockets

class ChatCommunication:
    def __init__(self, callback, host = "127.0.0.1"):
        self.callback = callback
#setting the socket
        # HOST = input('Enter host: ')
        # PORT = input('Enter port: ')
        PORT = 5000
        HOST = host
        if not PORT:
            PORT = 33000
        else:
            PORT = int(PORT)

        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        receive_thread = Thread(target=self.__receive)
        receive_thread.start()
#recievs the messages
    def __receive(self):
        """Handles receiving of messages."""
        BUFSIZ = 1024
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                lines = msg.split("\n")
                for line in lines:
                    self.callback(line)
            except OSError:  # Possibly client has left the chat.
                break
#sends the messages
    def send(self, msg):  # event is passed by binders.
        """Handles sending of messages."""
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            return False
        return True
