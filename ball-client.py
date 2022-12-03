#!/usr/bin/env python3

#
# Client side of the NetworkBall application
# Receive the ball from the server, and display it with Qt
#

# External dependencies
import sys
from PySide6.QtCore import QPoint
from PySide6.QtGui import Qt, QKeySequence, QPainter, QShortcut
from PySide6.QtNetwork import QHostAddress, QTcpSocket
from PySide6.QtWidgets import QApplication, QWidget

# Widget to display the ball
class BallClientWidget( QWidget ) :
	# Initialization
	def __init__( self ) :
		# Initialize the widget
		super( BallClientWidget, self ).__init__()
		# Change the window title
		self.setWindowTitle( 'Network Ball' )
		# Change the widget background color
		self.setStyleSheet( "background-color:white;" )
		# Set the Escape key to close the application
		QShortcut( QKeySequence( Qt.Key_Escape ), self ).activated.connect( self.close )
		# Set the F12 key to toggle fullscreen
		QShortcut( QKeySequence( Qt.Key_F12 ), self ).activated.connect( self.ToggleFullScreen )
		# Network connection
		self.connection = QTcpSocket( self )
		self.connection.readyRead.connect( self.ReceiveMessage )
		self.connection.disconnected.connect( self.close ) 
		self.connection.connectToHost( QHostAddress( sys.argv[ 1 ] ), 10000 )
		# Wait for the connection
		if not self.connection.waitForConnected() :
			print( 'Cannot connect to server...' )
			exit()
		# Initialize ball position
		self.position = [ 0, 0 ]
	# Receive the messages
	def ReceiveMessage( self ) :
		# Read the message from the server
		message = self.connection.readLine()
		# Decode the message to get the ball position
		x, _, y = str( message, 'ascii' ).partition( ';' )
		# Save the ball position
		self.position = [ float( x ), float( y ) ]
		# Update the widget and the ball
		self.update()
	# Paint the ball
	def paintEvent( self, event ) :
		# Set up the painter
		paint = QPainter( self )
		paint.setRenderHint( QPainter.Antialiasing )
		paint.setBrush( Qt.red )
		# Get the ball position
		position = QPoint( int( self.position[0] * self.size().width() ), int( self.position[1] * self.size().height() ) )
		# Draw the ball
		paint.drawEllipse( position, 60, 60 )
	# Toggle widget fullscreen
	def ToggleFullScreen( self ) :
		# Show normal
		if self.isFullScreen() : self.showNormal()
		# Show fullscreen
		else : self.showFullScreen()

# Main application
if __name__ == '__main__' :
	# Check command line argument
	if len( sys.argv ) != 2 :
		print( 'Usage :', sys.argv[0], 'server_address' )
		exit()
	# Launch application
	application = QApplication( sys.argv )
	widget = BallClientWidget()
	widget.show()
	sys.exit( application.exec() )
