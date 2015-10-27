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


#
# Class to send the ball position to the clients
#
class BallServer( object ) :

	#
	# Initialization
	#
	def __init__( self ) :

		# Set up the server connection
		self.server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		self.server.bind( ( '', 10000 ) )
		self.server.listen( 5 )
		
		# List of connected clients
		self.clients = []

	#
	# Start the server
	#
	def Start( self ) :
		
		# Ball coordinates and speed
		x, y, v, dx, dv = 0.02, 0.04, 0, 0.006, 0.004

		# Infinite service
		while True :

			# Get the list of sockets which are ready to be read through select
			ready, _, _ = select.select( [ self.server ], [], [], 0 )
			
			# New client connection
			if ready :
				client, _ = self.server.accept()
				self.clients.append( client )
					
			# Continue if there is no client
			if not self.clients :
				time.sleep( 0.1 )
				continue

			# Compute the ball position
			if x < 0 or x > len( self.clients ) :
				dx = -dx
			x += dx
			v += dv
			y += v 
			if y > 0.8 :
				y = 0.8
				v = -v

			# Loop through the client list to send the ball position
			for n, client in enumerate( self.clients ) :
				
				# Send the coordinates
				try : client.send( '{};{}\n'.format( x - n, y ) )
				
				# Client connection error
				except IOError :
					
					# Close the client connection
					client.close()
					
					# Remove the client connection from the client list
					self.clients.remove( client )
					
					# Fix the ball position
					if self.clients and x > len( self.clients ) :
						x -= 1

			# Temporization
			time.sleep( 0.03 )


#
# Main application
#
if __name__ == '__main__' :

	# Start the server
	ball = BallServer()
	try : ball.Start()
			
	# Keyboard interruption
	except KeyboardInterrupt :

		# Close the client connections
		for client in ball.clients :
			client.close()

		# Close the server
		ball.server.close()
