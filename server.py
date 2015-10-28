#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# Server side of the NetworkDemo application
#
# Send a ball to all the clients (like a token ring)
#


#
# External dependencies
#
import select
import socket
import time


# Set up the server connection
server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
server.bind( ( '', 10000 ) )
server.listen( 5 )

# List of connected clients
clients = []

# Ball coordinates and speed
x, y, v, dx, dv = 0.1, 0.1, 0, 0.006, 0.006

# Infinite service
while True :

	# New client connection
	ready, _, _ = select.select( [ server ], [], [], 0 )
	if ready :
		client, _ = server.accept()
		clients.append( client )
			
	# Temporize, and continue if there is no client
	if not clients :
		time.sleep( 0.1 )
		continue

	# Compute the ball position
	if x < 0 or x > len( clients ) :
		dx = -dx
	x += dx
	v += dv
	y += v 
	if y > 0.95 :
		y = 0.95
		v = -v

	# Loop through the client list to send the ball position
	for n, client in enumerate( clients ) :
		
		# Send the coordinates
		try : client.send( '{};{}\n'.format( x - n, y ) )
		
		# Client connection error
		except IOError :
			
			# Close the client connection
			client.close()
			
			# Remove the client connection from the client list
			clients.remove( client )
			
			# Fix the ball position
			if clients and x > len( clients ) :
				x -= 1

	# Temporization
	time.sleep( 0.03 )
