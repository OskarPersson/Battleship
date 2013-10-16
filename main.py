import os
import sys
import battlefield
import bombfield
import ship
import player

clear = lambda : os.system('tput reset') #Clears the screen, instead of 'clear' which just adds new lines
clear()

nth = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth"
}

rowlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

def columnExist(column):
    if("A" <= column <= "J"): #is the column A-J?
        return True
    else:
        return False

def rowExist(row):
    if(1 <= row <= 10): #is the row 1-10?
        return True
    else:
        return False
    
def printField(f):
    
    l = [' ', 'A','B','C','D','E','F','G','H','I','J']
    spacing = ' '.join(['{:<2}'] * len(l)) #creates a string with len(l)-numbers of '{:<2}' with a space between each one
    print spacing.format(*l) #prints the header (column names) with a spacing of 2

    for v in range(1,len(l)):
        print spacing.format(v, f['A'][v],f['B'][v],f['C'][v],f['D'][v] ,f['E'][v] ,f['F'][v] ,f['G'][v] ,f['H'][v] ,f['I'][v],f['J'][v]) #Adds all the rows with the row number to the left and a spacing of 2

def placeShips(player):
    counter = 1
    #player instructions
    print player.name + ", you have 10x10 cells where you can place your ships,\n"
    print "Remember not to tell your opponent where you place your ships\n"
    print "Then you say which direction the ship is turned (right, left, up or down)\n"

    printField(player.field.field)

    #place ships
    for x in player.ships:
        column = ""
        row = ""
        direction = ""
        cellBusy = True
        pff = player.field.field
        while columnExist(column) == False or row not in rowlist or cellBusy == True: #loop until the user enters a valid cell
            userInput = raw_input(player.name + ", in which cell (A-J)(1-10) do you want to place your " + nth[counter] + " ship?\n") #user input for cell
            if (len(userInput) >= 2): #user input must be atleast 2 characters
                column = userInput[0].upper()
                row = userInput[1]
                if len(userInput) >= 3: #since there is 10 rows, grab the third enter character too 
                    row += userInput[2]
            if(columnExist(column) and row in rowlist): #If the column and row is valid, check if the cell is busy
                cellBusy = pff[column][int(row)]
        
        row = int(row)
        newrow = row
        newcolumn = column
        
        while (direction != "right" and direction != "left" and direction != "up" and direction != "down") or rowExist(newrow) == False or columnExist(newcolumn) == False or cellBusy == True: #loop until the user enters a valid direction
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
                if columnExist(newcolumn) and rowExist(newrow):
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


        clear()
        printField(player.field.field)
        counter += 1

def newPlayer(n, ships, field, bombfield): #Creates a new player with the player number, ships, field and bombfield
    newName = raw_input("Player " + str(n) + ", what's your name?\n")
    while newName == "":
        newName = raw_input("Please, enter something\n")
    clear()
    p = player.Player(newName, ships[:], field, bombfield)

    placeShips(p)
    return p #Returns the player object

def anythingLeft(d): #Checks if there is any ships left
    newList = []
    def myprint(d):
        for k, v in d.iteritems():
            if isinstance(v, dict): #If v is a dict, call the function with that dict
              myprint(v)
            else:
              newList.append(v) #Else, add v (False/True) to the dict
    myprint(d)
    return True in newList #Returns True if there is a True in the list, else return False

def bomb(player, enemy): #Gives the current player a change to bomb the sent enemy
    column = ""
    row = ""
    eff = enemy.field.field 

    printField(player.bombfield.field)

    while columnExist(column) == False or row not in rowlist:
        userInput = raw_input(player.name + ", in which cell (A-J)(1-10) do you want to bomb your enemy?\n")
        
        if (len(userInput) < 2):
            column = ""
            row = ""
        else:
            column = userInput[0].upper()
            row = userInput[1]
            if len(userInput) == 3:     
                row += userInput[2]

    row = int(row)
    clear()
    if(eff[column][row] == True): #if there is a ship at the cell, set an x in the bombfield
        print "Hit!"
        eff[column][row] = False
        player.bombfield.field[column][row] = 'X'
        if anythingLeft(eff) == False: #Does the enemy have any ships left?
            print(player.name + " wins!")
            sys.exit() #Exit the application
    elif(eff[column][row] == False and player.bombfield.field[column][row] != 'X'): #If empty cell and not hit
        print "Miss!"
        player.bombfield.field[column][row] = 'O'
    printField(player.bombfield.field)
    raw_input('Press enter to go to next player')
    clear()



### CREATE BATTLEFIELDS ###
p1Field = battlefield.Battlefield()
p2Field = battlefield.Battlefield()
p1BombField = bombfield.Bombfield()
p2BombField = bombfield.Bombfield()


### CREATE SHIPS ###
ships = [];
ships.append(ship.Ship(5))
ships.append(ship.Ship(4))
ships.append(ship.Ship(3))
ships.append(ship.Ship(3))
ships.append(ship.Ship(2))

### CREATE PLAYERS ###

p1 = newPlayer(1, ships[:], p1Field, p1BombField)
raw_input('Press enter to go to next player')
clear()
p2 = newPlayer(2, ships[:], p2Field, p2BombField)
raw_input('Press enter to go to next player')
clear()


while anythingLeft(p1.field.field) and anythingLeft(p2.field.field): #While ships left, keep playing
    bomb(p1, p2)
    if anythingLeft(p1.field.field) and anythingLeft(p2.field.field):
        bomb(p2, p1)





