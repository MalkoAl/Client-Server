#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.log import error
import sqlite3
import pathlib
import socket
#from typing_extensions import Self

class ServerApp:

    IP_ADDRESS = 'localhost'
    IP_PORT = 58080
    
    def __init__(self):

        self.index = 0

        # connect to DB
        self.connect_db()

        # there init server
        server_socket = socket.socket()
        server_socket.bind((self.IP_ADDRESS, self.IP_PORT))
        print('Server on ' + self.IP_ADDRESS + ':' + str(self.IP_PORT))
        server_socket.listen(1)
        self.conn, self.address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(self.address))

    def connect_db(self):
        db = pathlib.Path.cwd() / 'test.db'

        try:
            self.connection = sqlite3.connect(db)
        except sqlite3.Error as error:
            print('Error with Database!')
        
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Test (id int PRIMARY KEY, name varchar(24))''')

        if(self.cursor.lastrowid == 0):
            self.index = 0
            print('last ID = 0')
        else:
            print('last ID', self.cursor.lastrowid)
            self.index = self.cursor.lastrowid + 1
    
    def reconnect(self):
        #try reconnect
        try:
            server_socket = socket.socket()
            server_socket.bind((self.IP_ADDRESS, self.IP_PORT))
            print('Server reconnect ' + self.IP_ADDRESS + ':' + str(self.IP_PORT))
            server_socket.listen(1)
            self.conn, self.address = server_socket.accept() 
            print("Reconnection from: " + str(self.address))
            return True        
        except:
            print("Connection lose!!!")
            return False

    def run(self):
        # start event loop from server

        self.conn.send(b'start')

        while True:

            data = ''
            try:
                data = self.conn.recv(1024).decode()
            except Exception as e:
                print(e)
                # There is disconnect - need restart and wait for reconnect...
                print('Connection closed from client... Exit')
                Reconn = self.reconnect()    
                if Reconn:
                    print("Connection recover... ")
                    self.run()
                else:
                    print("Can't connection ...")
                    break
                
            if not data:
                print('End Data?')
            else:
                ind = str(self.cursor.lastrowid)
                cmd = 'INSERT OR IGNORE INTO Test VALUES (' + ind + ',"' + data + '")'
                print(cmd)
                self.cursor.execute(cmd)
                self.index = self.index + 1
                self.cursor.execute("SELECT * FROM Test")
                print(self.cursor.fetchall())
                
                print("from connected user: " + str(data))
                self.connection.commit()
                self.conn.send(data.encode())  # send data to the client
        
        self.conn.close()
        self.connection.close()


if __name__ == '__main__':
    app = ServerApp()
    app.run()

