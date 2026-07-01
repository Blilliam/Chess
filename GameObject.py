import pygame

from Board import Board
from Constants import *


class GameObject:

    def __init__(self):
        self.mainBoard = Board()
        self.mainBoard.fillBoard()
        self.isRunning = True

    def draw(self, screen):
        self.mainBoard.draw(screen)

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handleClick(event)

    def handleClick(self, event):
        cCol = event.pos[0] // TILE_SIZE
        cRow = event.pos[1] // TILE_SIZE

        cTile = self.mainBoard.board[cRow][cCol]
        selTile = None

        for i in range(len(self.mainBoard.board)):
            for j in range(len(self.mainBoard.board[i])):
                tile = self.mainBoard.board[i][j]
                if tile.isOccupied() and tile.piece.isSelected:
                    selTile = tile
                    break
            if selTile:
                break

        if selTile is not None and cTile.isMoveable:
            selTile.piece.isSelected = False
            
            cTile.putPiece(selTile.piece)
            selTile.putPiece(None)
            
            if cTile.piece:
                cTile.piece.x = cCol
                cTile.piece.y = cRow

        elif cTile.isOccupied():
            cTile.piece.isSelected = True

        for i in range(len(self.mainBoard.board)):
            for j in range(len(self.mainBoard.board[i])):
                self.mainBoard.board[i][j].isMoveable = False
                if self.mainBoard.board[i][j].isOccupied():
                    self.mainBoard.board[i][j].isSelected = False

            
            