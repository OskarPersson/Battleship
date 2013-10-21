
mode = ''
while mode != 'l' and mode != 'n':
    mode = raw_input('[l] Local or [n] Network?\n');


### CREATE PLAYERS ###
if mode == 'l':
    import game

    g = game.Game()

    g.p1 = g.newPlayer(1, g.ships[:], g.p1Field, g.p1BombField)
    raw_input('Press enter to go to next player')
    g.clear()
    
    g.p2 = g.newPlayer(2, g.ships[:], g.p2Field, g.p2BombField)
    raw_input('Press enter to go to next player')
    g.clear()

    g.start()
else:
    sc = ''
    while sc != 's' and sc != 'c':
        sc = raw_input('[s] Server or [c] Client?\n');
    if sc == 's':
        import server
        s = server.Server()
        s.connect()

    else:
        import client
        
        c = client.Client()