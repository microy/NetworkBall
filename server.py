#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# Server side of the NetworkDemo application
#


#
# External dependencies
#
import select
import socket
import time

	
# Screen size
sw = 1920
sh = 1200

# Ball coordinates and speed
x, y, v, dx, dv = 50, 50, 0, 12, 5

# Border
sh = sh - 100 - 30

# Set up the server connection
server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
server.bind( ( '', 10000 ) )
server.listen( 5 )

# List of the connected clients
clients = []

# Catch keyboard interruption
try :
	
	# Infinite service
	while True :

		# Get the list of sockets which are ready to be read through select
		ready, _, _ = select.select( [ server ], [], [], 0 )
		
		# New client connection
		if ready :
			client, _ = server.accept()
			clients.append( client )
				
		# Continue if there is no client
		if not clients :
			time.sleep( 0.1 )
			continue

		# Compute the ball position
		if x > len( clients ) * sw or x < 0 :
			dx = -dx
		x = x + dx
		v = v + dv
		y = y + v 
		if y > sh :
			y = sh
			v = -v

		# Loop through the client list to send the ball position
		for n, client in enumerate( clients ) :
			
			# Send the coordinates
			try : client.send( '{},{}.\n'.format( x - n * sw, y ) )
			
			# Client connection error
			except IOError :
				
				# Close the client connection
				client.close()
				
				# Remove the client connection from the client list
				clients.remove( client )
				
				# Fix the ball position
				if clients and x > len( clients ) * sw :
					x -= sw

		# Waiting timer
		time.sleep( 0.03 )

# Keyboard interruption with Ctrl+C
except KeyboardInterrupt :

	# Close the server
	server.close()

	# Close the client connections
	for client in clients :
		client.close()
