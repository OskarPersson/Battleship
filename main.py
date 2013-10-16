import os
import sys
import battlefield
import bombfield
import ship
import player

clear = lambda : os.system('tput reset')
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
    if("A" <= column <= "J"):
        return True
    else:
        return False

def rowExist(row):
    if(1 <= row <= 10):
        return True
    else:
        return False
    
def printField(f):
    
    l = [' ', 'A','B','C','D','E','F','G','H','I','J']
    spacing = ' '.join(['{:<2}'] * len(l))
    print spacing.format(*l)

    for v in range(1,len(l)):
        print spacing.format(v, f['A'][v],f['B'][v],f['C'][v],f['D'][v] ,f['E'][v] ,f['F'][v] ,f['G'][v] ,f['H'][v] ,f['I'][v],f['J'][v])

def placeShips(player):
    counter = 1
    #instructions
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
        while columnExist(column) == False or row not in rowlist or cellBusy == True:
            userInput = raw_input(player.name + ", in which cell (A-J)(1-10) do you want to place your " + nth[counter] + " ship?\n")
            if (len(userInput) < 2):
                column = ""
                row = ""
            else:
                column = userInput[0].upper()        
                row = userInput[1]
                if len(userInput) == 3:     
                    row += userInput[2]
            if(columnExist(column) and row in rowlist):
                cellBusy = pff[column][int(row)]
        
        row = int(row)
        newrow = row
        newcolumn = column
        
        while (direction != "right" and direction != "left" and direction != "up" and direction != "down") or rowExist(newrow) == False or columnExist(newcolumn) == False or occupied == True:
            direction = raw_input(player.name + ", in what direction (right, left, up or down) is your " + nth[counter] + " ship turned?\n")
            occupied = False    
            partCounter = 0

            for y in range(len(x.parts)):
                newcolumn = column
                newrow = row
                if(direction == "down"):
                    newrow = row + partCounter
                    
                elif (direction == "up"):
                    newrow = row - partCounter
                    
                elif (direction == "left"):
                    newcolumn = chr(ord(column) - partCounter)
                    
                elif(direction == "right"):
                    newcolumn = chr(ord(column) + partCounter)
                    
                partCounter += 1
                if columnExist(newcolumn) and rowExist(newrow):
                    if(pff[newcolumn][newrow] == True):
                        occupied = True


            if(direction == "down"):
                newrow = row + len(x.parts) - 1
            elif (direction == "up"):
                newrow = row - len(x.parts)
            elif (direction == "left"):
                newcolumn = chr(ord(column) - len(x.parts)+1)
            elif(direction == "right"):
                newcolumn = chr(ord(column) + len(x.parts))
            
        
        
        newrow = row
        newcolumn = column
        partCounter = 0
        for y in range(len(x.parts)):
            if(direction == "down"):
                newrow = row + partCounter
                pff[column][newrow] = True
            elif (direction == "up"):
                newrow = row - partCounter
                pff[column][newrow] = True
            elif (direction == "left"):
                newcolumn = chr(ord(column) - partCounter)
                pff[newcolumn][row] = True
            elif(direction == "right"):
                newcolumn = chr(ord(column) + partCounter)
                pff[newcolumn][newrow] = True
            partCounter += 1

        clear()
        printField(player.field.field)
        counter += 1

def newPlayer(n, ships, field, bombfield):
    newName = raw_input("Player " + str(n) + ", what's your name?\n")
    while newName == "":
        newName = raw_input("Please, enter something\n")
    clear()
    p = player.Player(newName, ships[:], field, bombfield)

    placeShips(p)
    return p

def anythingLeft(d):
    newList = []
    def myprint(d):
        for k, v in d.iteritems():
            if isinstance(v, dict):
              myprint(v)
            else:
              newList.append(bool(v))
    myprint(d)
    return True in newList

def bomb(player, enemy):
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
    if(eff[column][row] == True):
        print "Hit!"
        eff[column][row] = False
        player.bombfield.field[column][row] = 'X'
        if anythingLeft(enemy.field.field) == False:
            print(player.name + " wins!")
            sys.exit()
    else:
        print "Miss!"
        player.bombfield.field[column][row] = 'O'
    printField(player.bombfield.field)
    raw_input('Press enter to go to next player')
    clear()



### BATTLEFIELD ###
p1Field = battlefield.Battlefield()
p2Field = battlefield.Battlefield()
p1BombField = bombfield.Bombfield()
p2BombField = bombfield.Bombfield()


### SHIPS ###
ships = [];
ships.append(ship.Ship(5))
ships.append(ship.Ship(4))
ships.append(ship.Ship(3))
ships.append(ship.Ship(3))
ships.append(ship.Ship(2))

### PLAYER ###

p1 = newPlayer(1, ships[:], p1Field, p1BombField)
raw_input('Press enter to go to next player')
clear()
p2 = newPlayer(2, ships[:], p2Field, p2BombField)
raw_input('Press enter to go to next player')
clear()


while anythingLeft(p1.field.field) == True and anythingLeft(p2.field.field):
    bomb(p1, p2)
    if anythingLeft(p1.field.field) == True and anythingLeft(p2.field.field):
        bomb(p2, p1)





