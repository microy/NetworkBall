#! /usr/bin/env python3

#
# Server side of the NetworkBall application
# Send a ball to all the clients (like a token ring)
#

# External dependencies
import asyncio

# Client connections
clients = []

# Ball server
async def BallServer() :
	# Ball coordinates and speed
	x, y, v, dx, dv = 0.1, 0.1, 0, 0.006, 0.006
	# Infinite loop
	while True :
		# Continue if there is no client
		if not clients :
			await asyncio.sleep( 0.1 )
			continue
		# Fix ball position if we lost a client
		if x - 0.1 > len( clients ) : x -= 1
		# Invert the ball direction if it reaches a border
		if x < 0 or x > len( clients ) : dx = -dx
		if y > 0.95 :
			y = 0.95
			v = -v
		# Compute the ball position
		x += dx
		v += dv
		y += v
		# Send the ball position to every client
		for n, client in enumerate( clients ) :
			client.transport.write( '{};{}\n'.format( x - n, y ).encode( 'ascii' ) )
		# Wait
		await asyncio.sleep( 0.03 )

# Client connection handle
class BallServerProtocol( asyncio.Protocol ) :
	# Connection
	def connection_made( self, transport ) :
		self.peername = transport.get_extra_info( 'peername' )[:2]
		print( 'Connection opened from', self.peername )
		self.transport = transport
		clients.append( self )
	# Disconnection
	def connection_lost( self, _ ) :
		print( 'Connection closed from', self.peername )
		clients.remove( self )

# Main program
async def main():
	# Create the ball server task
	task = asyncio.create_task( BallServer() )
	# Create the server to handle client connections
	server = await asyncio.get_running_loop().create_server( lambda: BallServerProtocol(), '', 10000)
	async with server :
		await server.serve_forever()
	# Run the ball server
	await task

# Main application
if __name__ == '__main__' :
	try :
		print( '\nPress ^C to stop the server...\n' )
		asyncio.run( main() )
	except KeyboardInterrupt :
		pass
