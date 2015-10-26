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
import threading
import time


#
# Thread to compute the position of the ball
#
class NetworkBallServer( threading.Thread ) :
	
	#
	# Initialization
	#
	def __init__( self ) :

		# Initialize the thread
		super( NetworkBallServer, self ).__init__()

		# Client list
		self.clients = []

	#
	# Thread main loop
	#
	def run( self ) :
		
		self.running = True

		# Screen size
		sw = 1920
		sh = 1200

		# Ball coordinates and speed
		x, y, v, dx, dv = 50, 50, 0, 12, 5

		# Border
		sh = sh - 100 - 30

		# Thread running
		while self.running :
			
			# No clients
			if not self.clients :
				time.sleep( 0.1 )
				continue

			# Horizontal move
			if x > len(self.clients)*sw or x < 0 :     # rebond sur les parois latérales :
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
			for n, client in enumerate( self.clients ) :
				
			#	print( 'Coordonnées ({},{}) envoyées à {}:{}'.format( x, y, *chost ) )

				# Send the coordinates
				try : client.send( '{},{}.\n'.format( x-n*sw, y ) )
				
				# Client isn't here anymore
				except :
					print( 'Connection lost...' )
					client.close()
					self.clients.remove( client )
					# Initialize ball parameters
					if self.clients : x -= sw

			# Timer
			time.sleep( 0.03 )


# Set up Internet TCP socket
server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

# Bind socket to port 10000
server.bind( ( '', 10000 ) )

# Start listening for contacts from clients
server.listen( 5 )

# Ball thread
ball_thread = NetworkBallServer()
ball_thread.start()

try :

	# Client connection
	while True :
		
		connection, _ = server.accept()
		print( 'Connection from {}:{}...'.format( *connection.getpeername() ) )
		ball_thread.clients.append( connection )

except :
	
	# Close the server
	server.close()
	ball_thread.running = False
	ball_thread.join()
	for client in ball_thread.clients :
		client.connection.close()
