import random

"""
1) If a move to the King row with a regular checker is available, take it so
the checker will become a King
2) If a move to a side square is available, take it
3) If a jump to a King row with a regular checker is available, take it so
the checker will become a king
4) If multiple jumps are available, take the longest jump.  If all jumps are
equal length, take the jump that lands closest to the opposing home row.
5) A heuristic of your own choosing
"""

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

#Heuristic 1
def MoveRegularCheckerToKingRow(validMovesList,kingRow,board):
    move=""
    choiceList=[]
    for possible in validMovesList:
        if int(ord(possible[3])-65)==kingRow and board[ord(possible[0])-65][int(possible[1])] in ['r','b']:
            choiceList.append(possible)
    if choiceList!=[]:
        move=choiceList[random.randrange(len(choiceList))]
    return move

#Heuristic 2
def MoveAnyToSideSquare(validMovesList):
    move=""
    choiceList=[]
    for possible in validMovesList:
        if int(possible[4])==0 or int(possible[4])==7:
            choiceList.append(possible)
    if choiceList!=[]:
        move=choiceList[random.randrange(len(choiceList))]
    return move

#Heuristic 3
def JumpToKingRowRegularChecker(expandedJumpsList,kingRow,board):
    jump=""
    choiceList=[]
    for possible in expandedJumpsList:
        if int(ord(possible[-2])-65)==kingRow and board[ord(possible[0])-65][int(possible[1])] in ['r','b']:
            choiceList.append(possible)
    if choiceList!=[]:
        jump=choiceList[random.randrange(len(choiceList))]
    return jump

#Heuristic 4
def JumpTakeLongestOrFurthest(expandedJumpsList,kingRow):
    jump=""
    choiceList=[]
    if expandedJumpsList!=[]:
        #Check for longest
        maxLen=len(expandedJumpsList[0])
        for item in expandedJumpsList:
            if len(item)>maxLen:
                maxLen=len(item)
        for item in expandedJumpsList:
            if len(item)==maxLen:
                choiceList.append(item)
        if len(choiceList)!=1:
            minDist=abs(ord(expandedJumpsList[0][-2])-65-kingRow)
            for item in expandedJumpsList:
                if abs(ord(item[-2])-65-kingRow)<minDist:
                    minDist=abs(ord(item[-2])-65-kingRow)
            for item in expandedJumpsList:
                if abs(ord(item[-2])-65-kingRow)==minDist:
                    choiceList.append(item)
        if choiceList!=[]:
            jump=choiceList[random.randrange(len(choiceList))]
    return jump

#4 NEW HURISTICS:

# 5: This function allows the current player to prioritize blocking an available jump by the opposing player either through moving or jumping
def blockJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    
    otherOldJumpsList = listValidSingleJumps(board,opposingPlayerTokens,-1*(forwardRowInc),currentPlayerTokens) 
    otherJumps = expandJumps(board,player,otherOldJumpsList,opposingPlayerTokens,currentPlayerTokens,-1*(forwardRowInc))
    
    for jump in otherJumps:
        for move in myMoves:
            if (jump[-2] + jump[-1]) == (move[-2] + move[-1]):
                return move
            
    for jump in otherJumps:
        for jumps in myJumps:
            if (jump[-2] + jump[-1]) == (jumps[-2] + jumps[-1]):
                return jumps
            
    return ''

# 6: This function will disallow the current player's checker to move to the same place another opposing checker can move/jump to
def noMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    
    otherMoves = listValidMoves(board,opposingPlayerTokens,-1*(forwardRowInc)) 
    otherOldJumpsList = listValidSingleJumps(board,opposingPlayerTokens,-1*(forwardRowInc),currentPlayerTokens) 
    otherJumps = expandJumps(board,player,otherOldJumpsList,opposingPlayerTokens,currentPlayerTokens,-1*(forwardRowInc))

    #if two moves move to the same to spot            
    for otherMove in otherMoves:
        for myMove in myMoves:
            if (otherMove[-2] + otherMove[-1]) == (myMove[-2] + myMove[-1]):
                if len(myMoves) == 1:
                    return ''
                else:
                    myMoves.remove(myMove)
                    return myMoves[0]
    return ''

# 7: This function will prioritize the current player's checker to jump to the same place another opposing checker can jump to in order to create a block
def idealJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    
    otherMoves = listValidMoves(board,opposingPlayerTokens,-1*(forwardRowInc)) 
    otherOldJumpsList = listValidSingleJumps(board,opposingPlayerTokens,-1*(forwardRowInc),currentPlayerTokens) 
    otherJumps = expandJumps(board,player,otherOldJumpsList,opposingPlayerTokens,currentPlayerTokens,-1*(forwardRowInc))

    #if two jumps jump to the same to spot, then you want to take said jump and, in turn, block the opposing jump            
    for otherJump in otherJumps:
        for myJump in myJumps:
            if (otherJump[-2] + otherJump[-1]) == (myJump[-2] + myJump[-1]):
                if len(myJumps) == 1:
                    return ''
                else:
                    return myJump
    return ''

# 8: This function will allow checkers to have a "goup mentality." In other words, this funtion moves a current player checker behind another current player checker if possible
def watchYourSix(currentPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    move = ''
    for row in range(8):
        for col in range(8):
            #check if there is an empty space behind a fellow checker
            if board[row][col] in currentPlayerTokens and board[row+2*forwardRowInc][col+2*forwardRowInc] in currentPlayerTokens \
               and board[row+forwardRowInc][col+forwardRowInc] == '':
                move = chr(row+65)+str(col)+":"+chr(row+forwardRowInc+65)+str(col+forwardRowInc)
                return move
    return ''

# 9: Moves "home row" current player checkers when necessary (i.e when the current player has at least one king checker)
def stayHome(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    kingCount = 0
    redFromHomeSquares = ['A1','A3','A5','A7']
    blackFromHomeSquares = ['H0','H2','H4','H6']
    
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)

    for row in range(8):
        for col in range(8):
            if board[row][col] in ['R','B']:
                kingCount += 1
                
    if kingCount > 0:
        if 'r' in currentPlayerTokens:
            for move in myMoves:
                if move[:2] in redFromHomeSquares:
                    return move
        else:
            for move in myMoves:
                if move[:2] in blackFromHomeSquares:
                    return move
    return ''

# 10: This heuristic takes the first move in the current player's move list, if no other above move heuristics are possible
def firstMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    return myMoves[0] 

# 11: This heuristic takes the first jump in current player's jump list, if no other above jump heuristics are possible
def firstJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    return myJumps[0]

# 12: This heuristic blocks a opposing player's double jump, if they have one (by move)
def blockDoubleJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    myMoves = listValidMoves(board,currentPlayerTokens,forwardRowInc)
    myOldJumpsList = listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens) 
    myJumps = expandJumps(board,player,myOldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    
    otherMoves = listValidMoves(board,opposingPlayerTokens,-1*(forwardRowInc)) 
    otherOldJumpsList = listValidSingleJumps(board,opposingPlayerTokens,-1*(forwardRowInc),currentPlayerTokens) 
    otherJumps = expandJumps(board,player,otherOldJumpsList,opposingPlayerTokens,currentPlayerTokens,-1*(forwardRowInc))
    
    for jump in otherJumps:
        if len(jump) == 8:
            for move in myMoves:
                if (move[-2] + move[-1] == jump[-2] + jump[-1]) or (move[-2] + move[-1] == jump[3] + jump[4]):
                    return move
        else:
            return ''
    return ''
                
def getValidPlayerAction(PRINT_DEBUG,player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
    #Prepare lists for move selection
    if forwardRowInc==-1:
        kingRow=0
    else:
        kingRow=7
    validMovesList=listValidMoves(board,currentPlayerTokens,forwardRowInc)
    print("Valid Moves List",validMovesList)
    validSingleJumpsList=listValidSingleJumps(board,currentPlayerTokens,forwardRowInc,opposingPlayerTokens)
    print("Valid Single Jumps List",validSingleJumpsList)
    oldJumpsList=validSingleJumpsList
    expandedJumpsList=expandJumps(board,player,oldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    while expandedJumpsList != oldJumpsList:
        oldJumpsList=expandedJumpsList
        expandedJumpsList=expandJumps(board,player,oldJumpsList,currentPlayerTokens,opposingPlayerTokens,forwardRowInc)
    print("Expanded Jumps List",expandedJumpsList)
    #Decide on move
    if len(expandedJumpsList)>0: #JUMP MUST BE TAKEN
        if JumpTakeLongestOrFurthest(expandedJumpsList,kingRow) !="":
            input("Press enter to make this move or a similar one " + JumpTakeLongestOrFurthest(expandedJumpsList,kingRow))
            return JumpTakeLongestOrFurthest(expandedJumpsList,kingRow)
        if idealJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
            input("Press enter to make this move or a similar one " + idealJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
            return idealJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc)
        if JumpToKingRowRegularChecker(expandedJumpsList,kingRow,board) !="":
            input("Press enter to make this move or a similar one " + JumpToKingRowRegularChecker(expandedJumpsList,kingRow,board))
            return JumpToKingRowRegularChecker(expandedJumpsList,kingRow,board)
##        move=expandedJumpsList[0]
        move=input("Enter jump for player "+player+" => ").upper()
        while move != "QUIT" and move not in expandedJumpsList:
            print("Must take a jump . . .  try again!")
            move=input("Enter jump for player "+player+" => ").upper()
    else: #Select a Move 
        if MoveRegularCheckerToKingRow(validMovesList,kingRow,board) !="":
            input("Press enter to make this move or a similar one " + MoveRegularCheckerToKingRow(validMovesList,kingRow,board))
            return MoveRegularCheckerToKingRow(validMovesList,kingRow,board)
        if blockDoubleJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
           input("Press enter to make this move or a similar one " + blockDoubleJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
           return blockDoubleJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc)
        if blockJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
            input("Press enter to make this move or a similar one " + blockJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
            return blockJump(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc)
        if watchYourSix(currentPlayerTokens,board,forwardRowInc) != '':
           input("Press enter to make this move or a similar one " + watchYourSix(currentPlayerTokens,board,forwardRowInc))
           return watchYourSix(currentPlayerTokens,board,forwardRowInc)
        if noMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
            input("Press enter to make this move or a similar one " + noMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
            return noMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) 
        if MoveAnyToSideSquare(validMovesList) !="":
            input("Press enter to make this move or a similar one " + MoveAnyToSideSquare(validMovesList))
            return MoveAnyToSideSquare(validMovesList)
        if stayHome(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
            input("Press enter to make this move or a similar one " + stayHome(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
            return stayHome(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc)
        if firstMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc) != '':
            input("Press enter to make this move or a similar one " + firstMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc))
            return firstMove(player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc)
##        move=validMovesList[0]
        move=input("Enter move for player "+player+" => ").upper()
        while move != "QUIT" and move not in validMovesList:
            print("Bad move . . .  try again!")
            move=input("Enter move for player "+player+" => ").upper()
    return move

