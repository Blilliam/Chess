import pygame

from Board import Board
from Constants import *


class GameObject:

    def __init__(self):
        self.mainBoard = Board()
        self.mainBoard.fillBoard()
        self.isRunning = True
        self.cPiece = None

    def draw(self, screen):
        self.mainBoard.draw(screen)
    
    def update(self):
        self.mainBoard.update()

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handleClick(event)

    def handleClick(self, event):
        cX = event.pos[0] // TILE_SIZE
        cY = event.pos[1] // TILE_SIZE

        tempPiece = self.mainBoard.getPeice(cX, cY)

        if (tempPiece == None): # tile
            cTile = self.mainBoard.board[cY][cX]
            if (cTile.isMoveable and self.cPiece != None):
                cTile.putPiece(self.cPiece)
                self.mainBoard.board[self.cPiece.y][self.cPiece.x].putPiece(None)
                
                if cTile.piece:
                    cTile.piece.x = cX
                    cTile.piece.y = cY
        else: # piece
            self.cPiece = tempPiece
            self.cPiece.isSelected = True

        for i in range(len(self.mainBoard.board)):
            for j in range(len(self.mainBoard.board[i])):
                if self.mainBoard.board[i][j].isOccupied():
                    if (i != cY and j != cX):
                        self.mainBoard.board[i][j].piece.isSelected = False

        for i in range(len(self.mainBoard.board)):
            for j in range(len(self.mainBoard.board[i])):
                self.mainBoard.board[i][j].isMoveable = False

            
            