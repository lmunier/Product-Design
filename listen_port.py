#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm201217.0517

# File to listen on the specified port

import socket
import select

from manage_db import add_data

hote = ''
port = 2048

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))

serveur_lance = True

while serveur_lance:
    connexion_principale.listen(5)
    clients_connectes = []

    # Listen on connection port to know if client would like to connect, 50ms wait max
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()

        # Add socket to client list
        clients_connectes.append(connexion_avec_client)

    # We test client_a_lire, if it's empty we have an exception
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass
    else:
        # We browse our client list
        for client in clients_a_lire:
            # Client is a socket type
            msg_recu = client.recv(1024)

            # Can fail if msg_recu have special characters
            msg_recu = msg_recu.decode()
            add_data(msg_recu)

            # Send confirmation to client and close it
            client.send(b"y")
            client.close()

            # Possibility to close all the connections
            if msg_recu == "f":
                serveur_lance = False

# close all the connections
for client in clients_connectes:
    client.close()

connexion_principale.close()
