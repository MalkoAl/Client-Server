#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import socket
import time

# there include SQL library
import sqlite3

class ClientApp:

    IP_ADDRESS = 'localhost'
    IP_PORT = 58080
        
    def __init__(self):
        # there init client
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((self.IP_ADDRESS, self.IP_PORT))
        print('Client on ' + self.IP_ADDRESS + ':' + str(self.IP_PORT))
        self.timeOld = time.time()
        self.timeNew = time.time() + 1
        self.index = 0

    def run(self):
        # start event loop from client
        data = self.client_socket.recv(1024).decode()  # receive response
        
        while True:

            if(data == 'start'):
                print('Begin..')
                data = b''

            self.timeOld = time.time()

            if(self.timeOld > self.timeNew):
                print('Tick..')
                self.timeOld = time.time()
                self.timeNew = time.time() + 1
                if self.sendSocket() == False:
                    # There is disconnect from server. May try ping or something..
                    break

    def sendSocket(self):
        adata = bytearray(b'Hello server ')
        adata.extend(str(self.index).encode())
        try:
            self.client_socket.send(adata)
        except Exception as e:
            print(e)
            # There is disconnect - need restart and wait for reconnect...
            print('Connection closed from server... Exit')
            return False
        self.index += 1
        print(self.index)
        return True


if __name__ == '__main__':
    app = ClientApp()
    app.run()

