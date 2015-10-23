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
from Tkinter import *

# Graphical user interface
root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
#print( 'Screen width  = {}'.format( sw ) )
#print( 'Screen height = {}'.format( sh ) )

# Set to full screen
root.geometry( '{}x{}+0+0'.format( sw, sh ) )

can = Canvas( root, width =sw, height=sh-100, bg='white' )
can.pack()
balle = can.create_oval( 0, 0, 0, 0, fill = 'red' )
Button( root, text = 'Quit', command = root.quit ).pack( side = BOTTOM, pady = 30 )

# Create Internet TCP socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Server address
host = sys.argv[ 1 ]

# Server port
port = int( sys.argv[ 2 ] )

# Network connection
try :

	s.connect( ( host, port ) )

except socket.error :

	print( 'Connection failed...' )
	sys.exit()    

print( 'Connected to the server...' )

# Main loop
while 1 :

	msg = s.recv( 256 )
	if not msg : break
#	print( 'Frame {}'.format( msg ) )
	car, sep, cdr = msg.partition( '.' )
	sx, sep, sy = car.partition( ',' )
	x = int( sx )
	y = int( sy )
#	print( 'x = {}  ~  y = {}'.format( x, y ) )
	can.coords( balle, x-30, y-30, x+30, y+30 )
	root.update()

print( 'Connection lost...' )
s.close()

        
        
