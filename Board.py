import pygame
import Tile
from Tile import Tile
from Piece import *
from Constants import *

class Board: 
    def __init__(self):
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            for j in range(8):
                color = Constants.COLOR1
                if (i+j) % 2 == 0:
                    color = Constants.COLOR2
                self.board[i][j] = Tile(i, j, color, self)
                
    def getPeice(self, x, y):
        if (0 <= x <= 7 and 0 <= y <= 7):
            if (self.board[y][x].isOccupied()):
                return self.board[y][x].piece
        return None

    def update(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j].update()

    def draw(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j].draw(screen)

    def fillBoard(self):
        
        self.board[0][0].putPiece(Rook(WHITE, 0, 0, "WhiteRook.png", self))
        self.board[0][1].putPiece(Knight(WHITE, 0, 1, "WhiteKnight.png", self))
        self.board[0][2].putPiece(Bishop(WHITE, 0, 2, "WhiteBishop.png", self))
        self.board[0][3].putPiece(Queen(WHITE, 0, 3, "WhiteQueen.png", self))
        self.board[0][4].putPiece(King(WHITE, 0, 4, "WhiteKing.png", self))
        self.board[0][5].putPiece(Bishop(WHITE, 0, 5, "WhiteBishop.png", self))
        self.board[0][6].putPiece(Knight(WHITE, 0, 6, "WhiteKnight.png", self))
        self.board[0][7].putPiece(Rook(WHITE, 0, 7, "WhiteRook.png", self))
        

        for j in range(8):
            self.board[1][j].putPiece(Pawn(WHITE, 1, j,"WhitePawn.png", self))

        self.board[7][0].putPiece(Rook(BLACK, 7, 0, "BlackRook.png", self))
        self.board[7][1].putPiece(Knight(BLACK, 7, 1, "BlackKnight.png", self))
        self.board[7][2].putPiece(Bishop(BLACK, 7, 2, "BlackBishop.png", self))
        self.board[7][3].putPiece(Queen(BLACK, 7, 3, "BlackQueen.png", self))
        self.board[7][4].putPiece(King(BLACK, 7, 4, "BlackKing.png", self))
        self.board[7][5].putPiece(Bishop(BLACK, 7, 5, "BlackBishop.png", self))
        self.board[7][6].putPiece(Knight(BLACK, 7, 6, "BlackKnight.png", self))
        self.board[7][7].putPiece(Rook(BLACK, 7, 7, "BlackRook.png", self))
        

        for j in range(8):
            self.board[6][j].putPiece(Pawn(BLACK, 6, j, "BlackPawn.png", self))
        

        #self.board[3][3].putPiece(Bishop(WHITE, 3, 3, "WhiteBishop.png", self))     
