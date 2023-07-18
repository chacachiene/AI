import initial
import random
import numpy as np
from copy import deepcopy
import math
VAR = initial.Define()

class Board:
    def __init__(self, board, numberreadyToBulb = [], numberOfNumberCell = [],numberBulb =[]):
        self.board = board
        self.numberreadyToBulb = numberreadyToBulb      
        self.numberOfNumberCell = numberOfNumberCell 
        self.numberBulb = numberBulb                
        self.numberCross = self.setCross()             
        self.numberExplode= -1                     
        self.numberOfNumberExplode = -1            
        self.numberLighted = 0
        self.score = -1000               
        self.isSolution = self.checkEnd()
    # count number of cell in board that can put bulb in  this 
    # return a list of bulb's location
    def readyToBulb(self):
        res = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if 0<= self.board[i][j] <=5 or self.board[i][j] == VAR.BULB  or (self.board[i][j] + 2)%8 ==0: continue
                res += [(i, j)]
        self.numberreadyToBulb = res
        return res
    
    # count number of cell that have number
    # return a list of cell's location
    def countNumberCell(self):
        count = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if 0<=self.board[i][j]<=5:
                    count += [(i,j)]
        self.numberOfNumberCell = count
        return count
    
    #---- count number of bulb in board
    #---- return a list of bulb's location
    def countBulb(self):
        bulbLocal = []
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if self.board[i][j]==8:
                    bulbLocal += [(i,j)]
        #self.numberBulb = bulbLocal
        return bulbLocal
    
    #---- count number of cross in board (that can't put bulb)
    #---- return number of cross
    def setCross(self):
        count = 0
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if self.board[i][j]==0:
                    if i < VAR.DIMENTION-1 and self.board[i+1][j] == -1:
                        self.board[i+1][j] = -2
                        count +=1
                    if i > 0 and self.board[i-1][j] ==-1:
                        self.board[i-1][j]=-2
                        count +=1
                    if j< VAR.DIMENTION - 1 and self.board[i][j+1] == -1:
                        self.board[i][j+1]=-2
                        count +=1
                    if j>0 and self.board[i][j-1] == -1:
                        self.board[i][j-1] = -2
                        count +=1
        return count
    
    #---- count number of bulb that explode (when it light up another bulb)
    #---- return number of explore
    def countExplode(self):
        explode = 0
        
        
        #---- check row
        for i in range(VAR.DIMENTION):
            start = 0
            j = 0
            while j < VAR.DIMENTION:
                if self.board[i][j] == VAR.BULB:
                    start = j
                    k = start + 1
                    while k < VAR.DIMENTION:
                        if 0 <= self.board[i][k] <= 5:
                            j = k
                            break

                    
                        if self.board[i][k] == 8:
                            explode += 1
                        k += 1
                j += 1
                
        #---- check col
        for i in range(VAR.DIMENTION):
            start = 0
            j = 0  # Introduce a separate variable to track the current row
            while j < VAR.DIMENTION:
                if self.board[j][i] == VAR.BULB:
                    start = j
                    k = start + 1
                    while k < VAR.DIMENTION:
                        if 0 <= self.board[k][i] <= 5:
                            j = k
                            break
                        if self.board[k][i] == 8:
                            explode += 1
                        k += 1
                j += 1
        self.numberExplode = explode
        return explode
    
    #---- count number of bulb that not match with number in cell
    #---- return number of numberExplode
    def countNumberExplode(self):
        explode = 0
        numberCell = self.numberOfNumberCell
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            number = self.board[x][y]
            bulb = 0
            if self.board[x][y] == VAR.NONUMBER: continue
            if x+1 < VAR.DIMENTION:
                bulb +=1 if self.board[x+1][y] == VAR.BULB else 0
            if x-1 >= 0:
                bulb +=1 if self.board[x-1][y] == VAR.BULB else 0
            if y+1 < VAR.DIMENTION:
                bulb +=1 if self.board[x][y+1] == VAR.BULB else 0
            if y-1 >= 0:
                bulb +=1 if self.board[x][y-1] == VAR.BULB else 0
            if bulb != number :
                explode += abs(number - bulb)
        self.numberOfNumberExplode = explode
        return explode
    
    #---- count the number of cell that light up
    #---- return number of lighted
    def countLighted(self):
        light = 0
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if self.board[i][j] > 5:
                    light += 1
        self.numberLighted = light
        return light
    
    #---- calculate score of a state (board)
    #---- return score
    def heuristic(self):
        
        countNumberCell = len(self.numberOfNumberCell)
        countNumberBulb = len(self.countBulb())
        countExplore = self.numberExplode
        countNumberExplode = self.numberOfNumberExplode    
        countLight = self.numberLighted
        #score = countLight // (VAR.DIMENTION*VAR.DIMENTION -countNumberCell) - countExplore*3 - countNumberExplode*2
        score = countLight - countExplore - countNumberExplode
        #score = VAR.DIMENTION*countLight/(VAR.DIMENTION*VAR.DIMENTION -countNumberCell) - countExplore/countNumberBulb - (VAR.DIMENTION - 1)*countNumberExplode/countNumberCell
        self.score = score
        return score
    
    #---- change the value of cells when bulb is put
    def lightUp(self, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            if nextcol < VAR.DIMENTION:
                for i in range(nextcol, VAR.DIMENTION):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: continue
                    self.board[x][i] +=8
            if nextrow < VAR.DIMENTION:
                for i in range(nextrow, VAR.DIMENTION):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: continue
                    self.board[i][y] +=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: continue
                    self.board[i][y] +=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: continue
                    self.board[x][i] +=8
        return self.board
    
    #---- change the value of cells when bulb is removed
    def lightOff(self, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            c = 0
            if nextcol < VAR.DIMENTION:
                for i in range(nextcol, VAR.DIMENTION):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: 
                        c +=1
                        continue
                    self.board[x][i] -=8
                    
            if nextrow < VAR.DIMENTION:
                for i in range(nextrow, VAR.DIMENTION):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: 
                        c +=1
                        continue
                    self.board[i][y] -=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: 
                        c +=1
                        continue
                    self.board[i][y] -=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: 
                        c += 1
                        continue
                    self.board[x][i] -=8
            self.board[x][y] = c * 8 -1
        return self.board

    #---- check if the board is a solution
    def checkEnd(self):
        for i in range(VAR.DIMENTION):
            for j in range(VAR.DIMENTION):
                if self.board[i][j] == VAR.EMPTY or self.board[i][j] == VAR.CROSS:
                    return False
        if self.countNumberExplode() > 0 or self.countExplode() > 0:
            return False
        self.isSolution =True
        return True

def main():
    game =initial.StateStart()
    game = Board(game.board)
    game.update()
    print(game.board)
    print(game.numberOfNumberCell)
    print(game.score)
    print(game.numberreadyToBulb)
    print(game.numberBulb)
    print(game.numberCross)
    print(game.numberExplode)
    print(game.numberOfNumberExplode)
    print(game.isSolution)

if __name__=='__main__':
    main()