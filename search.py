import initial
import random
import numpy as np
from copy import deepcopy
import math
VAR = initial.Define()

class state:
    def __init__(self, path, value):
        self.path = path
        self.value = value
        
# class problem:
#     def __init__(self, start, goal, heuristic, schedule ):
#         self.start = start
#         self.goal = goal
#         self.heuristic = heuristic
#         self.schedule = schedule
        

    
def simulated_annealing(problem, numberiterator):
    current = problem.start
    goalState = problem.goal 
    time =[]
    value = []
    for t in range(int(numberiterator)):
        T = problem.schedule(t)
        nextState, nextValue = problem.getNeighbors(current.path)
        
        if nextValue > goalState.value:
            problem.goal.path = nextState
            problem.goal.value = nextValue 
        
        if nextValue > current.value:  
            problem.current.path = nextState
            problem.current.value = nextValue
        else:
            randum = np.random.rand()
            E = -abs(current.value - nextValue)
            p = np.exp(E/T)
            if randum < p:
                problem.current.path = nextState
                problem.current.value = nextValue
        if t% 100 ==0:
            time += [t]
            value += [problem.goal.value]
        if t == numberiterator:
            time +=[t]
            value += [problem.goal.value]
    return problem.goal

class problem:

    path = []
    Cc = 7
    Pp = 0.37
    def __init__(self, start, goal, schedule ):
        self.start = start
        self.current=start
        self.goal = goal
        self.schedule = schedule
        self.numberreadyToBulb = []
        self.numberBulb = [] #ok
        self.numberCross = 0 # ok
        self.numberExplode= 0
        self.numberOfNumberExplode = 0
        self.numberOfNumberCell = self.countNumberCell(start)
        

    def checkEnd(self,board):
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if board[i][j] == -1:
                    return False
        if self.countNumberExplode(board) > 0 or self.countExplode(board) > 0:
            return False
        return True
    def getNeighbors(self, board):
        add = self.addToNextState(board)
        dell = self.delToNextState(board)
        move = self.moveToNextState(board)
        m = max(add[1], dell[1], move[1])
        if m == add[1]:
            return (add[0],add[1])
        if m ==  dell[1]:
            return (dell[0],dell[1])
        if m == move[1]:
            return (move[0],move[1])

                
    def readyToBulb(self, board):
        res = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if board[i][j] == -1:
                    res += [(i, j)]
                    
        self.numberreadyToBulb = res
        return res
    def setCross(self,board):
        count = 0
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if board[i][j]==0:
                    if i < VAR.DIMENTION-1 and board[i+1][j] == -1:
                        board[i+1][j] = -2
                        count +=1
                    if i > 0 and board[i-1][j] ==-1:
                        board[i-1][j]=-2
                        count +=1
                    if j< VAR.DIMENTION - 1 and board[i][j+1] == -1:
                        board[i][j+1]=-2
                        count +=1
                    if j>0 and board[i][j-1] == -1:
                        board[i][j-1] = -2
                        count +=1
        self.numberCross = count
        return count
    def countBulb(self, board):
        bulbLocal = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if board[i][j]==8:
                    bulbLocal += [(i,j)]
        #self.numberBulb = bulbLocal
        return bulbLocal
    def lightUp(self, board, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            if nextcol < VAR.DIMENTION:
                for i in range(nextcol, VAR.DIMENTION):
                    if 0 <= board[x][i]<=5: break
                    if board[x][i] == 8: continue
                    board[x][i] +=8
            if nextrow < VAR.DIMENTION:
                for i in range(nextrow, VAR.DIMENTION):
                    if 0 <= board[i][y]<=5: break
                    if board[i][y] == 8: continue
                    board[i][y] +=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= board[i][y]<=5: break
                    if board[i][y] == 8: continue
                    board[i][y] +=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= board[x][i]<=5: break
                    if board[x][i] == 8: continue
                    board[x][i] +=8
        return board
    def lightOff(self, board, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            if nextcol < VAR.DIMENTION:
                for i in range(nextcol, VAR.DIMENTION):
                    if 0 <= board[x][i]<=5: break
                    if board[x][i] == 8: continue
                    board[x][i] -=8
            if nextrow < VAR.DIMENTION:
                for i in range(nextrow, VAR.DIMENTION):
                    if 0 <= board[i][y]<=5: break
                    if board[i][y] == 8: continue
                    board[i][y] -=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= board[i][y]<=5: break
                    if board[i][y] == 8: continue
                    board[i][y] -=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= board[x][i]<=5: break
                    if board[x][i] == 8: continue
                    board[x][i] -=8
        return board
    def countExplode(self, board):
        explode = 0
        for i in range(VAR.DIMENTION):
            start = 0
            j =0
            while j < VAR.DIMENTION:
                if board[i][j] == VAR.BULB:
                    start = j
                    
                    for k in range(start+1, VAR.DIMENTION):
                        if 0<=board[i][k] <=5 or k == VAR.DIMENTION-1: 
                            j = k
                            break
                        if board[i][k] == 8:
                            explode += 1
                j += 1
        for i in range(VAR.DIMENTION):
            start = 0
            j = 0  # Introduce a separate variable to track the current row
            while j < VAR.DIMENTION:
                if board[j][i] == VAR.BULB:
                    start = j
                    k = start + 1
                    while k < VAR.DIMENTION:
                        if 0 <= board[k][i] <= 5 or k == VAR.DIMENTION - 1:
                            j = k
                            break
                        if board[k][i] == 8:
                            explode += 1
                        k += 1
                j += 1
        self.numberExplode = explode
        return explode
    def countNumberCell(self,board):
        count = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if 0<=board[i][j]<=5:
                    count += [(i,j)]
        #self.numberOfNumberCell = count
        return count
    def countNumberExplode(self, board):
        explode = 0
        numberCell = self.numberOfNumberCell
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            number = board[x][y]
            bulb = 0
            if x+1 < VAR.DIMENTION:
                bulb +=1 if board[x+1][y] == VAR.BULB else 0
            if x-1 >= 0:
                bulb +=1 if board[x-1][y] == VAR.BULB else 0
            if y+1 < VAR.DIMENTION:
                bulb +=1 if board[x][y+1] == VAR.BULB else 0
            if y-1 >= 0:
                bulb +=1 if board[x][y-1] == VAR.BULB else 0
            if bulb != number and board[x][y]!=5:
                explode += abs(number - bulb)
        self.numberOfNumberExplode = explode
        return explode
                
    def randomeBulb(self, board, num):
        CellForBulb = self.readyToBulb(board)
        newBulb = random.sample(CellForBulb,num)
        return newBulb
        
    def prepareToAStar(self,board):
        self.setCross(board)
        self.setBulb(board)
    
        self.numberBulb = self.countBulb(board)
        
        numNewBulb = VAR.DIMENTION *2 - len(self.countBulb(board))
        newBulbLocation = self.randomeBulb(board,numNewBulb )
        for i in range(numNewBulb):
            board[newBulbLocation[i][0]][newBulbLocation[i][1]] = VAR.BULB
            self.lightUp(board, newBulbLocation[i])
        return board
    def setBulb(self,board):
        numberCell = self.numberOfNumberCell 
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            if board[x][y] != 5:
                bulb = []
                if x+1 < VAR.DIMENTION:
                    bulb += [(x+1,y)] if board[x+1][y] == VAR.EMPTY else []
                if x-1 >= 0:
                    bulb += [(x-1,y)] if board[x-1][y] == VAR.EMPTY else []
                if y+1 < VAR.DIMENTION:
                    bulb += [(x,y+1)] if board[x][y+1] == VAR.EMPTY else []
                if y-1 >= 0:
                    bulb+= [(x,y-1)] if board[x][y-1] == VAR.EMPTY else []
                
                if bulb:
                    if len(bulb) < board[x][y]:
                        return False
                    bulbReal = random.sample(bulb, board[x][y])
                    self.numberBulb += bulbReal
                    for x in bulbReal:
                        board[x[0]][x[1]] = VAR.BULB
        return True

        
        
        
    def heuristic(self, board):
        score = 0
        if not self.numberreadyToBulb:
            self.readyToBulb(board)
        countWhite = len(self.numberreadyToBulb)
        if not self.numberExplode:
            self.countExplode(board)
        countExplore = self.numberExplode
        if not self.numberBulb:
            self.countBulb(board)
        countBulb = len(self.numberBulb)
        
        countNumberCell = len(self.numberOfNumberCell)
        if not self.numberOfNumberExplode:
            self.countNumberExplode(board)
        countNumberExplode = self.numberOfNumberExplode
        
        countLight = VAR.DIMENTION * VAR.DIMENTION - countWhite - countNumberCell
        
        score = countLight // countWhite - countExplore - countNumberExplode if countWhite != 0 else - countExplore - countNumberExplode
        return score
        
                
    def addToNextState(self, board):
        if not self.numberreadyToBulb:
            self.readyToBulb(board)
        readyToBulb = self.numberreadyToBulb
        if not self.numberBulb:
            self.countBulb(board)
        curBulb = deepcopy(self.numberBulb)
        res = ([],-1000,(-1,-1))
        score = -1000
        curboard = deepcopy(board)
        
        if len(readyToBulb) > 10:
            nextBulb = random.sample(readyToBulb, 10)
            for i in range(nextBulb):
                tmpBoard = deepcopy(curboard)
                
                tmpBoard[nextBulb[i][0]][nextBulb[i][1]] = VAR.BULB
                self.lightUp(tmpBoard, [nextBulb[i]])
                
                h = self.heuristic(tmpBoard)
                if h > score:
                    score = h
                    res = (tmpBoard,h, nextBulb[i])
            if res[1] > -1000:
                curBulb += res[2]
        elif len(readyToBulb) > 0:
            for i in range(len(readyToBulb)):
                tmpBoard = deepcopy(curboard)
                
                tmpBoard[readyToBulb[i][0]][readyToBulb[i][1]] = 8
                tmpLight = self.lightUp(tmpBoard, [readyToBulb[i]])
                h = self.heuristic(tmpBoard)
                if h > score:
                    score = h
                    res = (tmpBoard,h,readyToBulb[i])
            if res[1] > -1000:  
                curBulb += res[2]
        else:
            res=(curboard,score,curBulb)
        
        return res
    def delToNextState(self, board):
        curBoard = deepcopy(board)
        if self.numBulb == []:
            self.countBulb(board)
        curBulb = deepcopy(self.numBulb)
        
        res = ([],-1000,(-1,-1))
        score = -1000
        dell = False
        if len(curBulb) > 10:
            delBulb = random.sample(curBulb, 10)
            for i in range(len(delBulb)):
                tmpBoard = deepcopy(curBoard)
                tmpBoard[delBulb[i][0]][delBulb[i][1]] = -1
                self.lightOff(curBoard, [delBulb[i]])
                h = self.heuristic(tmpBoard)
                if h > score:
                    score = h
                    res = (tmpBoard,h, delBulb[i])
                    dell = True
            if dell:
                curBulb = curBulb.remove(res[2])
        elif len(curBulb) > 0:
            tmpBoard = deepcopy(curBoard)
            for i in range(len(curBulb)):
                tmpBoard[curBulb[i][0]][curBulb[i][1]] = 8
                tmpLight = self.lightOff(tmpBoard, [curBulb[i]])
                h = self.heuristic(tmpBoard)
                if h > score:
                    score = h
                    res = (tmpBoard,h)
                    dell = True
        else:
            res=(curBoard,score,curBulb)
        
        return res
            
    def moveToNextState(self,board):
        curBoard = deepcopy(board)
        if self.numberBulb == []:
            self.numberBulb = self.countBulb(board)
        curBulb = deepcopy(self.numberBulb)
        score = -1000
        res = ([],-1000,(-1,-1))
        if self.numberreadyToBulb == []:
            self.numberreadyToBulb = self.readyToBulb(board)
        readyToBulb = deepcopy(self.numberreadyToBulb)
        if len(readyToBulb) > 0 and len(curBulb) > 0:
            for i in range(VAR.DIMENTION):    
                if curBulb:
                    Bulb = random.sample(curBulb,1)
                    if readyToBulb:
                        tmpFree = random.sample(readyToBulb,1)
                        tmpBoard = deepcopy(curBoard)
                        curBulb.remove(Bulb[0])
                        readyToBulb.remove(tmpFree[0])
                        curBulb += tmpFree
                        tmpBoard[Bulb[0][0]][Bulb[0][1]] = VAR.EMPTY
                        self.lightOff(tmpBoard, Bulb)
                        readyToBulb += Bulb
                        tmpBoard[tmpFree[0][0]][tmpFree[0][1]] = VAR.BULB
                        self.lightUp(tmpBoard, tmpFree)
                        h = self.heuristic(curBoard)
                        if h > score:
                            score = h
                            res = (tmpBoard,h,Bulb[0],tmpFree[0])
                else: 
                    return (curBoard, score, curBulb,0)
            return res
        else:
            return (curBoard, score, curBulb,0)


import time 
def main():
    Cc = 7
    Pp = 0.37
    numberiterator = 1000
    def schedule(time, C= Cc, p = Pp):
        return C/(time + 1)**p
    a = initial.StateStart()
    s = problem(a.board, a.board, schedule)
    startTime = time.time()
    initialPath = s.prepareToAStar(a.board)
    initialState = state(initialPath, s.heuristic(initialPath))
    bestState  = state(initialPath, -1000)
    theGame = problem(initialState, bestState, schedule )
    solution = simulated_annealing(theGame, numberiterator)
    print(solution.value)
    endTime = time.time() - startTime
    print('time elapsed', endTime)
if __name__ == "__main__":
    main()