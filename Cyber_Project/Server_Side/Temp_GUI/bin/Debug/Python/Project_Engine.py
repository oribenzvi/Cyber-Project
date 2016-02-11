

## Python Engine

import socket
from threading import Thread
import threading
import sys
import time
import struct
import os
import sqlite3
from Connection_Module import *
from DB_Managment import *



def Socket_Server():

    Adress = ("0.0.0.0",8086)
    Server_Socket = socket.socket()
    Server_Socket.bind(Adress)
    Server_Socket.listen(15)

    while True:
        print 'waiting for client connection...'
        (Client_Socket, Client_Adress) = Server_Socket.accept()
        print "Connected From: " + str(Client_Adress[0])

        DB_Obj = DB_Managment_Class()
        Bool_Result = DB_Obj.If_Client_Already_Exists(Client_Adress[0])

        ##Bool_Result = If_Client_Already_Exists(str(Client_Adress[0]))

        if Bool_Result == True:
            DB_Obj.Clients_DataBase_Add(str(Client_Adress[0]))

        DB_Obj.Current_ID()

        t1 = Thread(target=Client_Handler, args=(Client_Socket,Client_Adress,))
        t1.start()
        time.sleep(2)


def Client_Handler( Client_Socket, Client_Adress):
    print "Inside Handler"

    Local_Obj_Socket = Connecting_Using_Socket()
    Data_From_Client = Local_Obj_Socket.Socket_Recieve(Client_Socket)

    Local_Obj_Pipe = Connecting_Using_Pipe()
    print Data_From_Client

    if "KILL PROCESS USING CAMERA" in Data_From_Client:
        Pipe_Client_To_Server = Thread(target=Local_Obj_Pipe.Pipe_Client_To_Server(Data_From_Client,))
        Pipe_Client_To_Server.start()

        Pipe_Server_To_Client = Thread(target=Local_Obj_Pipe.Pipe_Server_To_Client(), args=())
        Pipe_Server_To_Client.start()


    Local_Obj_Socket.Socket_Send(Client_Socket,Data_To_Send="Hello From Server!")



if __name__=='__main__':
    global Counter

    t = Thread(target = Socket_Server())
    t.start()

    ####################################################################

    ##Obj2 = Connecting_Using_Socket()









        
