import os
import sys
import battlefield
import bombfield
import ship
import player

nth = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth"
}

rowlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

class Game:

	def clear(self):
		os.system('tput reset') #clears the terminal window, does not just add new lines but deletes whats been written

	def __init__(self):

		### CREATE PLAYER VARIABLES ###

		self.p1 = ""
		self.p2 = ""

		### CREATE BATTLEFIELDS ###
		self.p1Field = battlefield.Battlefield()
		self.p2Field = battlefield.Battlefield()
		self.p1BombField = bombfield.Bombfield()
		self.p2BombField = bombfield.Bombfield()


		### CREATE SHIPS ###
		self.ships = [];
		'''self.ships.append(ship.Ship(5))
		self.ships.append(ship.Ship(4))'''
		self.ships.append(ship.Ship(3))
		self.ships.append(ship.Ship(3))
		self.ships.append(ship.Ship(2))

	def columnExist(self, column):
	    if("A" <= column <= "J"): #is the column A-J?
	        return True
	    else:
	        return False

	def rowExist(self, row):
	    if(1 <= row <= 10): #is the row 1-10?
	        return True
	    else:
	        return False
	    
	def printfield(self, f):
	    
	    l = [' ', 'A','B','C','D','E','F','G','H','I','J'] #Creates the header
	    spacing = ' '.join(['{:<2}'] * len(l)) #creates a string with len(l)-numbers of '{:<2}' with a space between each one
	    text = spacing.format(*l) #prints the header (column names) with a spacing of 2

	    for v in range(1,len(l)):
	        text += "\n" + spacing.format(v, f['A'][v],f['B'][v],f['C'][v],f['D'][v] ,f['E'][v] ,f['F'][v] ,f['G'][v] ,f['H'][v] ,f['I'][v],f['J'][v]) #Adds all the rows with the row number to the left and a spacing of 2

	    return text
	def placeShips(self, player):
	    counter = 1
	    
	    ### PLAYER INSTRUCTIONS ###
	    print player.name + ", you have 10x10 cells where you can place your ships,\n"
	    print "Remember not to tell your opponent where you place your ships\n"
	    print "Then you say which direction the ship is turned (right, left, up or down)\n"

	    print(self.printfield(player.field.field)) #prints the player's field

	    ### PLACE SHIPS ###
	    for x in player.ships:
	        column = ""
	        row = ""
	        direction = ""
	        cellBusy = True
	        pff = player.field.field
	        while self.columnExist(column) == False or row not in rowlist or cellBusy == True: #loop until the user enters a valid cell
	            userInput = raw_input(player.name + ", in which cell (A-J)(1-10) do you want to place your " + nth[counter] + " ship?\n") #user input for cell
	            if (len(userInput) >= 2): #user input must be atleast 2 characters
	                column = userInput[0].upper() #make userinput upper-case
	                row = userInput[1]
	                if len(userInput) >= 3: #since there is 10 rows, grab the third entered character too (if any)
	                    row += userInput[2]
	            if(self.columnExist(column) and row in rowlist): #If the column and row is valid, check if the cell is busy
	                cellBusy = pff[column][int(row)]
	        
	        row = int(row) #row is converted to integer here because now the entered row must be a valid integer

	        newrow = row
	        newcolumn = column
	        
	        while (direction != "right" and direction != "left" and direction != "up" and direction != "down") or self.rowExist(newrow) == False or self.columnExist(newcolumn) == False or cellBusy == True: #loop until the user enters a valid direction
	            direction = raw_input(player.name + ", in what direction (right, left, up or down) is your " + nth[counter] + " ship turned?\n") #user input for direction
	            cellBusy = False    
	            partCounter = 0

	            for y in range(len(x.parts)): #For each part of the current ship check if the cell is available
	                newcolumn = column
	                newrow = row
	                if(direction == "down"):
	                    newrow = row + partCounter
	                    
	                elif (direction == "up"):
	                    newrow = row - partCounter
	                    
	                elif (direction == "left"):
	                    newcolumn = chr(ord(column) - partCounter) #chr(ord(a) - b) convert 'a' to ASCII, subtract b and convert back the result to a character
	                    
	                elif(direction == "right"):
	                    newcolumn = chr(ord(column) + partCounter)
	                    
	                partCounter += 1
	                if self.columnExist(newcolumn) and self.rowExist(newrow):
	                    if pff[newcolumn][newrow] == True: #is the cell busy?
	                        cellBusy = pff[newcolumn][newrow]
	                    
	                    elif pff[newcolumn][newrow] == False and partCounter == len(x.parts): #if the last cell is available fill all the checked cells
	                        for p in range(0, partCounter):
	                            if(ord(newcolumn) < ord(column)):
	                                pff[chr(ord(column)-p)][newrow] = True
	                            elif(ord(newcolumn) > ord(column)):
	                                pff[chr(ord(column)+p)][newrow] = True
	                            elif(newrow < row):
	                                pff[newcolumn][newrow + p] = True
	                            elif(newrow > row):
	                                pff[newcolumn][newrow - p] = True


	        self.clear()
	        print(self.printfield(player.field.field))
	        counter += 1

	def newPlayer(self, n, ships, field, bombfield): #Creates a new player with the given ships, field and bombfield
	    newName = raw_input("Player " + str(n) + ", what's your name?\n")
	    while newName == "":
	        newName = raw_input("Please, enter something\n")
	    self.clear()
	    p = player.Player(newName, ships[:], field, bombfield)

	    self.placeShips(p)
	    return p #Returns the player object

	def anythingLeft(self, d): #Checks if there is any ships left on the given field
	    newList = []
	    def myprint(d):
	        for k, v in d.iteritems():
	            if isinstance(v, dict): #If v is a dict, call the function with that dict
	              myprint(v)
	            else:
	              newList.append(v) #Else, add v (False/True) to the dict
	    myprint(d)
	    return True in newList #Returns True if there is a True in the list, else return False

	def selectCell(self, player): #Lets the player select a cell to bomb
		column = ""
		row = ""
		while self.columnExist(column) == False or row not in rowlist: #loop until given a valid cell
			userInput = raw_input(player.name + ", in which cell (A-J)(1-10) do you want to bomb your enemy?\n")

			if (len(userInput) < 2): #Reset both values if the input is less than 2 characters
				column = ""
				row = ""
			else: #Set row and column
				column = userInput[0].upper() #Convert input to upper-case
				row = userInput[1]
				if len(userInput) == 3: #since there is 10 rows, grab the third entered character too (if any)
					row += userInput[2]

		return [column, row]

	def bomb(self, player, enemy, column, row): #Gives the given player a chance to bomb the given enemy
	    eff = enemy.field.field 
	    self.result = '' #self.result, saves the latest result from a bombing

	    row = int(row)
	    if(eff[column][row] == True): #if there is a ship at the cell, set an x in the bombfield
	        self.result = 'X' 
	        eff[column][row] = 'X' #mark the enemy's ship field as hit 
	        player.bombfield.field[column][row] = 'X' #mark the current players bombfiled as hit

	        if self.anythingLeft(eff) == False: #Does the enemy have any ships left?
	            self.result = player.name + " wins!"
	    else:
	        self.result = 'O'
	        eff[column][row] = '@' #mark the enemy's ship field as missed
	        if player.bombfield.field[column][row] != 'X': #only mark as missed if you have not hit a ship there before
	        	player.bombfield.field[column][row] = 'O'

	def start(self):
		while self.anythingLeft(self.p1.field.field) and self.anythingLeft(self.p2.field.field): #While ships left, keep playing
			print 'Your field:\n'
			print(self.printfield(self.p1.field.field))
			print '\nEnemy field:\n'
			print(self.printfield(self.p1.bombfield.field))
			cell = self.selectCell(self.p1)
			self.bomb(self.p1, self.p2, cell[0], cell[1]) #player 1 bombs player 2 at the cell given above
			self.clear()

			if self.result == 'X':
				print 'Hit!'
			elif self.result == 'O':
				print 'Miss!'
			else:
				print self.result
				sys.exit() #Exit the application

			print(self.printfield(self.p1.bombfield.field))

			raw_input('Press enter to go to next player')
			self.clear()

			if self.anythingLeft(self.p1.field.field) and self.anythingLeft(self.p2.field.field):
				print 'Your field:\n'
				print(self.printfield(self.p1.field.field))
				print '\nEnemy field:\n'
				print(self.printfield(self.p2.bombfield.field))
				cell = self.selectCell(self.p2)
				self.bomb(self.p2, self.p1, cell[0], cell[1]) #player 2 bombs player 1 at the cell given above
				self.clear()

				if self.result == 'X':
					print 'Hit!'
				elif self.result == 'O':
					print 'Miss!'
				else:
					print self.result
					sys.exit() #Exit the application

				raw_input('Press enter to go to next player')
				self.clear()


