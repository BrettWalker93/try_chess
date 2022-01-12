#import PySimpleGUI as sg
import sklearn as sk
import tkinter as tk

#   TODO:
#       finish (start) gui implementation

#modified FEN of starting position of chess, as an array {0 position, 1 "Whose Turn Is It?", 2 castling rights, 3 en passant (holy hell), 4 1/2 clock, 5 move number, 6 check}
startingPosition = ["rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR", "w", "KQkq", "e99", '0', "1", "n"]

def findLegalMoves(pos):
    
    #list of legal moves [(file, rank, file after, rank after, special), ...]
    moveset = []

    #nested loop iterates through rank (i) and file (j)
    i = 0
    for r in pos[0]:
        j = 0
        for z in r:
            #white
            if pos[1] == "w":

                if z == ("R"):
                    for m in findRookMoves(pos, i, j):
                        if (j == 7):
                            if (i == 0):
                                m[4] == 'rQ'
                            elif (i == 7):
                                m[4] == 'rK'
                        moveset.append(m)
                elif z == ("N"):
                    for m in findKnightMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("B"):
                    for m in findBishopMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("Q"):
                    for m in findQueenMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("K"):
                    for m in findWhiteKingMoves(pos, i, j):
                        moveset.append(m)
                    kingi = i
                    kingj = j
                elif z == ("P"):
                    for m in findWhitePawnMoves(pos, i, j):
                        moveset.append(m)

            #black
            elif pos[1] == "b":
                if z == ("r"):
                    for m in findRookMoves(pos, i, j):
                        if (j == 0):
                            if (i == 0):
                                m[4] = 'rq'
                            elif (i == 7):
                                m[4] = 'rk'
                        moveset.append(m)
                elif z == ("n"):
                    for m in findKnightMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("b"):
                    for m in findBishopMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("q"):
                    for m in findQueenMoves(pos, i, j):
                        moveset.append(m)
                elif z == ("k"):
                    for m in findBlackKingMoves(pos, i, j):
                        moveset.append(m)
                    kingi = i
                    kingj = j
                elif z == ("p"):
                    for m in findBlackPawnMoves(pos, i, j):
                        moveset.append(m)
            j = j +1
        i = i + 1
    
    #check check    
    for l in moveset:
        checkpos = pos.copy()
        checkpos[0] = pos[0].copy()
        checkpos = getNewPos(checkpos, l)
        if selfCheck(pos[1], l, kingi, kingj, checkpos):
            #print("Removing a self check")
            moveset.remove(l)
        checkpos.clear()

    return moveset

def findWhitePawnMoves(pos, i, j):
    
    #print("finding white pawn moves: " + str(i) + ", " + str(j))
    moveset = []

    #pawns on 2nd rank
    if i == 6:
        if canPawnMove("m2", pos, i-2, j): moveset.append([i, j, i-2, j, "e" + str(i-1) + str(j) + str(i-2) + str(j)])
    
    #capture right
    if j < 7:
        if canPawnMove("c", pos, i-1, j+1): moveset.append([i, j, i-1, j+1, ""])
    
    #capture left
    if j > 0:
        if canPawnMove("c", pos, i-1, j-1): moveset.append([i, j, i-1, j-1, ""])

    #promote
    if i == 1:
        if canPawnMove("m", pos, i-1, j):
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "N"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "B"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "Q"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "R"])
        return moveset

    #move forward 1 square
    if canPawnMove("m", pos, i-1, j): moveset.append([i, j, i-1, j, ""])

    #print("sending valid move count: " + str(len(moveset)))
    return moveset

def findBlackPawnMoves(pos, i, j):

    moveset = []

    #pawns on 7th rank
    if i == 1:
        if canPawnMove("m2", pos, i+2, j): moveset.append([i, j, i+2, j, "e" + str(i+1) + str(j) + str(i+2) + str(j)])

    #capture right
    if j < 7:
        if canPawnMove("c", pos, i+1, j+1): moveset.append([i, j, i+1, j+1, ""])
    #capture left
    if j > 0:
        if canPawnMove("c", pos, i+1, j-1): moveset.append([i, j, i+1, j-1, ""])

    #promote
    if i == 7:
        if canPawnMove("m", pos, i+1, j):
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "n"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "b"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "q"])
            moveset.append([i, j, i-1, j, "p" + str(i-j) + str(j) + "r"])
        return moveset

    #move forward 1 square
    if canPawnMove("m", pos, i+1, j): moveset.append([i, j, i+1, j, ""])

    return moveset

def findKnightMoves(pos, i, j):
    
    #print("finding knight moves: " + str(i) + ", " + str(j))
    moveset = []

    #target squares
    tmoveset = []

    #potential target squares
    pmoveset = [[i+1, j+2], [i-1, j+2], [i+1, j-2], [i-1, j-2], [i+2, j+1], [i-2, j+1], [i+2, j-1], [i-2, j-1]]

    #populate target squares
    for p in pmoveset:
        if not(p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1] < 0): tmoveset.append(p)

    for t in tmoveset:
        #print("checking a knight move" + str(t))
        if canOccupy(pos, t[0], t[1]): moveset.append([i, j, t[0], t[1], ""])

    #print("sending valid move count: " + str(len(moveset)))
    return moveset
    
def findRookMoves(pos, i, j):

    moveset = []

    #print("checking rook at: " + str(i) + ", "+ str(j))
   
    t = pos[1]

    #up
    ni = i
    nj = j
    while (ni > 0):
        ni = ni - 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break


    #down
    ni = i
    while (ni < 7):
        ni = ni + 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break

    #left
    ni = i
    while (nj > 0):
        nj = nj - 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break
    #right
    nj = j
    while (nj < 7):
        nj = nj + 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break

    return moveset

def findBishopMoves(pos, i, j):
    
    t = pos[1]

    moveset = []
    
    #topleft
    ni = i
    nj = j
    while (ni > 0 and nj > 0):
        ni = ni - 1
        nj = nj - 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break

    #topright
    ni = i
    nj = j
    while (ni < 7 and nj > 0):
        ni = ni + 1
        nj = nj - 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break 

    #botleft
    ni = i
    nj = j
    while (ni > 0 and nj < 7):
        ni = ni - 1
        nj = nj + 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break 

    #botright
    while (ni < 7 and nj < 7):
        ni = ni + 1
        nj = nj + 1
        p = pos[0][ni][nj]
        if p == '0':
            moveset.append([i, j, ni, nj, ''])
        elif p.islower():
            if t == 'w':
                moveset.append([i, j, ni, nj, ''])
            break
        elif p.isupper():
            if t == 'b':
                moveset.append([i, j, ni, nj, ''])
            break 

    return moveset

def findQueenMoves(pos, i, j):
    
    moveset = []

    for m in findBishopMoves(pos, i, j):
        moveset.append(m)

    for m in findRookMoves(pos, i, j):
        moveset.append(m)

    return moveset

def findWhiteKingMoves(pos, i, j):
    
    moveset = []

    #castle
    if 'K' in pos[2]:
        if pos[0][5][7] == '0' and pos[0][6][7] == '0':
            moveset.append([i, j, i+2, j, 'cK'])
    if 'Q' in pos[2]:
        if pos[0][1][7] == '0' and pos[0][2][7] == '0' and pos[0][3][7] == '0':
            moveset.append([i, j, i-3, j, 'cQ'])

    #normal move
    for m in range(-1, 2, 1):
        for n in range(-1, 2, 1):
            try:
                if pos[0][i+m][j+n] == '0' or pos[0][i+m][j+n].islower():
                    moveset.append([i, j, i+m, j+n, 'rB'])
            except IndexError:
                pass

    return moveset

def findBlackKingMoves(pos, i, j):
    
    moveset = []

    #castle
    if 'k' in pos[2]:
        if pos[0][5][0] == '0' and pos[0][6][0] == '0':
            moveset.append([i, j, i+2, j, 'ck'])
    if 'q' in pos[2]:
        if pos[0][1][0] == '0' and pos[0][2][0] == '0' and pos[0][3][0] == '0':
            moveset.append([i, j, i-3, j, 'cq'])

    #normal move
    for m in range(-1, 2, 1):
        for n in range(-1, 2, 1):
            try:
                if pos[0][i+m][j+n] == '0' or pos[0][i+m][j+n].isupper() and i+m >= 0:
                    moveset.append([i, j, i+m, j+n, 'rb'])
            except IndexError:
                pass

    return moveset

def fenToCoord(pos):

    arr = [[0 for i in range(8)] for j in range(8)]
    
    i = 0
    j = 0
    for l in pos:
        if i == 8:
            i = 0
            j = j + 1
        arr[j][i] = l
        i = i + 1    

    return arr

def canOccupy(pos, i, j):

    p = pos[0][i][j]

    #print("checking if can occupy [" + str(i) + ", " + str(j) + "] with piece: " + str(p))

    if p == '0':
        #print("can occupy: empty square")
        return True

    elif pos[1] == "w":
        if p.islower(): return True

    else:
        if p.isupper(): return True

    return False

def selfCheck(t, l, i, j, pos):
    
    #print("Self Check")
    #print(pos[0])

    #king move special case
    if len(l[4]) > 0:
        if l[4][0] == ('c' or 'r'):
            i = l[2]
            j = l[3]

    #check from the king's perspective whether it can be captured (eg could the king now move like a bishop to capture an opposing bishop)

    #pawns
    if t == 'w':
        #in bounds:
        if i > 1:
            #check right
            if j < 7:
                if pos[0][i-1][j-1] == 'p':
                    return True
            if j > 0:
                if pos[0][i-1][j+1] == 'p':
                    return True
    else:
        if i < 6:
            #check right
            if j < 7:
                if pos[0][i+1][j-1] == 'P':
                    #print("here1")
                    return True
            #check left
            if j > 0:
                if pos[0][i+1][j+1] == 'P':
                    #print("here2")
                    return True

    #rooks/queens
    ni = i
    nj = j
    #down
    while (nj < 7):
        nj = nj + 1
        p = pos[0][i][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'r' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'R' or p == 'Q':
                #print("here3")
                return True
            elif p.islower(): break
    #up
    nj = j
    while (nj > 0):
        nj = nj - 1
        p = pos[0][i][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'r' or p == 'q':
                return True
            elif p.isupper(): break

        elif t == 'b':
            if p == 'R' or p == 'Q':
                #print("here4")
                return True
            elif p.islower(): break
    #left
    nj = j
    while (ni > 0):
        ni = ni - 1
        p = pos[0][ni][j]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'r' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'R' or p == 'Q':
                #print("here6")
                return True
            elif p.islower(): break
    #right
    ni = i
    while (ni < 7):
        ni = ni + 1
        p = pos[0][ni][j]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'r' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'R' or p == 'Q':
                #print("here5")
                return True
            elif p.islower(): break

    #bishops/queens
    #topleft
    ni = i
    nj = j
    while (ni > 0 and nj > 0):
        ni = ni - 1
        nj = nj - 1
        p = pos[0][ni][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'b' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'B' or p == 'Q':
                return True
            elif p.islower(): break
    #topright
    ni = i
    nj = j
    while (ni < 7 and nj > 0):
        ni = ni + 1
        nj = nj - 1
        p = pos[0][ni][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'b' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'B' or p == 'Q':
                return True
            elif p.islower(): break
    #botleft
    ni = i
    nj = j
    while (ni > 0 and nj < 7):
        ni = ni - 1
        nj = nj + 1
        p = pos[0][ni][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'b' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'B' or p == 'Q':
                #print("here9")
                return True
            elif p.islower(): break
    #botright
    ni = i
    nj = j
    while (ni < 7 and nj < 7):
        ni = ni + 1
        nj = nj + 1
        p = pos[0][ni][nj]
        if p == '0':
            pass
        elif t == 'w':
            if p == 'b' or p == 'q':
                return True
            elif p.isupper(): break
        elif t == 'b':
            if p == 'B' or p == 'Q':
                #print("here10")
                return True
            elif p.islower(): break

    #knights
    #candidates

    #tArget moveset
    amoveset = []
    #potential moveset
    pmoveset = [[i+1, j+2], [i-1, j+2], [i+1, j-2], [i-1, j-2], [i+2, j+1], [i-2, j+1], [i+2, j-1], [i-2, j-1]]

    #populate tArget squares
    for p in pmoveset:
        if not(p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1] < 0): amoveset.append(p)

    #check if knight-king could capture a knight in tArget
    for a in amoveset:
        if (t == 'w' and pos[0][a[0]][a[1]] == 'n'):
            return True
        elif (t == 'b' and pos[0][a[0]][a[1]] == 'N'):
            return True

    #opposing kings
    for m in range(-1, 2, 1):
        for n in range(-1, 2, 1):
            try:
                p = pos[0][i+m][i+n]

                if t == 'w':
                    if p == 'k':
                        return True
                elif t == 'b':
                    if p == 'K':
                        print("here11")
                        return True
            except IndexError:
                pass

    #print("Self Check End")
    #print(pos[0])

    return False

def canPawnMove(s, pos, i, j):

    p = pos[0][i][j]

    if pos[1] == "w":
        if s == "m":
            if p == '0': return True 
        elif s == "m2":
            if p == '0' and pos[0][i+1][j] == '0': return True 

        else:
            #print("checking capture: " + str(i) + ", " + str(j) + str(p))
            if (pos[3][0] == i and pos[3][1] == j):
                return True
            elif p == '0': 
                return False
            elif p.islower(): return True
    elif pos[1] == "b":
        if s == "m":
            if p == '0': return True 
        elif s == "m2":
            if p == '0' and pos[0][i-1][j] == '0': return True 

        else:
            if (pos[3][0] == i and pos[3][1] == j):
                return True
            elif p == '0': return False
            elif p.isupper(): return True

    return False

def getNewPos(pos, move):

    #move: (start i, start j, end i, end j, special)

    #print("making move")

    newPos = []
    newPos.append([])
    #position
    for r in pos[0]:
        newPos[0].append(r.copy())

    #whose turn is it
    if pos[1] == 'w':
        newPos.append('b')
    else: newPos.append('w')

    #castling rights
    newPos.append(pos[2])

    #en passant
    newPos.append("e99")

    #halfclock
    newPos.append("0")

    #movenumber
    newPos.append("1")

    #check
    newPos.append("n")

    #print("New Pos")
    #print(newPos[0])

    #clear current spot and occupy new spot
    newPos[0][move[2]][move[3]] = newPos[0][move[0]][move[1]]
    newPos[0][move[0]][move[1]] = '0'

    #special
    sp = newPos[3] #ex: 'e0203' for en passant on a6
    #check for and do ep capture
    if (sp[1] == move[2] and sp[2] == move[3]):
        newPos[0][sp[3]][sp[4]] = '0'


    s = move[4]
    if len(s) > 0:
        #'cK' or 'rK' or 'rB' for white kingside castle or white losing kingside castle rights or all castle rights respectively
        #castle rights
        if (s[0] == 'r' and not(newPos[2] == '')):
            if s[1] == 'B':
                newPos[2].replace('K', '')
                newPos[2].replace('Q', '')

            elif s[1] == 'b':
                newPos[2].replace('k', '')
                newPos[2].replace('q', '')

            else:
                newPos[2].replace(s[1], '')

        #castle
        elif s == 'cK':
            newPos[0][5][7] = 'R'
            newPos[0][7][7] = '0'
            newPos[2].replace('K', '')
            newPos[2].replace('Q', '')
        elif s == 'cQ':
            newPos[0][3][7] = 'R'
            newPos[0][0][7] = '0'
            newPos[2].replace('K', '')
            newPos[2].replace('Q', '')
        elif s == 'ck':
            newPos[0][5][0] = 'r'
            newPos[0][7][0] = '0'
            newPos[2].replace('k', '')
            newPos[2].replace('q', '')
        elif s == 'cq':
            newPos[0][3][0] = 'r'
            newPos[0][0][0] = '0'
            newPos[2].replace('k', '')
            newPos[2].replace('q', '')

        #add new ep
        if s[0] == 'e':
            newPos[3] = s[0:3]

        #pawn promotion
        if s[0] == 'p':
            newPos[0][int(s[1])][int(s[2])] = s[3]
    
    #print("New Pos End")
    #print(newPos[0])
    
    return newPos

def testMain():

    myPos = [fenToCoord("rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR"), "w", "KQkq", "e99", '0', "1", "n"]

    cmd = ""
    
    while cmd != "off":
        print(myPos)
        i = 1
        ml = []
        for m in findLegalMoves(myPos):
            print(str(i) + ": " + str(m))
            i = i + 1
            ml.append(m)

        print("Current Position")
        print(myPos)

        cmd = input("do it: ")

        if cmd.isdigit():
            print ("doing move: " + str(ml[int(cmd) - 1]))
            myPos = getNewPos(myPos, ml[int(cmd) - 1])

    return 0

testMain()

#----------------GUI---------------------

#construct gui
def gmain(pos):

    sg.Window(title="How to Chess?", layout=[[]], margins=(100, 50)).read()
    
    return None


def guiTestMain():
    myPos = [fenToCoord("rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR"), "w", "KQkq", "e99", '0', "1", "n"]

    ml = []

    cmd = ""

    boardWindow = tk.Tk()

    boardWindow.title = "Bortbortbort GUI"
    boardWindow.rowconfigure(0, minsize=800, weight=1)
    boardWindow.columnconfigure(1, minsize=800, weight=1)

    moveEntry = tk.Entry()

    listButton = tk.Button(
        text = "Get List",
    )

    enterButton = tk.Button(
        text = "Enter",
    )

    listButton.bind("<Button-1>", )
    
    enterButton.bind("<Button-1>", handleEnterClick())

    for i in range(8):
        for j in range(8):
            frame = tk.Frame(
                master = boardWindow,
                borderwidth = 1
            )

            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                frame.bg = "#035aa1"

            else:
                frame.bg = "#03b6fc"

            frame.grid(row = i, column = j)
            label = tk.Label(master = frame, text = str(myPos[0][i][j]))
            label.pack()

    boardWindow.mainloop()

    return 0

def handleEnterClick():

    return 0

#guiTestMain()