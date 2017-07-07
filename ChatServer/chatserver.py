#!/usr/bin/python

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

import commands

PORT = 30736
NAME = 'MTGWF'
ASCIIART = """
                ..:::::::::..
           ..:::::?Y8888888b::::..
        .:::::d8888P:::Y8888888b::::.
      .:::::d88888b:::::Y88P::Y888b:::.
    .::::::d8P:::::::::::88::::88888b:::.
   :::::::P:d:::::::::::d??ba:d8888888b:::
  :::::::::?::::::::::::::::::::::Y8888b:Y:
 ::::::::::::::::::::::::::::::::::Y8888b:Y:
.::::::::::::::::::::::::::::::::b::88888:8:.
:::::::::::::::::;;:::::::;;a:::::b::888888::
:::::::::::::::d8888baaaaa88::::::)P:888888::
:::::::::::::d8888888888888P::::::d:d88888P::
`:::::::::::d88888888888P::::::::d8888888P::'
 ::::::::::d88888888888P::::::d8888888P::;::
  ::::::::d888888888888::::d88888888P?:dP::
   :::::::888888888888888888888888888bdP::
    `:::::888888888888888888888888888P::'
      `::::Y888888888888888888888P::::'
        `::::Y8888888888888888P:::::'
           ``:::::Y8888888baaa;:''
                ``:::::::::''
"""

class ChatSession(async_chat):
    def __init__(self, server, sock, player):
        async_chat.__init__(self, sock)
        self.server = server
        self.player = player
        self.set_terminator(' end}')
        self.data = []

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data) + ' end}'
        line = line[line.find('{'):]
        self.data = []
        if not commands.handle(line, self):
            self.server.broadcast(line, self)

    def handle_close(self):
        async_chat.handle_close(self)
        self.server.disconnect(self)

class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(6)
        self.name = name
        self.sessions = []

    def disconnect(self, session):
        player = session.player
        self.broadcast('{announce ' + player + ' disconnected... end}\r\n', session)
        self.sessions.remove(session)

    def broadcast(self, line, sender):
        for session in self.sessions:
            if session is not sender:
                session.push(line)

    def handle_accept(self):
        conn, addr = self.accept()
        playerNum = str(len(self.sessions) + 1)
        newSession = ChatSession(self, conn, 'Player ' + playerNum)
        self.sessions.append(newSession)
        newSession.push(ASCIIART + '\r\n')
        newSession.push('{info Welcome to MTG With Friends. end}\r\n')
        newSession.push('{info You are now connected as: Player ' + playerNum + ' end}\r\n')
        self.broadcast('{announce Player ' + playerNum + ' connected! end}\r\n', newSession)

if __name__ == '__main__':
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
