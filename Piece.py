import pygame
import Board
import Constants

class Piece():


    def __init__(self, team:str, row:int, col:int, path:str, mainBoard:Board):
        # Store the piece's team, position, sprite, and link to the board.
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
            for move in self.getLegalMoves():
                self.mainBoard.board[move[0]][move[1]].isMoveable = True

    def draw(self, screen):
        screen.blit(self.img, (self.x * Constants.TILE_SIZE, self.y * Constants.TILE_SIZE))
       


    def getMoves(self) -> list:
        raise NotImplemented

    def getLegalMoves(self) -> list:
        # Test each candidate move on its own fresh board snapshot to avoid
        # mutating the real piece or leaking state between iterations.
        legalMoves = []

        for move in self.getMoves():
            row, col = move
            if not (0 <= row < 8 and 0 <= col < 8):
                continue

            tempBoard = self.mainBoard.createBoardSnapshot(self.mainBoard)
            startTile = tempBoard.board[self.y][self.x]
            targetTile = tempBoard.board[row][col]

            movingPiece = startTile.piece
            if movingPiece is None:
                continue

            if targetTile.isOccupied() and targetTile.piece.team == self.team:
                continue

            startTile.putPiece(None)
            targetTile.putPiece(movingPiece)
            movingPiece.x = targetTile.x
            movingPiece.y = targetTile.y

            king = tempBoard.getKingOnBoard(self.team)
            if not tempBoard.isBoardInCheck(king):
                legalMoves.append(move)

        return legalMoves

    def getCopy(self, board) -> "Piece":
        copyPiece = self.__class__.__new__(self.__class__)
        copyPiece.team = self.team
        copyPiece.x = self.x
        copyPiece.y = self.y
        copyPiece.img = self.img
        copyPiece.mainBoard = board
        copyPiece.hasMoved = self.hasMoved
        copyPiece.isSelected = False
        return copyPiece



class Pawn(Piece):
    def getMoves(self) -> list:
        # Pawns move forward, capture diagonally, and can move two squares from their start.
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
                if self.mainBoard.board[row][col].isOccupied() or self.mainBoard.passantTile == (row, col):
                    moves.append([row, col])


        

        return moves

class King(Piece):

    def getMoves(self, includeCastling = True) -> list:
        # Kings move one square in any direction.
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



        if includeCastling and not self.hasMoved: #if havent moved
            oppMoves = self.mainBoard.getAllOppMoves(self.team)

            if (self.y, self.x) not in oppMoves: #if not in check
                rookTile = self.mainBoard.board[self.y][0]

                for i in range(-1, 2, 2):
                    if (rookTile.isOccupied() and isinstance(rookTile.piece, Rook)):
                        if (not rookTile.piece.hasMoved):
                            #empy check
                            isEmpty = not any(self.mainBoard.board[self.y][i].isOccupied() for i in range(1, self.x))
                            isSafe = (self.y, self.x+i) not in oppMoves and (self.y, self.x+2 * i) not in oppMoves
                            if isEmpty and isSafe:
                                moves.append([self.y, self.x+2 * i])
                    rookTile = self.mainBoard.board[self.y][ 7]



        # if (not self.hasMoved and (self.y, self.x) not in self.mainBoard.getAllOppMoves(self.team, True)):
        #     print(self.mainBoard.board[self.y][0].piece, self.y)
        #     if (not self.mainBoard.board[self.y][0].piece.hasMoved):
        #         if ((not (self.y, 2) in self.mainBoard.getAllOppMoves(self.team)) and not self.mainBoard.board[self.y][2].isOccupied()):
        #             if ((not (self.y, 3) in self.mainBoard.getAllOppMoves(self.team))and not self.mainBoard.board[self.y][3].isOccupied()):
        #                 if (not self.mainBoard.board[self.y][1].isOccupied()):
        #                     moves.append([self.y, self.x-2])

        #     if (not self.mainBoard.board[self.y][7].piece.hasMoved):
        #         if ((not (self.y, 6) in self.mainBoard.getAllOppMoves(self.team)) and not self.mainBoard.board[self.y][6].isOccupied()):
        #             if ((not (self.y, 5) in self.mainBoard.getAllOppMoves(self.team))and not self.mainBoard.board[self.y][5].isOccupied()):
        #                 moves.append([self.y, self.x+2])
                    

            

        
                        
        return moves

class Queen(Piece):
    def getMoves(self):
        # Queens move like a rook and bishop combined.
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
        # Rooks move horizontally or vertically until blocked.
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
        # Bishops move diagonally until blocked.
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
        # Knights move in an L-shape and are not blocked by pieces in between.
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