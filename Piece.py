import pygame
import Board
import Constants

class Piece():


    def __init__(self, team:str, row:int, col:int, path:str, mainBoard:Board):
        self.team = team
        startString = "Images/"
        if team == Constants.BLACK:
            startString += "Black/"
        else:
            startString += "White/"
        self.img = pygame.image.load(startString + path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (Constants.TILE_SIZE, Constants.TILE_SIZE))
        self.x = col
        self.y = row
        self.isSelected = False
        self.mainBoard = mainBoard

    def update(self):
        ...

    def draw(self, screen):
        screen.blit(self.img, (self.x * Constants.TILE_SIZE, self.y * Constants.TILE_SIZE))
        if self.isSelected:
            for move in self.getMoves():
                self.mainBoard.board[move[0]][move[1]].isMoveable = True


    def getMoves(self) -> list:
        raise NotImplemented

class Pawn(Piece):
    def getMoves(self) -> list:
        moves = []
        
        direction = -1 
        if self.team == Constants.WHITE:
            direction = 1
        
        row = self.y + direction
        col = self.x
        
        if 0 <= row < 8 and 0 <= col < 8:
            if not self.mainBoard.board[row][col].isOccupied():
                moves.append([row, col])
                
        return moves

class King(Piece):
    def getMoves(self) -> list:
        moves = []
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                
                row = self.y + dy
                col = self.x + dx

                if 0 <= row < 8 and 0 <= col < 8:
                    if not self.mainBoard.board[row][col].isOccupied():
                        moves.append([row, col])
                        
        return moves

class Queen(Piece):
    def getMoves(self):
        moves = []
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                step = 1
                while True:
                    row = self.y + (dy * step)
                    col = self.x + (dx * step)
                    
                    if not (0 <= row < 8 and 0 <= col < 8):
                        break
                        
                    square = self.mainBoard.board[row][col]
                    
                    if not square.isOccupied():
                        moves.append([row, col])
                        step += 1
                    else:
                        if square.piece.team != self.team:
                            moves.append([row, col])
                        break
                    
        return moves

class Rook(Piece):
    def getMoves(self):
        moves = []
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                step = 1
                while True:
                    row = self.y + (dy * step)
                    col = self.x + (dx * step)
                    
                    if not (0 <= row < 8 and 0 <= col < 8):
                        break
                    if not (dx == 0 or dy == 0):
                        break
                        
                    square = self.mainBoard.board[row][col]
                    
                    if not square.isOccupied():
                        moves.append([row, col])
                        step += 1
                    else:
                        if square.piece.team != self.team:
                            moves.append([row, col])
                        break
                    
        return moves

class Bishop(Piece):
    def getMoves(self):
        moves = []
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                step = 1
                while True:
                    row = self.y + (dy * step)
                    col = self.x + (dx * step)
                    
                    if not (0 <= row < 8 and 0 <= col < 8):
                        break
                    if  dx == 0 or dy == 0:#only change between bishop and rook
                        break
                        
                    square = self.mainBoard.board[row][col]
                    
                    if not square.isOccupied():
                        moves.append([row, col])
                        step += 1
                    else:
                        if square.piece.team != self.team:
                            moves.append([row, col])
                        break
                    
        return moves

class Knight(Piece):
    def getMoves(self):
        ...