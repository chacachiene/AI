import csv
board=[]
d = 0
with open('input/14normal.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        intRow = [int(element) for element in row]
        #intRow = [int(element) for element in row]
        board += [intRow]
    d = len(board)
print(board)
    
class Define:
    def __init__(self):
        self.DIMENTION = d
        self.BULB = 8
        self.EMPTY = -1
        self.CROSS = -2
        self.NONUMBER = 5
        self.NUMBER0 = 0
        self.NUMBER1 =1
        self.NUMBER2 = 2
        self.NUMBER3 = 3
        self.NUMBER4 = 4
        self.LIGHTED = [7,15,23]
        self.CROSSLIGHT = [6,14,22]

class StateStart:
    def __init__(self):
        self.board = board
        self.history=[]
    
    
    def makeMove(self, move):
        if move.type == 1:
            sq = self.board[move.row][move.col]
            nextrow = move.row + 1
            nextcol = move.col + 1
            prerow = move.row - 1
            precol = move.col -1
            if sq < 0:
                self.board[move.row][move.col] = 8
                for i in range(nextrow, 7):
                    if self.board[i][move.col] >=0 and self.board[i][move.col]<=5: break
                    self.board[i][move.col] +=8
                for i in range(nextcol, 7):
                    if self.board[move.row][i] >=0 and self.board[move.row][i]<=5: break
                    self.board[move.row][i] +=8
                for i in range(prerow, -1, -1):
                    
                    if self.board[i][move.col] >=0 and self.board[i][move.col]<=5: break

                    self.board[i][move.col] +=8
                for i in range(precol, -1, -1):
                    if self.board[move.row][i] >=0 and self.board[move.row][i] <=5: break
                    self.board[move.row][i] +=8
            elif self.board[move.row][move.col] ==8:
                self.board[move.row][move.col] = -1
                for i in range(nextrow, 7):
                    
                    if self.board[i][move.col] >=0 and self.board[i][move.col]<=5: break
                    self.board[i][move.col] -=8
                for i in range(move.col+1, 7):
                    if self.board[move.row][i] >=0 and self.board[move.row][i]<=5: break
                    self.board[move.row][i] -=8
                for i in range(move.row-1, -1, -1):
                    if self.board[i][move.col] >=0 and self.board[i][move.col] <=5 : break
                    self.board[i][move.col] -=8
                for i in range(move.col-1, -1, -1):
                    if self.board[move.row][i] >=0 and self.board[move.row][i] <=5: break
                    self.board[move.row][i] -=8               
                self.history.append(move)
            elif sq == 7 or sq ==15:
                pass
                
                
        if move.type == 3:
            if self.board[move.row][move.col] == 8 or self.board[move.row][move.col]==-1:
                self.board[move.row][move.col] = -2
                if self.board[move.row][move.col] == 8:
                    self.board[move.row][move.col] = -1
                    for i in range(move.row+1, 7):
                        if self.board[i][move.col] >=0 and self.board[i][move.col]<=5: break
                        self.board[i][move.col] -=8
                    for i in range(move.col+1, 7):
                        if self.board[move.row][i] >=0 and self.board[move.row][i]<=5: break
                        self.board[move.row][i] -=8
                    for i in range(move.row-1, -1, -1):
                        if self.board[i][move.col] >=0 and self.board[i][move.col] <=5 : break
                        self.board[i][move.col] -=8
                    for i in range(move.col-1, -1, -1):
                        if self.board[move.row][i] >=0 and self.board[move.row][i] <=5: break
                        self.board[move.row][i] -=8    
                    self.history.append(move)
            elif self.board[move.row][move.col] == -2 or self.board[move.row][move.col] == 6 or self.board[move.row][move.col] == 14:
                self.board[move.row][move.col] +=1
                self.history.append(move)
            elif self.board[move.row][move.col] ==7 or self.board[move.row][move.col] == 15:
                self.board[move.row][move.col] -=1
                self.history.append(move)

    def check(self,light):
        if light.row not in light.l or light.col not in light.l.values():
            light.l[light.row]=light.col
            return (True,(light.row,light.col))
        return (False,(light.row, light.col))
class StateMove():
    def __init__(self, board, sq, type):
        self.board = board
        self.row = sq[0]
        self.col = sq[1] 
        self.type = type
class checkLight():
    def __init__(self, board,sq):
        self.l = dict({})
        self.board = board
        self.row=sq[0]
        self.col=sq[1]