#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Server side of the NetworkDemo application
#

#
# External dependencies
#
import socket
import sys
import time

# Set up Internet TCP socket
server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

# Bind socket to port 10000
server.bind( ( '', 10000 ) )

# Start listening for contacts from clients
server.listen( 16 )

# Client list
hosts = []

# Required client number
N = 2

# Client connection list
liste_client = {}

# Client connection
while len( hosts ) < N :
	
	clnt, ap = server.accept()
	client = clnt.getpeername()
	print( 'Connection from {}:{}...'.format( *client ) )
	hosts.append( client )
	liste_client[ client ] = clnt

# Close the server
server.close()

# Screen size
sw = 1920
sh = 1200

# Ball coordinates and speed
x, y, v, dx, dv = 50, 50, 0, 12, 5

# Border
sh = sh - 100 - 30

# Main loop
while 1 :

	# Horizontal move
	if x > N*sw or x < 0 :     # rebond sur les parois latérales :
		dx = -dx             # on inverse le déplacement
	x = x + dx

	# Vertical speed variation
	v = v + dv

	# Vertical move
	y = y + v 
	if y > sh :              # niveau du sol à 240 pixels : 
		y = sh             #  défense d'aller + loin !
		v = -v               # rebond : la vitesse s'inverse

	# Send ball coordinates to the clients
	for n, chost in enumerate( hosts ) :
		
	#	print( 'Coordonnées ({},{}) envoyées à {}:{}'.format( x, y, *chost ) )
		clnt = liste_client[ chost ]
		
		# Send the coordinates
		try : clnt.send( '{},{}.\n'.format( x-n*sw, y ) )
		
		# Client isn't here anymore
		except socket.error :
			print( 'Connection lost with {}:{}...'.format( *chost ) )
			hosts.remove( chost )
			del liste_client[ chost ]
	
	# No more clients
	if not hosts : break

	# Timer
	time.sleep( 0.03 )
