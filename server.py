#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

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
            data = "".join([user, ":", str(self.dicc_Data[user])])
            json.dump(data, data_file)

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        for line in self.rfile:
            DATA = line.decode('utf-8').split()
            if DATA:
                if int(DATA[4]) == 0:
                    try:
                        del self.dicc_Data[DATA[2]]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    except KeyError:
                        self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
                elif int(DATA[4]) >= 0:
                    DATA_LIST= " ".join(DATA[0:3] + DATA[5:])
                    print( DATA_LIST,"\r\n\r\n")
                    self.dicc_Data[DATA[2]] = self.client_address[0], DATA[4]
                    self.register2json(DATA[2])
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                #IMPRIME MI DICCIONARIO
                print(self.dicc_Data)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
