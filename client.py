#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# Client side of the NetworkDemo application
#
# Receive the ball from the server, and display it
#


#
# External dependencies
#
import socket
import sys
import threading
from PyQt4 import QtCore
from PyQt4 import QtGui


#
# Class to receive the ball position from the server (threaded)
#
class BallClient( threading.Thread ) :
	
	#
	# Initialization
	#
	def __init__( self, server, widget ) :

		# Initialize the thread
		super( BallClient, self ).__init__()
		
		# Server address
		self.server = server

		# Graphical user interface
		self.widget = widget

		# Ball position
		self.position = [ 0, 0 ]

	#
	# Thread main loop
	#
	def run( self ) :
		
		# Connect to the server
		connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		connection.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		connection.connect( ( self.server, 10000 ) )

		# Continuously receive messages from the server
		self.running = True
		while self.running :

			# Receive the message from the server
			message = connection.recv( 256 )
			
			# Server is dead
			if not message :
				
				# Stop the client connection
				self.running = False
				break
				
			# Decode the message to get the ball position
			sx, _, sy = message.decode( 'ascii' ).partition( ';' )

			# Save the ball position
			self.position = [ float( sx ), float( sy ) ]

			# Update the widget
			self.widget.update()

		# Close the connection
		connection.close()

		# Close the widget
		self.widget.close()


#
# Widget to display the ball
#
class BallWidget( QtGui.QWidget ) :
	
	#
	# Initialization
	#
	def __init__( self, parent = None ) :

		# Initialize the widget
		super( BallWidget, self ).__init__( parent )

		# Change the window title
		self.setWindowTitle( 'NetworkDemo' )
		
		# Change the window position and size
		self.setGeometry( 0, 0, 1920, 1200 )
		
		# Change the widget background color
		self.setStyleSheet( "background-color:white;" )

		# Set the Escape key to close the application
		QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self ).activated.connect( self.close )
		
		# Ball client thread
		self.ball = BallClient( sys.argv[ 1 ], self )
		self.ball.start()
		
	#
	# Paint the ball
	#
	def paintEvent( self, event ) :
		
		# Set up the painter
		paint = QtGui.QPainter( self )
		paint.setRenderHint( QtGui.QPainter.Antialiasing )
		paint.setBrush( QtCore.Qt.red )
		
		# Get the ball position
		position = QtCore.QPoint( self.ball.position[0] * self.size().width(),
								  self.ball.position[1] * self.size().height() )
								  
		# Draw the ball
		paint.drawEllipse( position, 60, 60 )

	#
	# Close the widget
	#
	def closeEvent( self, event ) :

		# Stop the ball client
		if self.ball.running :
			self.ball.running = False
			self.ball.join()
			
		# Close the widget
		event.accept()


#
# Main application
#
if __name__ == '__main__' :

	# Start Qt application
	application = QtGui.QApplication( sys.argv )
	widget = BallWidget()
	widget.show()
	sys.exit( application.exec_() )

