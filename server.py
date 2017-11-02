#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import json
import socketserver
import sys
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_Data = {}

    def register2json(self):
        """
        Convierte mi biblioteca de datos a un archivo json
        """
        with open("registered.json", "w") as data_file:
            json.dump(self.dicc_Data, data_file)

    def json2registered(self):
        """
        Recoge los datos del archivo json (si existe) y los
        vuelca en mi diccioario de datos
        """
        try:
            with open("registered.json", "r") as data_file:
                self.dicc_Data = json.load(data_file)
        except (NameError, FileNotFoundError):
            pass

    def check_server(self):
        """
        Comprueba los usuarios caducados
        """
        dicc_Temp = {}
        Time_Format = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.gmtime(time.time()))
        if self.dicc_Data:
            for user in self.dicc_Data:
                tiempo = self.dicc_Data[user][1]
                dicc_Temp[user] = tiempo[9:]
            for user in dicc_Temp:
                if dicc_Temp[user] < Time_Format:
                    del self.dicc_Data[user]
            self.register2json()

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        DATA = []
        self.json2registered()
        self.check_server()
        for line in self.rfile:
            DATA.append(line.decode('utf-8'))
        DATA = "".join(DATA).split()
        user = DATA[1].split(":")
        if DATA[0] == "REGISTER":
            if int(DATA[4]) == 0:
                try:
                    print("Usuario borrado:", user[1], "\r\n\r\n")
                    del self.dicc_Data[user[1]]
                    self.register2json()
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                except KeyError:
                    self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
            elif int(DATA[4]) >= 0:
                tiempo_exp = float(DATA[4]) + time.time()
                tiempo_exp = time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.gmtime(tiempo_exp))
                print(" ".join(DATA), "\r\n\r\n")
                self.dicc_Data[user[1]] = (self.client_address[0],
                                           "Expires: " + tiempo_exp)
                self.register2json()
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    try:
        serv = socketserver.UDPServer(("", int(sys.argv[1])),
                                      SIPRegisterHandler)
        print("Lanzando servidor UDP de eco...")
    except ValueError:
        sys.exit("./server port")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
