import pygame
import Piece
import Constants
import os
import Constants
from PIL import Image, ImageDraw
import Board

class Tile() :
    def __init__(self, row:int, col:int, color:list, mainBoard:Board, piece:Piece = None):
        self.piece = piece
        self.color = color
        self.x = col
        self.y = row
        self.isMoveable = False
        self.mainBoard = mainBoard
    
    def update(self) -> None:
        if self.piece != None:
            self.piece.update()

    def draw(self, screen) -> None:

        pygame.draw.rect(screen, self.color, [self.x * Constants.TILE_SIZE + Constants.BOARDX, self.y * Constants.TILE_SIZE + Constants.BOARDY,Constants.TILE_SIZE, Constants.TILE_SIZE])

        if (self.isOccupied()):
            self.piece.draw(screen)
        elif(self.isMoveable):
            pygame.draw.circle(screen, [100,100,100], (self.x * Constants.TILE_SIZE + Constants.BOARDX + Constants.TILE_SIZE/2, self.y * Constants.TILE_SIZE + Constants.BOARDY + Constants.TILE_SIZE/2), Constants.TILE_SIZE/4)
    
        
    def putPiece(self, peice):
        self.piece = peice

    def isOccupied(self) -> bool:
        return not self.piece == None
    


            

    