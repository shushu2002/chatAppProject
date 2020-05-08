class ChatManager:
    _channels = {}
#channels -> channel -> name -> client
#Adds a member to a channel
    def addToChannel(self, channel, name, client):
#Create channel if does not exist
        if not self._channels.get(channel):
            self._channels[channel] = {}
#Join client to the channel
        if not self._channels[channel].get(name):
            self._channels[channel][name] = client
#Removes a member from a channel
    def removeFromChannel(self, channel, name):
        del self._channels[channel][name]
#Manage if the client was the last in the channel.
        if not self._channels[channel]:
            del self._channels[channel]
#Returns a channel
    def getChannel(self, channel):
        if self._channels.get(channel):
            return self._channels[channel]
        return []