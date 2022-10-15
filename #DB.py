#DB
from distutils.log import error
from operator import index
import sqlite3
import time
import pathlib
import socket

class ServerApp:

    IP_ADDRESS = 'localhost'
    IP_PORT = 8000


    def __init__(self):
        # there init server
        # connect to DB
        self.timeOld = time.time()
        self.timeNew = time.time() + 1
        self.index = 0
        self.connect_db()
   

    def connect_db(self):
        
        db = pathlib.Path.cwd() / 'test.db'
        try:
            self.connection = sqlite3.connect(db)
        except sqlite3.Error as error:
            print('Error with Database!')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''DROP TABLE IF EXISTS Test''')
        print(self.cursor.fetchone())
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Test (ID INT PRIMARY KEY , code VARCHAR(20) NOT NULL, 
        name varchar(24))''')
        
        lastIndex = self.cursor.execute("SELECT * FROM Test ORDER BY id DESC LIMIT 1")
        print(lastIndex.lastrowid)

        self.connection.commit()
              
        if(self.cursor.lastrowid == 0):
            self.index = 0
            print('last ID = 0')
        else:
            print('last ID', self.cursor.lastrowid)
            self.index = self.cursor.lastrowid + 1

    def run(self):
        while self.index < 5:
            data = 'start + ' + str(self.index)
            ind = str(self.index)
            cmd = 'INSERT OR REPLACE INTO Test(ID,code,name) VALUES ( "'+ ind +'","'+ ind +'","' + data + '")'
            #index_query = 'CREATE INDEX code_index ON Test(code)'
            print(cmd)
            self.cursor.execute(cmd)
            print(self.cursor.lastrowid)
            #self.cursor.execute(index_query)
            self.connection.commit()
            
            self.index = self.index + 1
            #self.cursor.execute("CREATE INDEX last_index ON Test(id) ")
            self.cursor.execute("SELECT * FROM Test")
            print(self.cursor.fetchall())
            #if(data == 'start'):
            #   print('Begin..')
            #    data = b''
            #else:
            #    pass
                #print('Received from server: ' + str(data))  # show in terminal

            self.timeOld = time.time()

            if(self.timeOld > self.timeNew):
                print('Tick..')
                self.timeOld = time.time()
                self.timeNew = time.time() + 1

if __name__ == '__main__':
    app = ServerApp()
    app.run()

