#!/usr/bin/env python3

#
# Client side of the NetworkBall application
# Receive the ball from the server, and display it with Qt
#

# External dependencies
import ipaddress
import os
import socket
import sys
import threading
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

# Class to receive the ball position from the server (threaded)
class BallClient( threading.Thread ) :
	# Initialization
	def __init__( self, server, widget ) :
		# Initialize the thread
		super( BallClient, self ).__init__()
		# Server address
		self.server = server
		# Graphical user interface
		self.widget = widget
		# Ball position
		self.position = [ 0, 0 ]
		# Thread running
		self.running = False
	# Thread main loop
	def run( self ) :
		# Connect to the server
		connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		connection.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		try : connection.connect( ( self.server, 10000 ) )
		except :
			print( 'Cannot connect to server...' )
			self.widget.close()
			return
		print( 'Client :', connection.getsockname() )
		print( 'Server :', connection.getpeername() )
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
			x, _, y = message.decode( 'ascii' ).partition( ';' )
			# Save the ball position
			self.position = [ float( x ), float( y ) ]
			# Update the widget
			self.widget.update()
		# Close the connection
		connection.close()
		# Close the widget
		self.widget.close()

# Widget to display the ball
class BallClientWidget( QtWidgets.QWidget ) :
	# Initialization
	def __init__( self, parent = None ) :
		# Initialize the widget
		super( BallClientWidget, self ).__init__( parent )
		# Change the window title
		self.setWindowTitle( 'NetworkBall' )
		# Change the widget background color
		self.setStyleSheet( "background-color:white;" )
		# Set the Escape key to close the application
		QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self ).activated.connect( self.close )
		# Set the F12 key to toggle fullscreen
		QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_F12 ), self ).activated.connect( self.ToggleFullScreen )
		# Ball client thread
		self.ball = BallClient( sys.argv[ 1 ], self )
		self.ball.start()
	# Paint the ball
	def paintEvent( self, event ) :
		# Set up the painter
		paint = QtGui.QPainter( self )
		paint.setRenderHint( QtGui.QPainter.Antialiasing )
		paint.setBrush( QtCore.Qt.red )
		# Get the ball position
		position = QtCore.QPoint( int( self.ball.position[0] * self.size().width() ), int( self.ball.position[1] * self.size().height() ) )
		# Draw the ball
		paint.drawEllipse( position, 60, 60 )
	# Close the widget
	def closeEvent( self, event ) :
		# Stop the ball client
		if self.ball.is_alive() and self.ball.running :
			self.ball.running = False
			self.ball.join()
		# Close the widget
		event.accept()
	# Toggle widget fullscreen
	def ToggleFullScreen( self ) :
		# Show normal
		if self.isFullScreen() : self.showNormal()
		# Show fullscreen
		else : self.showFullScreen()

# Main application
if __name__ == '__main__' :
	# Remove Qt warnings
	os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
	os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
	os.environ["QT_SCALE_FACTOR"] = "1"
	# Check command line argument
	if len( sys.argv ) != 2 :
		print( 'Usage :', sys.argv[0], '<server_address>' )
		exit()
	# Validate the IP address in command line
	try : ip = ipaddress.ip_address( sys.argv[1] )
	except :
		print('Server address is invalid :', sys.argv[1] )
		exit()
	# Launch application
	application = QtWidgets.QApplication( sys.argv )
	widget = BallClientWidget()
	widget.show()
	sys.exit( application.exec_() )
