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
        self.imgPath = startString + path
        self.img = pygame.image.load(self.imgPath).convert_alpha()
        self.img = pygame.transform.scale(self.img, (Constants.TILE_SIZE, Constants.TILE_SIZE))
        self.x = col
        self.y = row
        self.isSelected = False
        self.mainBoard = mainBoard
        self.hasMoved = False

    def update(self):
        if self.isSelected:
            for move in self.getMoves():
                self.mainBoard.board[move[0]][move[1]].isMoveable = True

    def draw(self, screen):
        screen.blit(self.img, (self.x * Constants.TILE_SIZE, self.y * Constants.TILE_SIZE))
       


    def getMoves(self) -> list:
        raise NotImplemented

    def getLegalMoves(self) -> list:
        legalMoves = []

        tempBoard = self.mainBoard.createBoardSnapshot(self.mainBoard)
    
        for move in self.getMoves():
            row, col = move
            if not (0 <= row < 8 and 0 <= col < 8):
                continue
            startTile = tempBoard.board[self.y][self.x]
            targetTile = tempBoard.board[row][col]

            if targetTile.isOccupied() and targetTile.piece.team == self.team:
                continue

            originalX = self.x
            originalY = self.y
            originalBoard = self.mainBoard
            targetTile.putPiece(None)
            targetTile.putPiece(startTile.piece)
            startTile.putPiece(None)
            startTile.piece.x = targetTile.x
            startTile.piece.y = targetTile.y

            king = self.getKingOnBoard(tempBoard, self.team)
            if not self.isBoardInCheck(tempBoard, king):
                legalMoves.append(move)

            movingPiece.mainBoard = originalBoard
            self.x = originalX
            self.y = originalY

        return legalMoves

    def getCopy(self, board) -> Piece:
        copyPiece = self.__class__.__new__(self.__class__)
        copyPiece.team = self.team
        copyPiece.x = self.x
        copyPiece.y = self.y
        copyPiece.img = self.img
        copyPiece.mainBoard = board



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

                if not self.hasMoved:
                    row = self.y + direction *  2

                    if 0 <= row < 8 and 0 <= col < 8:
                        if not self.mainBoard.board[row][col].isOccupied():
                            moves.append([row, col])
                    
        row = self.y + direction
        for i in (-1, 1):
            col = self.x + i
            if 0 <= row < 8 and 0 <= col < 8:
                if self.mainBoard.board[row][col].isOccupied():
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
                    else:
                        if self.mainBoard.board[row][col].piece.team != self.team:
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
        startMoves = [[2, 1],
                 [2, -1],
                 [1, 2],
                 [1, -2],
                 [-1, 2],
                 [-1, -2],
                 [-2, 1],
                 [-2, -1],]
        moves = []

        
        
        for dx, dy in startMoves:
            row = self.y + dy
            col = self.x + dx

            if not (0 <= row < 8 and 0 <= col < 8):
                continue
                
            square = self.mainBoard.board[row][col]
            #if not square.isOccupied():
            moves.append([row, col])

            #else:
                # if square.piece.team != self.team:
                #     moves.append([row, col])
                # break

        return moves