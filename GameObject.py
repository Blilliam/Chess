import pygame

from Board import Board
import Constants
from Constants import *


class GameObject:

    def __init__(self):
        self.mainBoard = Board()
        self.mainBoard.fillBoard()
        self.isRunning = True
        self.cPiece = None
        self.turn = Constants.WHITE

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

    def clearSelectionAndMoves(self):
        for row in self.mainBoard.board:
            for tile in row:
                tile.isMoveable = False

        for row in self.mainBoard.board:
            for tile in row:
                if tile.isOccupied():
                    tile.piece.isSelected = False

    def selectPiece(self, piece):
        self.clearSelectionAndMoves()
        self.cPiece = piece
        self.cPiece.isSelected = True

        for move in self.cPiece.getMoves():
            row, col = move
            if 0 <= row < 8 and 0 <= col < 8:
                self.mainBoard.board[row][col].isMoveable = True

    def handleClick(self, event):
        cX = event.pos[0] // TILE_SIZE
        cY = event.pos[1] // TILE_SIZE

        if not (0 <= cX < 8 and 0 <= cY < 8):
            return

        clickedTile = self.mainBoard.board[cY][cX]
        tempPiece = self.mainBoard.getPeice(cX, cY)

        

        if self.cPiece != None and (clickedTile.isMoveable) and self.cPiece.team == self.turn:
            originTile = self.mainBoard.board[self.cPiece.y][self.cPiece.x]
            self.cPiece.isSelected = False
            originTile.movePiece(clickedTile)

            self.clearSelectionAndMoves()
            

            self.turn = Constants.getOppColor(self.turn)
            return

        if tempPiece is not None:
            if self.cPiece is tempPiece and self.cPiece.isSelected:
                self.clearSelectionAndMoves()
                self.cPiece = None
                return

            self.selectPiece(tempPiece)
            return

        self.clearSelectionAndMoves()

        print(self.turn)

            