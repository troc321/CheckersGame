import time
import copy
import random
import turtle
import P1
import P2

PRINT_DEBUG=False
DELAY=.5

def drawFilledSquare(t,sideLength,color):
    t.color(color)
    t.begin_fill()
    for x in range(4):
        t.forward(sideLength)
        t.left(90)
    t.end_fill()

def drawCheckerRow(tu,length,color1,color2):
    for ct in range(4):
        drawFilledSquare(tu,length,color1)
        tu.forward(length)
        drawFilledSquare(tu,length,color2)
        tu.forward(length)

def positionTurtlefForNextRow(t1):
    t1.up()
    t1.backward(8)
    t1.left(90)
    t1.forward(1)
    t1.right(90)
    t1.down()

def drawChecker(t,wn,row,col,color,ringColor,board,isKing):
    if (color=="black" and row==0) or (color=="red" and row==7) or isKing:
        board[row][col]=color[0].upper()
    else:
        board[row][col]=color[0]
    wn.tracer(False)
    t.color("black",color)
    t.begin_fill()
    t.up()
    t.goto(col+.5,row)
    t.down()
    t.circle(.48)
    t.end_fill()
    t.color(ringColor)
    for size in range(1,5):
        t.up()
        t.goto(col+.5,row+(.5-(size*.1)-.02))
        t.down()
        t.circle(size*.1)
    if board[row][col] in ["B","R"]:
        t.up()
        t.goto(col+.25,row+.58)
        t.down()
        t.setheading(0)
        t.color("yellow")
        t.begin_fill()
        for i in range(5):
            t.forward(.5)
            t.right(144)
        t.end_fill()
    wn.tracer(True)

def drawLabel(t,wn,row,col):
    wn.tracer(False)
    t.up()
    t.color("white","white")
    t.goto(col+.81,row+1.03)
    t.write(chr(row+65)+str(col), font=("courier new",10,"bold"))
    wn.tracer(True)

def setupBoard():
    wn=turtle.Screen()
    wn.setworldcoordinates(-1,9,9.5,-1)
    t=turtle.Turtle()
    wn.tracer(False)
    for i in range(4):
        drawCheckerRow(t,1,"red","gray")
        positionTurtlefForNextRow(t)
        drawCheckerRow(t,1,"gray","red")
        positionTurtlefForNextRow(t)
    for row in range(8):
        for col in range(8):
            if (row+col)%2==1:
                drawLabel(t,wn,row,col)
    wn.tracer(True)
    t.hideturtle()
    row=[""]*8
    board=[]
    for i in range(8):
        board.append(row[:])
    return t,wn,board

def newGame(t,wn,board):
    for row in range(0,3):
        for col in range(8):
            if (row+col)%2==1:
                board[row][col]="r"
                drawChecker(t,wn,row,col,"red","gray",board,False)
    for row in range(5,8):
        for col in range(8):
            if (row+col)%2==1:
                board[row][col]="b"
                drawChecker(t,wn,row,col,"black","gray",board,False)
    if random.randint(0,1)==0:
        currentPlayer="black"
        opposingPlayer="red"
        forwardRowInc=-1
        currentPlayerTokens=['b','B']
        opposingPlayerTokens=['r','R']
    else:
        currentPlayer="red"
        opposingPlayer="black"
        forwardRowInc=1
        currentPlayerTokens=['r','R']
        opposingPlayerTokens=['b','B']
    return currentPlayer,opposingPlayer,currentPlayerTokens,opposingPlayerTokens,forwardRowInc

def showLogicalBoard(board):
    print("Board State")
    index=0
    print ("  01234567")
    for row in board:
        print(chr(index+65)+" ",end="")
        index+=1
        for col in row:
            if col=="":
                print("-",end="")
            else:
                print(col,end="")
        print()
    print()

def switchPlayer(currentPlayer):
    if currentPlayer=="black":
        currentPlayer="red"
        opposingPlayer="black"
        forwardRowInc=1
        currentPlayerTokens=['r','R']
        opposingPlayerTokens=['b','B']
    else:
        currentPlayer="black"
        opposingPlayer="red"
        forwardRowInc=-1
        currentPlayerTokens=['b','B']
        opposingPlayerTokens=['r','R']
    return currentPlayer,currentPlayerTokens,opposingPlayer,opposingPlayerTokens,forwardRowInc

def removeChecker(t,wn,fromRow,fromCol,board):
    wn.tracer(False)
    board[fromRow][fromCol]=""
    t.up()
    t.goto(fromCol,fromRow)
    drawFilledSquare(t,1,"gray")
    t.color("white")
    drawLabel(t,wn,fromRow,fromCol)
    wn.tracer(True)

def parseValidMove(move):
    fromRow=ord(move[0])-65
    fromCol=int(move[1])
    toRow=ord(move[3])-65
    toCol=int(move[4])
    move=move[3:]
    return move,fromRow,fromCol,toRow,toCol

#function to return a list of all valid moves for the current player
def listValidMoves(board,currentPlayerTokens,rowInc):
    validMovesList=[]
    for row in range(8):
        for col in range(8):
            if board[row][col] in currentPlayerTokens:
                if board[row][col] in ['r','b']: #regular checkers
                    for colInc in [1,-1]:
                        if row+rowInc>=0 and row+rowInc <=7 \
                           and col+colInc>=0 and col+colInc<=7 \
                           and board[row+rowInc][col+colInc]=="":
                            validMovesList.append(chr(row+65)+str(col)+":"+chr(row+rowInc+65)+str(col+colInc))
                else: #king
                    for rInc in [1,-1]:
                        for cInc in [-1,1]:
                            if (col+cInc)>=0 and (col+cInc)<=7 \
                              and (row+rInc)>=0 and (row+rInc)<=7 \
                              and board[row+rInc][col+cInc]=="":
                                validMovesList.append(chr(row+65)+str(col)+":"+chr(row+rInc+65)+str(col+cInc))                       
    return validMovesList


#function to return a list of all valid jumps for the current player
def listValidSingleJumps(board,currentPlayerTokens,rowInc,opposingPlayerTokens): #Not finished
    validSingleJumpsList=[]
    for row in range(8):
        for col in range(8):
            if board[row][col] in currentPlayerTokens:
                if board[row][col] in ['r','b']: #regular cheecker
                    for colInc in [1,-1]:
                        if row+rowInc*2>=0 and row+rowInc*2<=7 and \
                           col+colInc*2>=0 and col+colInc*2<=7 and \
                           board[row+rowInc][col+colInc] in opposingPlayerTokens and \
                           board[row+(2*rowInc)][col+(2*colInc)]=='' : 
                            validSingleJumpsList.append(chr(row+65)+str(col)+":"+chr(row+2*rowInc+65)+str(col+colInc*2))
                else: #king checker
                    for rInc in [1,-1]:
                        for cInc in [-1,1]:
                            if (col+cInc)>=0 and (col+cInc)<=7 and \
                               (row+rInc)>=0 and (row+rInc)<=7 and \
                               board[row+rInc][col+cInc] in opposingPlayerTokens and \
                               (col+2*cInc)>=0 and (col+2*cInc)<=7 \
                               and row+(2*rInc)>=0 and row+(2*rInc)<=7 \
                               and board[row+(2*rInc)][col+(2*cInc)]=='' : 
                                validSingleJumpsList.append(chr(row+65)+str(col)+":"+chr(row+(2*rInc)+65)+str(col+(2*cInc)))                            
    return validSingleJumpsList

def expandJumps(board,player,oldJumps,playerTokens,opponentTokens,rowInc):
    VALID_RANGE=range(8)
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ['R','B']: #not a king
            for colInc in [1,-1]:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=="":
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in [1,-1]:
                for newRowInc in [1,-1]:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=="" or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps 

def oldGame(t,wn,board,gameName):
    outFile=open(gameName,"r")
    currentPlayer=outFile.readline()[:-1]
    currentPlayer,currentPlayerTokens,opposingPlayer,opposingPlayerTokens,forwardRowInc=switchPlayer(currentPlayer)
    currentPlayer,currentPlayerTokens,opposingPlayer,opposingPlayerTokens,forwardRowInc=switchPlayer(currentPlayer)
    lstLines=outFile.readlines()
    for row in range(len(lstLines)):
        for col in range(len(lstLines[row])-1):
            if (row+col)%2==1 and lstLines[row][col] != 'e':
                if lstLines[row][col] in ["b","B"]:
                    color="black"
                else:
                    color="red"
                if lstLines[row][col] in ['R','B']:
                    isKing=True
                else:
                    isKing=False
                drawChecker(t,wn,row,col,color,"gray",board, isKing)
    return currentPlayer,opposingPlayer,currentPlayerTokens,opposingPlayerTokens,forwardRowInc

def win(board):
    rCount=0
    bCount=0
    for row in board:
        for col in row:
            if col in ['r','R']:
                rCount+=1
            elif col in ['b','B']:
                bCount+=1
    if PRINT_DEBUG:print("Red on board",rCount,"    Black on board",bCount)
    if rCount==0:
        return [True,"black"]
    if bCount==0:
        return [True,"red"]
    return [False,""]

def saveGame(board,currentPlayer):
    answer=input("Enter file name to save game, or hit enter to quit => ")
    if answer != "":
        outFile=open(answer,"w")
        outFile.write(currentPlayer+"\n")
        for row in board:
            outRow=""
            for token in row:
                if token=="":
                    outRow=outRow+"e"
                else:
                    outRow=outRow+token
            outFile.write(outRow+"\n")
        outFile.close()

def checkMove(board,player,currentPlayerTokens,forwardRowInc,opposingPlayerTokens):
    #print("IN CHECK MOVE IN MAIN")
    validMovesList=listValidMoves(board,currentPlayerTokens,forwardRowInc)
    #showLogicalBoard(board)    
    #print("valid moves list from main:",validMovesList)
    validSingleJumpsList=listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
    oldJumpsList=validSingleJumpsList[:]
    expandedJumpsList=expandJumps(board,player,oldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    while expandedJumpsList != oldJumpsList:
        oldJumpsList=expandedJumpsList[:]
        expandedJumpsList=expandJumps(board,player,oldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    return expandedJumpsList,validMovesList

def checkers():
    t,wn,board=setupBoard()
    gameName=input("Press enter to start a new game, otherwise, type in the name of an old game => ") 
    if gameName!="":
        currentPlayer,opposingPlayer,currentPlayerTokens,opposingPlayerTokens,forwardRowInc=oldGame(t,wn,board,gameName)
    else:
        currentPlayer,opposingPlayer,currentPlayerTokens,opposingPlayerTokens,forwardRowInc=newGame(t,wn,board)
    boardCopy=copy.deepcopy(board)
    if currentPlayer=="red":
        start=time.time()
        move=P2.getValidPlayerAction(PRINT_DEBUG,currentPlayer,currentPlayerTokens,opposingPlayerTokens,boardCopy,forwardRowInc)
        stop=time.time()
        if PRINT_DEBUG:print("TIME:",stop-start)
        js,mvs=checkMove(board,currentPlayer,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
        #print("RED MOVES:",mvs)
        #print("RED JUMPS:",js)
        #print("MOVE SELECTED:",move)
        if js!=[]:
            if move not in js:
                print("You must take a jump!  You lose, red!")
                exit()
        else:
            if move not in mvs and mvs!=[]:
                print("You must take a jump!  You lose, red!")
                exit()                
    else:
        start=time.time()
        move=P1.getValidPlayerAction(PRINT_DEBUG,currentPlayer,currentPlayerTokens,opposingPlayerTokens,boardCopy,forwardRowInc)        
        stop=time.time()
        if PRINT_DEBUG:print("TIME:",stop-start)
        js,mvs=checkMove(board,currentPlayer,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
        #print("BLACK MOVES:",mvs)
        #print("BLACK JUMPS:",js)
        #print("MOVE SELECTED:",move)
        if js!=[]:
            if move not in js:
                print("You must take a jump!  You lose, black!")
                exit()
        else:
            if move not in mvs and mvs!=[]:
                print("You must take a jump!  You lose, black!")
                exit()                
    while move != "QUIT" and not win(board)[0]:
        while len(move)>=5:
            move,fromRow,fromCol,toRow,toCol=parseValidMove(move)
            if board[fromRow][fromCol] in ['R','B']:
                isKing=True
            else:
                isKing=False
            time.sleep(DELAY)
            removeChecker(t,wn,fromRow,fromCol,board)
            time.sleep(DELAY)
            drawChecker(t,wn,toRow,toCol,currentPlayer,"gray",board,isKing)
            time.sleep(DELAY)
            if abs(fromRow-toRow)>1: #Jump is occuring
                removeChecker(t,wn,(fromRow+toRow)//2,(fromCol+toCol)//2,board)
        boardCopy=copy.deepcopy(board)
        currentPlayer,currentPlayerTokens,opposingPlayer,opposingPlayerTokens,forwardRowInc=switchPlayer(currentPlayer)
        if currentPlayer=="red":
            start=time.time()
            move=P2.getValidPlayerAction(PRINT_DEBUG,currentPlayer,currentPlayerTokens,opposingPlayerTokens,boardCopy,forwardRowInc)
            stop=time.time()
            if PRINT_DEBUG:print("TIME:",stop-start)
            js,mvs=checkMove(board,currentPlayer,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
            #print("RED MOVES:",mvs)
            #print("RED JUMPS:",js)
            #print("MOVE SELECTED:",move)
            if js!=[]:
                if move not in js:
                    print("You must take a jump!  You lose, red!")
                    exit()
            else:
                if move not in mvs and mvs!=[]:
                    print("You must take a jump!  You lose, red!")
                    exit()             
        else:
            start=time.time()
            move=P1.getValidPlayerAction(PRINT_DEBUG,currentPlayer,currentPlayerTokens,opposingPlayerTokens,boardCopy,forwardRowInc)        
            stop=time.time()
            if PRINT_DEBUG:print("TIME:",stop-start)
            js,mvs=checkMove(board,currentPlayer,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
            #print("BLACK MOVES:",mvs)
            #print("BLACK JUMPS:",js)
            #print("MOVE SELECTED:",move)
            if js!=[]:
                if move not in js:
                    print("You must take a jump!  You lose, black!")
                    exit()
            else:
                if move not in mvs and mvs!=[]:
                    print("You must take a jump!  You lose, black!")
                    exit()                
    if move=="QUIT":
        saveGame(board,currentPlayer)

checkers()
