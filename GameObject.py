import pygame

from Board import Board
import Constants
from Constants import *
import Piece


class GameObject:

    def __init__(self):
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
        for row in self.mainBoard.board:
            for tile in row:
                tile.isMoveable = False

        for row in self.mainBoard.board:
            for tile in row:
                if tile.isOccupied():
                    tile.piece.isSelected = False

    def getKingOnBoard(self, board, team) -> Piece:
        for row in board.board:
            for tile in row:
                if tile.isOccupied() and isinstance(tile.piece, Piece.King) and tile.piece.team == team:
                    return tile.piece
        return None

    def createBoardSnapshot(self, sourceBoard=None):
        boardToCopy = self.mainBoard if sourceBoard is None else sourceBoard
        snapshotBoard = Board()
        for row in range(8):
            for col in range(8):
                sourceTile = boardToCopy.board[row][col]
                targetTile = snapshotBoard.board[row][col]
                if sourceTile.isOccupied():
                    piece = sourceTile.piece
                    targetTile.putPiece(piece)
                    piece.mainBoard = snapshotBoard
                    piece.x = col
                    piece.y = row
        return snapshotBoard

    def isBoardInCheck(self, board, king) -> bool:
        if king is None:
            return False

        allOppMoves = []
        for row in board.board:
            for tile in row:
                if tile.isOccupied() and king.team == Constants.getOppColor(tile.piece.team):
                    for move in tile.piece.getMoves():
                        allOppMoves.append(tuple(move))

        return (king.y, king.x) in allOppMoves

    def getLegalMoves(self, piece):
        self.pastBoard = self.createBoardSnapshot(self.mainBoard)
        legalMoves = []

        for move in piece.getMoves():
            row, col = move
            if not (0 <= row < 8 and 0 <= col < 8):
                continue

            simulatedBoard = self.createBoardSnapshot(self.pastBoard)
            originTile = simulatedBoard.board[piece.y][piece.x]
            targetTile = simulatedBoard.board[row][col]
            movingPiece = originTile.piece

            if targetTile.isOccupied() and targetTile.piece.team == movingPiece.team:
                continue

            originalX = movingPiece.x
            originalY = movingPiece.y
            originalBoard = movingPiece.mainBoard
            targetTile.putPiece(None)
            targetTile.putPiece(movingPiece)
            originTile.putPiece(None)
            movingPiece.x = targetTile.x
            movingPiece.y = targetTile.y

            king = self.getKingOnBoard(simulatedBoard, piece.team)
            if not self.isBoardInCheck(simulatedBoard, king):
                legalMoves.append(move)

            movingPiece.mainBoard = originalBoard
            movingPiece.x = originalX
            movingPiece.y = originalY

        return legalMoves

    def selectPiece(self, piece):
        self.clearSelectionAndMoves()
        self.cPiece = piece
        self.cPiece.isSelected = True

        for move in self.getLegalMoves(piece):
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

        if self.isInCheck(self.getKing(self.turn)):
            self.pastBoard = self.createBoardSnapshot(self.mainBoard)

        if self.cPiece != None and (clickedTile.isMoveable) and self.cPiece.team == self.turn:
            originTile = self.mainBoard.board[self.cPiece.y][self.cPiece.x]
            self.cPiece.isSelected = False
            originTile.movePiece(clickedTile)

            self.clearSelectionAndMoves()
            self.isInCheck(self.getKing(Constants.getOppColor(self.turn)))
            

            self.turn = Constants.getOppColor(self.turn)
            return

        if tempPiece is not None:
            if self.cPiece is tempPiece and self.cPiece.isSelected:
                self.clearSelectionAndMoves()
                self.isInCheck(self.getKing(Constants.getOppColor(self.turn)))
                self.cPiece = None
                return

            self.selectPiece(tempPiece)
            return

        self.clearSelectionAndMoves()
        self.isInCheck(self.getKing(Constants.getOppColor(self.turn)))
        

    def getKing(self, team) -> Piece:
        for row in self.mainBoard.board:
            for tile in row:
                if (tile.isOccupied() and isinstance(tile.piece, Piece.King) and tile.piece.team == team):
                    return tile.piece


    def isInCheck(self, king=None) -> bool:
        if king is None:
            king = self.getKing(self.turn)

        if king is None:
            return False

        allOppMoves = []
        for row in self.mainBoard.board:
            for tile in row:
                if tile.isOccupied() and king.team == Constants.getOppColor(tile.piece.team):
                    for move in tile.piece.getMoves():
                        allOppMoves.append(tuple(move))
        for y, x in allOppMoves:
            if king.x == x and king.y == y:
                return True
        return False


            