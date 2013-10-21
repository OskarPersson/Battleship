import socket
import ast
import sys
import threading
import player


class Server:

	def __init__(self):
		self.threads = []

		self.ip = socket.gethostbyname(socket.gethostname()) #Get computer IP
		self.port = 5005
		self.sock = socket.socket(socket.AF_INET, 	# Internet
	         					socket.SOCK_DGRAM) 	# UDP
		self.sock.bind((self.ip, self.port))

		self.addr = []
		self.connected = False
		self.serverDone = False
		self.clientDone = False

		print("Your IP: " + self.ip + " and port: " + str(self.port))

	def sendMessage(self, m):
		self.sock.sendto(str(m), (self.addr[0], self.addr[1])) #sends a message to the client

	def waitForClient(self): #checks if the client is done with the setup
		data = ''
		while len(self.addr) == 0 or data != 'done':
			data, self.addr = self.sock.recvfrom(4096) # buffer size is 4096 bytes
			
			if data != '':
				dataList = self.toList(data)
				data = dataList[0]
				self.enemyField = dataList[1]
				self.enemyName = dataList[2]
		
		self.clientDone = True

	def toList(self, s): #Converts string represantation of list to list object
		l = ast.literal_eval(s)
		return l

	def toDict(self, s):
		d = ast.literal_eval(s)
		return d

	def connect(self):

		while len(self.addr) == 0 or data != 'connect': #wait for a client to connect
			data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes

		print str(self.addr[0]) + ' connected'
		self.connected = True

		self.sendMessage('connected') #tells the client that it is connected

		#Start a separate thread to wait for the client while both players place their ships.
		#This way both players can do it at the same time and the application can then tell a player if the opponent is done or not

		thread = threading.Thread(target=self.waitForClient)
		thread.start()
		self.threads.append(thread)

		import game
		g = game.Game()
		g.p1 = g.newPlayer(1, g.ships[:], g.p1Field, g.p1BombField)
		self.done = True
		
		raw_input('Press enter when you are done')
		g.clear()

		#if the client is not done with the setup,
		#then stop the thread and wait for the message in the "main thread"
		self.threads[0]._Thread__stop()
		if self.clientDone == False:
			print 'Waiting for client...'
			self.waitForClient()
		
		print 'Client done'

		g.p2Field.field = self.enemyField
		g.p2 = player.Player(self.enemyName, g.ships[:], g.p2Field, g.p2BombField)

		while g.anythingLeft(g.p1.field.field) and g.anythingLeft(g.p2.field.field): #While ships left, keep playing
			g.clear()
			print 'Your field:\n'
			print(g.printfield(g.p1.field.field))
			print '\nEnemy field:\n'
			print(g.printfield(g.p1.bombfield.field))
			cell = g.selectCell(g.p1)
			g.bomb(g.p1, g.p2, cell[0], cell[1])
			g.clear()

			if g.result == 'X':
				print 'Hit!'
			elif g.result == 'O':
				print 'Miss!'
			else:
				print g.result
				self.sendMessage(['result', g.result])
				sys.exit() #Exit the application

			print 'Your field:\n'
			print(g.printfield(g.p1.field.field))
			print '\nEnemy field:\n'
			print(g.printfield(g.p1.bombfield.field))

			if g.anythingLeft(g.p1.field.field) and g.anythingLeft(g.p2.field.field):
				self.sendMessage(['selectCell', g.p2.field.field])
				data = ''
				print 'Waiting for client...'
				while len(self.addr) == 0 or data != 'cell':
					data, self.addr = self.sock.recvfrom(2048) # buffer size is 2048 bytes
					if data != '':
						dataList = self.toList(data)
						data = dataList[0]
						cell = dataList[1]

				g.bomb(g.p2, g.p1, cell[0], cell[1])
				
				if g.result == 'X' or g.result == 'O':
					self.sendMessage(['result', g.result])	
				else:
					print g.result
					self.sendMessage(['result', g.result])
					sys.exit() #Exit the application


