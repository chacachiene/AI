import pygame as p
import initial
import search
import board
import time
WIDTH = HEIGHT = 640

VAR = initial.Define()
MAXFPS = 15
SQSIZE = HEIGHT // VAR.DIMENTION
'''
LOAD IMAAGE
'''
IMAGE={}
def loadImage():
    for i in range(9):
        IMAGE[i] = p.transform.scale(p.image.load("img/"+str(i)+".png"), (SQSIZE/2,SQSIZE/2))
''''''     


def main():
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT+100))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    state = initial.StateStart()
   
    run = True
    sqSelected = ()
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                col = x // SQSIZE
                row = y // SQSIZE
                # move = initial.StateMove(state.board, (row, col), e.button)
                # state.makeMove(move)
                # check = initial.checkLight(state.board, (row,col))
                # if state.check(check):
                #     changeLight(screen,state.board, (row,col))
            elif e.type == p.KEYDOWN:
                solve(state)         
        drawState(screen, state)
        clock.tick(MAXFPS)
        p.display.flip()
def solve(state):
    Cc = 7
    Pp = 0.37
    numberiterator = 100000
    
    
    boardFirst = board.Board(state.board)
      
    s = search.problem(boardFirst, Cc,Pp,numberiterator)
    
    s.prepareToSearch(boardFirst)
    
    startTime = time.time()
    solution = search.simulated_annealing(s, numberiterator)
    
    endTime = time.time() - startTime
    for j in range(len(solution)):
        for i in range(VAR.DIMENTION):        
            print(solution[j].board[i])
        print(f'-------{solution[j].score}--------')
    if solution[j].isSolution:
        print('success')
    else:
        print('fail')
    print('time elapsed', endTime)


def drawState(screen, state):
    
    drawBoard(screen)
    drawPiece(screen, state.board)
    # checkSuccess(screen, state.board)
    
def drawBoard(screen):
    color = [p.Color("white"), p.Color("black")]
    for j in range(VAR.DIMENTION):
        for i in range(VAR.DIMENTION):
            p.draw.rect(screen, color[0], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE))
    for i in range(VAR.DIMENTION):
        p.draw.line(screen, color[1], (0,i*SQSIZE), (WIDTH, i*SQSIZE),1)
    for j in range(VAR.DIMENTION):
        p.draw.line(screen, color[1], (j*SQSIZE,0), (j*SQSIZE, HEIGHT))

    
def drawPiece(screen, board):
    color = {"wh": p.Color("white"), 
             "bl": p.Color("black"),
            "ye": p.Color("yellow"),
    }
    loadImage()
    for i in range(VAR.DIMENTION):
        for j in range(VAR.DIMENTION):
            if board[i][j] != -1:
                if board[i][j] in range(6):
                    p.draw.rect(screen, color["bl"], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE))
                    screen.blit(IMAGE[board[i][j]], p.Rect(j*SQSIZE+SQSIZE/4, i*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
                elif board[i][j] == VAR.BULB:
                    p.draw.rect(screen, color['ye'], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE))
                    screen.blit(IMAGE[6], p.Rect(j*SQSIZE+SQSIZE/4, i*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
                elif board[i][j] == VAR.CROSS:
                    screen.blit(IMAGE[7], p.Rect(j*SQSIZE+SQSIZE/4, i*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
                elif board[i][j] in VAR.CROSSLIGHT:
                    p.draw.rect(screen, color['ye'], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE))
                    screen.blit(IMAGE[7], p.Rect(j*SQSIZE+SQSIZE/4, i*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
                elif board[i][j] in VAR.LIGHTED:
                    p.draw.rect(screen, color['ye'], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE))
            else:
                p.draw.rect(screen, color['wh'], p.Rect(j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE)) 
    for i in range(VAR.DIMENTION+1):
        p.draw.line(screen, color['bl'], (0,i*SQSIZE), (WIDTH, i*SQSIZE),1)
    for j in range(VAR.DIMENTION+1):
        p.draw.line(screen, color['bl'], (j*SQSIZE,0), (j*SQSIZE, HEIGHT))   
def changeLight(screen,board, sq):
    for i in range(VAR.DIMENTION):
        if board[sq[0]][i] == 8:
            screen.blit(IMAGE[8], p.Rect(i*SQSIZE+SQSIZE/4, sq[0]*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
        if board[i][sq[1]] == 8:
            screen.blit(IMAGE[8], p.Rect(sq[1]*SQSIZE+SQSIZE/4, i*SQSIZE +SQSIZE/4, SQSIZE, SQSIZE))
def checkSuccess(screen, board):
    pass
if __name__ == "__main__":
    main()