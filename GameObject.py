import copy

import pygame

from Board import Board
import Constants
from Constants import *
import Piece 


class GameObject:

    def __init__(self):
        # Create the main board and initialize the game state.
        self.mainBoard = Board()
        self.mainBoard.fillBoard()
        self.pastBoard = Board()
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
        # Reset all move highlights and clear any previously selected piece.
        for row in self.mainBoard.board:
            for tile in row:
                tile.isMoveable = False

        for row in self.mainBoard.board:
            for tile in row:
                if tile.isOccupied():
                    tile.piece.isSelected = False


    def selectPiece(self, piece):
        # Clear old highlights, then mark the chosen piece as selected and show its legal moves.
        self.clearSelectionAndMoves()
        self.cPiece = piece
        self.cPiece.isSelected = True

        for move in piece.getLegalMoves():
            row, col = move
            if 0 <= row < 8 and 0 <= col < 8:
                self.mainBoard.board[row][col].isMoveable = True


    def handleClick(self, event):
        # Convert the mouse position into a board coordinate.
        cX = event.pos[0] // TILE_SIZE
        cY = event.pos[1] // TILE_SIZE

        if not (0 <= cX < 8 and 0 <= cY < 8):
            return

        clickedTile = self.mainBoard.board[cY][cX]  # clicked tile
        tempPiece = self.mainBoard.getPeice(cX, cY)  # clicked piece

        # Keep a snapshot before a move if the current side is in check.
        if self.mainBoard.isBoardInCheck(self.mainBoard.getKingOnBoard(self.turn)):
            self.pastBoard = self.mainBoard.createBoardSnapshot(self.mainBoard)

        # Try to move the selected piece to the clicked tile if the move is legal.
        if self.cPiece != None and (clickedTile.isMoveable) and self.cPiece.team == self.turn:
            originTile = self.mainBoard.board[self.cPiece.y][self.cPiece.x]
            self.cPiece.isSelected = False

            originTile.movePiece(clickedTile)

            self.clearSelectionAndMoves()
            self.mainBoard.isBoardInCheck(self.mainBoard.getKingOnBoard(Constants.getOppColor(self.turn)))

            self.turn = Constants.getOppColor(self.turn)
            return

        # Allow clicking the same piece again to deselect it.
        if tempPiece is not None:
            if self.cPiece is tempPiece and self.cPiece.isSelected:
                self.clearSelectionAndMoves()
                self.mainBoard.isBoardInCheck(self.mainBoard.getKingOnBoard(Constants.getOppColor(self.turn)))
                self.cPiece = None
                return

            self.selectPiece(tempPiece)
            return

        # Clicking an empty tile clears the current selection.
        self.clearSelectionAndMoves()
        self.mainBoard.isBoardInCheck(self.mainBoard.getKingOnBoard(Constants.getOppColor(self.turn)))
        


            