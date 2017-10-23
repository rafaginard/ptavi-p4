#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_Data = {}
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """

        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            line.decode('utf-8')
            dicc_Data[SERVER] =  port
            print("El cliente nos manda ", dicc_Data[SERVER])

if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
