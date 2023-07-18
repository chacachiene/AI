import initial
import random
import numpy as np
from copy import deepcopy

VAR = initial.Define()
from board import Board

   
def simulated_annealing(problem, numberiterator):
   
    current = problem.start
    goalState = problem.goal
    path = []
    for t in range(int(numberiterator)):
        T = problem.schedule(t) 
        nextState, nextValue, type = problem.getNeighbors(current)
        if current.checkEnd():
            return path
        if nextValue > goalState.score:
            goalState = nextState
            path += [goalState]
            
        if nextValue > current.score:  
            current = nextState
        else:
            randum = np.random.rand()
            E = -abs(current.score - nextValue)
            p = np.exp(E/T)
            if randum < p:
                current = nextState
        for i in range(VAR.DIMENTION):
            print(current.board[i])
        print(f'### {current.score}******T={T}******i={t} ###')
    return path
class problem:
    def __init__(self, start , Cc, Pp, numIter ):
        self.start = start
        self.goal = start
        self.Cc = Cc
        self.Pp = Pp
        self.numIter= numIter
        
    def schedule(self, t):
        # return self.Cc/(t + 1)**self.Pp
        # return 100/np.log(t + 1)
        return 1000/np.log(t + 1)
    #---- get the candidate state
    #---- return the next state, value of next state 
    def getNeighbors(self, board):
        newBoard = deepcopy(board)
        newBoard.countLighted()
        newBoard.readyToBulb()
        if newBoard.numberLighted < VAR.DIMENTION/2:
            p = np.random.rand()
            if p > newBoard.numberLighted/(VAR.DIMENTION*VAR.DIMENTION - newBoard.numberOfNumberCell):
                add = self.addToNextState(newBoard)
                return (add[0],add[1], "add")
        if len(newBoard.numberreadyToBulb) < VAR.DIMENTION/2:
            p = np.random.rand()
            if p > len(newBoard.numberreadyToBulb)/(VAR.DIMENTION*VAR.DIMENTION - newBoard.numberOfNumberCell):
                dell = self.delToNextState(newBoard)
                return (dell[0],dell[1], "dell")
        add = self.addToNextState(newBoard)
        dell = self.delToNextState(newBoard)
        move = self.moveToNextState(newBoard)
        # m = random.choice([add[1], dell[1], move[1]])
        m = max(add[1], dell[1], move[1])
        
        if m == add[1]:
            return (add[0],add[1], "add")
        if m ==  dell[1]:
            return (dell[0],dell[1],  "del")
        if m == move[1]:
            return (move[0],move[1], "move")

    #---- chose the number of ready cell to bulb          
    def randomeBulb(self, board, num):
        CellForBulb = board.readyToBulb()
        if len(CellForBulb) < num:
            return CellForBulb
        newBulb = random.sample(CellForBulb,num)
        return newBulb
    
    def prepareToSearch(self,board):
#        board.update()
        board.setCross()
        numberBulb = self.setBulb(board)
        board.lightUp(numberBulb)          
        
        numNewBulb = VAR.DIMENTION *2 - len(numberBulb) 
        
        newBulbLocation = self.randomeBulb(board,numNewBulb)
        
        for i in range(len(newBulbLocation)):
            board.board[newBulbLocation[i][0]][newBulbLocation[i][1]] = VAR.BULB

        board.numberBulb += newBulbLocation
        board.lightUp(newBulbLocation)
        board.countExplode()
        board.countNumberExplode()
        board.readyToBulb()
        board.heuristic()
        return board
    #---- set the bulb to match with the number in cell (not care about the explode)
    def setBulb(self,board):
        numberCell = board.countNumberCell()
        bulbReal = []
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            if board.board[x][y] != VAR.NONUMBER and board.board[x][y] != VAR.NUMBER0:
                bulb = []
                if x+1 < VAR.DIMENTION:
                    bulb += [(x+1,y)] if board.board[x+1][y] == VAR.EMPTY else []
                if x-1 >= 0:
                    bulb += [(x-1,y)] if board.board[x-1][y] == VAR.EMPTY else []
                if y+1 < VAR.DIMENTION:
                    bulb += [(x,y+1)] if board.board[x][y+1] == VAR.EMPTY else []
                if y-1 >= 0:
                    bulb+= [(x,y-1)] if board.board[x][y-1] == VAR.EMPTY else []
                
                if bulb:
                    if len(bulb) < board.board[x][y]:
                        bulbReal = bulb
                    else:
                        bulbReal = random.sample(bulb, board.board[x][y])
                    board.numberBulb += bulbReal
                    for x in bulbReal:
                        board.board[x[0]][x[1]] = VAR.BULB
        return board.numberBulb
        
    #---- move to next state by add a bulb to a current state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def addToNextState(self, board):
        
        newBoard = deepcopy(board)
        res = ([],-1000,(-1,-1))
        score = -1000
        readyToBulb = newBoard.numberreadyToBulb
        
        if len(readyToBulb) > VAR.DIMENTION:
            
            nextBulb = random.sample(readyToBulb, VAR.DIMENTION)
            
            for i in range(len(nextBulb)):                
                tmpBoard = deepcopy(newBoard)
                
                
                tmpBoard.numberreadyToBulb.remove(nextBulb[i])
                tmpBoard.numberBulb += [nextBulb[i]]
                
                tmpBoard.board[nextBulb[i][0]][nextBulb[i][1]] = VAR.BULB
                tmpBoard.lightUp([nextBulb[i]])
                
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()                
                
                h = tmpBoard.heuristic()

                if h > score:
                    score = h
                    res = (tmpBoard, h, nextBulb[i])   #  nextBulb for what
        elif len(readyToBulb) > 0:
            
            for i in range(len(readyToBulb)):
                tmpBoard = deepcopy(newBoard)
                tmpBoard.numberreadyToBulb.remove(readyToBulb[i])
                tmpBoard.numberBulb += [readyToBulb[i]]
                tmpBoard.board[readyToBulb[i][0]][readyToBulb[i][1]] = VAR.BULB
                tmpBoard.lightUp([readyToBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()                  
                h = tmpBoard.heuristic()
                if h > score:
                    score = h
                    res = (tmpBoard,h,readyToBulb[i])
        return res
    
    #---- move to next state by delete a bulb to a current state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def delToNextState(self, board):
        
        curBoard = deepcopy(board)
        res = ([],-1000,(-1,-1))
        score = -1000
        curBulb = curBoard.numberBulb
        
        if len(curBulb) > VAR.DIMENTION:
            delBulb = random.sample(curBulb, VAR.DIMENTION)
            for i in range(len(delBulb)):
                tmpBoard = deepcopy(curBoard)
                
                tmpBoard.numberreadyToBulb += [delBulb[i]]
                tmpBoard.numberBulb.remove(delBulb[i])
                tmpBoard.lightOff( [delBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()

                h = tmpBoard.heuristic()
                if h > score:
                    score = h
                    res = (tmpBoard,h, delBulb[i])
                    
            # if dell:
            #     curBulb = curBulb.remove(res[2])
        elif len(curBulb) > 0:
            for i in range(len(curBulb)):
                tmpBoard = deepcopy(curBoard)
                tmpBoard.numberreadyToBulb += [curBulb[i]]
                tmpBoard.numberBulb.remove(curBulb[i])
                tmpBoard.lightOff([curBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()
                
                h=tmpBoard.heuristic()
                
                if h > score:
                    score = h
                    res = (tmpBoard,h,curBulb[i])
        return res
    
    #---- move to next state by move a bulb for a cell to another state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def moveToNextState(self,board):
        curBoard = deepcopy(board)
        score = -1000
        res = ([],-1000)
        
        readyToBulb = curBoard.numberreadyToBulb
        curBulb = curBoard.numberBulb
        
        if len(readyToBulb) > 0 and len(curBulb) > 0:
            for i in range(VAR.DIMENTION):
                if curBulb:
                    Bulb = random.sample(curBulb,1)
                    if readyToBulb:
                        tmpFree = random.sample(readyToBulb,1)
                        
                        tmpBoard = deepcopy(curBoard)
                        
                        tmpBoard.numberreadyToBulb += Bulb
                        tmpBoard.numberBulb.remove(Bulb[0])
                        tmpBoard.lightOff(Bulb)
                        
                        tmpBoard.numberBulb += tmpFree
                        tmpBoard.numberreadyToBulb.remove(tmpFree[0])
                        tmpBoard.board[tmpFree[0][0]][tmpFree[0][1]] = VAR.BULB
                        tmpBoard.lightUp(tmpFree)
                        
                        tmpBoard.countExplode()
                        tmpBoard.countNumberExplode()
                        tmpBoard.countLighted()
                        
                        h = tmpBoard.heuristic()
                        if h > score:
                            score = h
                            res = (tmpBoard,h)
        return res
import time 
def main():
    # Cc = 7
    # Pp = 0.37
    # numberiterator = 30000

    # a = initial.StateStart()
    # s = problem(a.board, a.board, Cc,Pp,numberiterator)
    # boardFirst = Board(a.board)    
    # FirstState = s.prepareToAStar(boardFirst)
    # initialState = state(FirstState, FirstState.score)
    # bestState  = state(FirstState, -1000)
    # theGame = problem(initialState, bestState, Cc,Pp,numberiterator)
    
    # startTime = time.time()
    # solution = simulated_annealing(theGame, numberiterator)
    # endTime = time.time() - startTime
    
    # for i in range(VAR.DIMENTION):
        
    #     print(solution.path.board[i])
    # print(solution.path.score)
    # print(solution.path.numberBulb)
    # print(solution.path.isSolution)
    # print('time elapsed', endTime)
    Cc = 7
    Pp = 0.37
    numberiterator = 100000
    
    state = initial.StateStart() 
    boardFirst = Board(state.board)
      
    s = problem(boardFirst, Cc,Pp,numberiterator)
    
    s.prepareToSearch(boardFirst)
    
    startTime = time.time()
    solution = simulated_annealing(s, numberiterator)
    
    endTime = time.time() - startTime
    # for j in range(len(solution)):
    #     for i in range(VAR.DIMENTION):        
    #         print(solution[j].board[i])
    #     print(f'-------{solution[j].score}--------')

    print('time elapsed', endTime)
if __name__ == "__main__":
    main()