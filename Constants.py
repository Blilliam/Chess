import os 
import pygame 

WHITE = "white" 
BLACK = "black" 
TILE_SIZE = 64 
COLOR1 = [0, 0 , 0] 
COLOR2 = [255, 255, 255] 

BOARDX = 0
BOARDY = 0

def getOppColor(color):
    return BLACK if color == WHITE else WHITE