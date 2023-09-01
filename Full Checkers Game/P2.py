
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

def getValidPlayerAction(PRINT_DEBUG,player,currentPlayerTokens,opposingPlayerTokens,board,forwardRowInc):
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
    if len(expandedJumpsList)>0:
        move=expandedJumpsList[0]
##        move=input("Enter jump for player "+player+" => ").upper()
##        while move != "QUIT" and move not in expandedJumpsList:
##            print("Must take a jump . . .  try again!")
##            move=input("Enter jump for player "+player+" => ").upper()
    else:
        if len(validMovesList)>0:
            move=validMovesList[0]
        else:
            return "QUIT"
##        move=input("Enter move for player "+player+" => ").upper()
##        while move != "QUIT" and move not in validMovesList:
##            print("Bad move . . .  try again!")
##            move=input("Enter move for player "+player+" => ").upper()
    return move

