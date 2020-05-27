import sqlite3
from sqlite3 import Error
import os.path
from datetime import datetime

#This class is responsible for managing the database and the history

class HistoryStore:
    _fileName = "history.db"
    _createTable = """CREATE TABLE IF NOT EXISTS ChannelHistory (
                        Channel text NOT NULL,
                        InsertDate text NOT NULL,
                        Message text NOT NULL,
                        User text NOT NULL
                    );"""
    _insertMessage = """INSERT INTO ChannelHistory(Channel,InsertDate,Message, User)
                        VALUES(?,?,?,?)"""
    _readHistory = """SELECT Message, User 
                        FROM ChannelHistory
                        WHERE Channel=?
                        ORDER BY InsertDate ASC"""
    _readLastMessage = """SELECT Channel, User, InsertDate 
                        FROM ChannelHistory
                        WHERE Channel=?
                        AND User=?
                        ORDER BY InsertDate DESC
                        LIMIT 1"""
    _deleteMessage = """DELETE FROM ChannelHistory 
                        WHERE Channel=? 
                        AND User=? 
                        AND InsertDate=?"""
    _deleteChannel = """DELETE FROM ChannelHistory
                        WHERE Channel=?"""

    def __init__(self):
        # Check if the DB already exist
        newDB = not os.path.exists(self._fileName)
        # create a database connection to a SQLite database
        try:

            print(sqlite3.version)
            # If a new DB create the DB tables
            if newDB == True:
                connection = self.__connect()
                connection.cursor().execute(self._createTable)
                connection.commit()
                connection.close()
        except Error as e:
            print(e)
#Connects to the database
    def __connect(self):
        return sqlite3.connect(self._fileName)
#Sends the history of the current channel
    def readChannelHistory(self, channel):
        connection = self.__connect()
        data = connection.cursor().execute(self._readHistory, (channel,)).fetchall()
        connection.close()
        return data
#Stores the messages in the database
    def storeChannelMessage(self, channel, message, user):
        connection = self.__connect()
        connection.cursor().execute(self._insertMessage, (channel, datetime.now(), message, user))
        connection.commit()
        connection.close()
#Deletes the last message sent by the user
    def deleteLastMessage(self, channel, user):
        connection = self.__connect()
#Get last mesasge for the user
        data = connection.cursor().execute(self._readLastMessage, (channel, user)).fetchall()
#User has messages
        if len(data) != 0:
#Deletes last message for the user
            (channel, user, date) = data[0]
            connection.cursor().execute(self._deleteMessage, (channel, user, date))
        connection.commit()
        connection.close()

    def deleteChannelHistory(self, channel):
        connection = self.__connect()
        connection.cursor().execute(self._deleteChannel, (channel,)).fetchall()
        connection.commit()
        connection.close()
