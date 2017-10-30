#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import time
import json
import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_Data = {}
    def register2json(self, user):
        with open("register.json", "w") as data_file:
            for user in self.dicc_Data:
                data = "".join([user, ":", str(self.dicc_Data[user])])
            json.dump(data, data_file)

    def json2registered(self):
        try:
            with open("register.json", "r") as data_file:
                json.load(self.dicc_Data, data_file)
        except (NameError, FileNotFoundError, AttributeError):
            pass

    def check_server(self):
        dicc_Temp = {}
        for user in self.dicc_Data:
            tiempo = self.dicc_Data[user][1].split()
            dicc_Temp[user] = tiempo[1]
        for user in dicc_Temp:
            if time.gmtime(float(dicc_Temp[user])) < time.gmtime(time.time()):
                self.register2json(user)
                del self.dicc_Data[user]

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        for line in self.rfile:
            DATA = line.decode('utf-8').split()
            if DATA:
                self.check_server()
                if int(DATA[4]) == 0:
                    try:
                        del self.dicc_Data[DATA[2]]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    except KeyError:
                        self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
                elif int(DATA[4]) >= 0:
                    DATA_LIST= " ".join(DATA[0:3] + DATA[5:])
                    tiempo_exp = float(DATA[4]) + time.time()
                    tiempo_exp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(tiempo_exp))
                    print( DATA_LIST,"\r\n\r\n")
                    self.dicc_Data[DATA[2]] = self.client_address[0],"Expires: " + tiempo_exp
                    self.register2json(self.dicc_Data)
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                #IMPRIME MI DICCIONARIO
                print(self.dicc_Data)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())))
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
