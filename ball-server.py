#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Server side of the NetworkBall application
# Send a ball to all the clients (like a token ring)
#

# External dependencies
import select
import socket
import sys
import time
import threading

# Class to send the ball position to the clients
class BallServer( threading.Thread ) :
	# Server main loop
	def run( self ) :
		# Set up the server connection
		server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		server.bind( ( '', 10000 ) )
		server.listen( 5 )
		# List of connected clients
		clients = []
		# Ball coordinates and speed
		x, y, v, dx, dv = 0.1, 0.1, 0, 0.006, 0.006
		# Continuously accept client connection, and send ball position
		self.running = True
		while self.running :
			# New client connection
			ready, _, _ = select.select( [ server ], [], [], 0 )
			if ready :
				client, _ = server.accept()
				clients.append( client )
			# Temporize, and continue if there is no client
			if not clients :
				time.sleep( 0.1 )
				continue
			# Invert the ball direction if it reaches a border
			if x < 0 or x > len( clients ) : dx = -dx
			if y > 0.95 :
				y = 0.95
				v = -v
			# Compute the ball position
			x += dx
			v += dv
			y += v
			# Loop through the client list to send the ball position
			for n, client in enumerate( clients ) :
				# Send the coordinates
				try : client.send( '{};{}\n'.format( x - n, y ).encode( 'ascii' ) )
				# Client connection error
				except IOError :
					# Close the client connection
					client.close()
					# Remove the client connection from the client list
					clients.remove( client )
					# Fix the ball position
					if clients and x > len( clients ) : x -= 1
			# Temporization
			time.sleep( 0.03 )
		# Close the client connections
		for client in clients : client.close()
		# Close the server
		server.close()

# Main application
if __name__ == '__main__' :
	# Start the server
	server = BallServer()
	server.start()
	# Wait for user key press
	if sys.version_info[0] < 3 : raw_input( 'Press <enter> to stop the server...' )
	else : input( 'Press <enter> to stop the server...' )
	# Stop the server
	server.running = False
	server.join()
