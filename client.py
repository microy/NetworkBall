#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# Client side of the NetworkDemo application
#


#
# External dependencies
#
import socket
import sys
import threading
from Tkinter import *


#
# Thread to receive the ball position from the server
#
class Ball( threading.Thread ) :
	
	#
	# Initialization
	#
	def __init__( self, server, can, root ) :

		# Initialize the thread
		threading.Thread.__init__( self )
		
		# Graphical component
		self.can = can
		self.root = root

		# Create Internet TCP socket
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.connection.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

		# Network connection
		try :

			self.connection.connect( ( server, 10000 ) )

		except :

			print( 'Connection failed...' )
			sys.exit()    

		print( 'Connected to the server...' )

	#
	# Thread main loop
	#
	def run( self ) :
		
		self.running = True

		# Main loop
		while self.running :

			msg = self.connection.recv( 256 )
			if not msg : break
		#	print( 'Frame {}'.format( msg ) )
			car, sep, cdr = msg.partition( '.' )
			sx, sep, sy = car.partition( ',' )
			x = int( sx )
			y = int( sy )
		#	print( 'x = {}  ~  y = {}'.format( x, y ) )
			self.can.coords( balle, x-30, y-30, x+30, y+30 )
			self.root.update()



# Graphical user interface
root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry( '{}x{}+0+0'.format( sw, sh ) )
can = Canvas( root, width =sw, height=sh-100, bg='white' )
can.pack()
balle = can.create_oval( 0, 0, 0, 0, fill = 'red' )
Button( root, text = 'Quit', command = root.quit ).pack( side = BOTTOM, pady = 30 )

# Ball thread
try :
	ball_thread = Ball( sys.argv[ 1 ], can, root )
	ball_thread.start()
	root.mainloop()
except :
	ball_thread.running = False
	ball_thread.join()
	ball_thread.connection.close()

        
        
