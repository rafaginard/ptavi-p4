#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINE = sys.argv[4]
EXPIRES = sys.argv[5]


def register():
    DATA = ("REGISTER sip:" + LINE + " SIP/2.0\r\nExpires: " +
            EXPIRES + "\r\n\r\n")
    my_socket.send(bytes(DATA, "utf-8"))
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    if sys.argv[3] == "register":
        register()
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
