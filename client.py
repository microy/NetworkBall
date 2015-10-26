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
from PyQt4 import QtCore
from PyQt4 import QtGui


#
# Thread to receive the ball position from the server
#
class NetworkBallClient( threading.Thread ) :
	
	#
	# Initialization
	#
	def __init__( self, server, widget ) :

		# Initialize the thread
		super( NetworkBallClient, self ).__init__()
		
		# Graphical user interface
		self.widget = widget

		# Create Internet TCP socket
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.connection.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

		# Network connection
		try : self.connection.connect( ( server, 10000 ) )
		except :
			print( 'Connection failed...' )
			sys.exit()    
		print( 'Connection established...' )

	#
	# Thread main loop
	#
	def run( self ) :
		
		# Main loop
		self.running = True
		while self.running :

			msg = self.connection.recv( 256 )
			if not msg : break
		#	print( 'Frame {}'.format( msg ) )
			car, sep, cdr = msg.partition( '.' )
			sx, sep, sy = car.partition( ',' )
			x = int( sx )
			y = int( sy )
		#	print( 'x = {}  ~  y = {}'.format( x, y ) )
			# Send the image to the widget through a signal
			self.widget.ball_position_updated.emit( x, y )
			
		print( 'Connection closed...' )
		self.connection.close()
		self.widget.close()


#
# Widget to display the ball
#
class Widget( QtGui.QWidget ) :
	
	#
	# Signal to receive the new ball position from the server
	#
	ball_position_updated = QtCore.pyqtSignal( int, int )

	#
	# Initialization
	#
	def __init__( self, parent = None ) :

		# Initialize QLabel
		super( Widget, self ).__init__( parent )

		# Change the window title
		self.setWindowTitle( 'NetworkDemo' )
		
		# Change the widget position and size
		self.setGeometry( 0, 0, 1920, 1200 )
		
		# Set the Escape key to close the application
		QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self ).activated.connect( self.close )
		
		# Ball thread
		self.ball_thread = NetworkBallClient( sys.argv[ 1 ], self )
		self.ball_thread.start()
		
		# Ball Position
		self.ball_position = QtCore.QPoint()

		# Connect the signal to update the ball position
		self.ball_position_updated.connect( self.UpdateBallPosition )
		
	#
	# Update the ball position
	#
	def UpdateBallPosition( self, x, y ) :
		
		self.ball_position.setX( x )
		self.ball_position.setY( y )
		self.update()

	#
	# Paint the ball
	#
	def paintEvent( self, event ) :
		
		paint = QtGui.QPainter( self )
		paint.setRenderHint( QtGui.QPainter.Antialiasing )
		paint.setBrush( QtCore.Qt.red )
		paint.drawEllipse( self.ball_position, 60, 60 )

	#
	# Close the widget
	#
	def closeEvent( self, event ) :

		self.ball_thread.running = False
		self.ball_thread.join()
		event.accept()


#
# Main application
#
if __name__ == '__main__' :

	application = QtGui.QApplication( sys.argv )
	widget = Widget()
	widget.show()
	sys.exit( application.exec_() )

