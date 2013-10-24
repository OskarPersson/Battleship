import socket
import ast
import sys

class Client:
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, 	# Internet
	         					socket.SOCK_DGRAM) 	# UDP
		self.addr = []
		self.connected = False
		ip = raw_input('IP to connect to?\n')
		port = raw_input('Port to connect to?\n')
	
		self.connect(ip, port)

	def sendMessage(self, m):
		self.sock.sendto(str(m), (self.addr[0], self.addr[1])) #Sends a message to the server

	def toList(self, s): #Converts string represantation of list to list object
		l = ast.literal_eval(s)
		return l

	def connect(self, ip, port):
	
		message = 'connect'
		self.sock.sendto(message, (ip, int(port))) #send a the "connect" message to the given ip and port
		
		while self.connected == False: #waits for the 'connected' message from the correct ip
			data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
			if isinstance(self.addr, tuple) and data == 'connected':
				if self.addr[0] == ip:
					self.connected = True

		print 'connected to ' + str(self.addr[0])
		

		import game
		g = game.Game() #Starts the game
		g.p2 = g.newPlayer(2, g.ships[:], g.p2Field, g.p2BombField)

		self.sendMessage(['done', g.p2.field.field, g.p2.name])

		while data != 'gameDone': #waits for the 'gameDone' message from the correct ip
			print 'Waiting for server...'
			data, self.addr = self.sock.recvfrom(2048) # buffer size is 2048 bytes
			if data != '':
				dataList = self.toList(data)
				if dataList[0] == 'selectCell':
					g.clear()
					g.p2.field.field = dataList[1]
					print 'Your field:\n'
					print(g.printfield(g.p2.field.field))
					print '\nEnemy field:\n'
					print(g.printfield(g.p2.bombfield.field))
					cell = g.selectCell(g.p2)
					self.sendMessage(['cell', cell])

					while data != 'result': #waits for the 'result' message from the correct ip
						data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
						if data != '':
							dataList = self.toList(data)
							data = dataList[0]
							if data == 'result':
								g.clear()
								if dataList[1] == 'X':
									print 'Hit!'
								elif dataList[1] == 'O':
									print 'Miss!'
								else:
									data = 'gameDone'
									print dataList[1]
									sys.exit()
								g.p2.bombfield.field[cell[0]][int(cell[1])] = dataList[1]
								print 'Your field:\n'
								print(g.printfield(g.p2.field.field))
								print '\nEnemy field:\n'
								print g.printfield(g.p2.bombfield.field)
					data = ''
				
				elif dataList[0] == 'result':
					g.clear()
					if dataList[1] == 'X':
						print 'Hit!'
					elif dataList[1] == 'O':
						print 'Miss!'
					else:
						data = 'gameDone'
						print dataList[1]
						sys.exit() #Exit the application





