#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Application serveur JPO IUT Auxerre
#
# Le programme "serveur" accepte les connexions d'une liste prédéfinie de clients possibles
# et leur donne la main à tour de rôle, un peu comme un jeton dans un "token ring".
#
# (c)2010eB@uB

# python JPOsrvr.py port_number

import socket # Module réseau local TCP/IP
import thread # Module de gestion des sous-processus
import sys
from time import sleep

# Message de bienvenue...
print "Bienvenue dans l'application JPO Auxerre: coté serveur"

# set up Internet TCP socket
lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])  # server port number
# bind lstn socket to this port 
lstn.bind(('', port))
# start listening for contacts from clients
lstn.listen(5)

# Liste des IP des clients
hosts = []

# Nombre de clients requis
N=2

# Clients connectés
chosts = []
clock = thread.allocate_lock()  

# Ecoute des demandes de connexion des clients tant que tous ne sont
# pas connectés

liste_client = {}

while len(hosts)<N:
	(clnt,ap) = lstn.accept()
	client = clnt.getpeername()
	print "Demande de connexion ",client
	hosts.append( client )
	# Teste si le client est un client autorisé
	if client in hosts:
		print( 'Demande de connexion de {}:{}'.format( *client ) )
		# Teste si le client est déjà connecté
		if client in chosts: 
			print "Client déjà connecté"
			print "Demande de connexion rejetée"
		else:
			print "Demande acceptée sur Port %s" % client[1]
			liste_client[client]=clnt
	else:
		print "Tentative de connexion d'un poste inconnu "+client[0]
		print "Demande de connexion rejetée"

print "Tous les clients sont connectés, l'application est opérationelle"

# Fermeture du port d'écoute principal
lstn.close()


sw = 1920
sh = 1200
# test
print "screen width  =", sw
print "screen height =", sh 

# initialisation des coordonnées, des vitesses et du témoin d'animation :    
x, y, v, dx, dv = 50, 50, 0, 12, 5
sh = sh - 100 - 30

while 1:
#   print "Calcul de l'itération suivante"
   xp, yp = x, y            # mémorisation des coord. précédentes
   # déplacement horizontal :
   if x > N*sw or x < 0 :     # rebond sur les parois latérales :
      dx = -dx             # on inverse le déplacement
   x = x + dx
   # variation de la vitesse verticale (toujours vers le bas):
   v = v + dv
   # déplacement vertical (proportionnel à la vitesse)
   y = y + v       
   if y > sh:              # niveau du sol à 240 pixels : 
      y = sh             #  défense d'aller + loin !
      v = -v               # rebond : la vitesse s'inverse
   n=0
   for chost in hosts:
      print( 'Coordonnées ({},{}) envoyées à {}:{}'.format( x, y, *chost ) )
      clnt=liste_client[chost]
      clnt.send("%d,%d.\n" % (x-n*sw,y))
      n=n+1
   sleep(0.03)

# Attente de la déconnexion de tous les clients 
while len(chosts) > 0: pass
print "Done"
