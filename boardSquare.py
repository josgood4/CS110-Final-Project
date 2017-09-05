# Collaborative

import pygame

BLACK = 0
WHITE = 1

(PAWN, BISHOP, KNIGHT, ROOK, QUEEN, KING) = (0,1,2,3,4,5)

SQUARE_SIZE = 50
X_BORDER = 100
Y_BORDER = 100

# boardSquare class - a class that represents each square on the chess board
# WHEN USING THIS CLASS, BE SURE TO CALL boardSquare.initMe() and 
#   send it the appropriate arguments
# When doing work with the class, it's easiest to manipulate
#   and refer to squares by their __indexTuple
#   which is of the form: (row, column) each item ranging from 0 to 7
#   (0,0) is the top-left square on the board

class boardSquare():
  # Class variables
  LETTER_LIST = ['a','b','c','d','e','f','g','h']
  NUMBER_LIST = ['8', '7', '6', '5', '4', '3', '2', '1']

  #---------------------------------------------------------------------
  # Constructor
  
  # param indexTuple (tuple) - (rowIndex, columnIndex)
  #   where rowIndex is the index of the row on the chess board
  #     (starting at zero); and columnIndex likewise 
  def __init__(self,indexTuple):
    #self.__player = player
    self.__indexTuple = indexTuple
    self.__coordTuple = (X_BORDER + self.__indexTuple[0] * \
                          SQUARE_SIZE, Y_BORDER + \
                          self.__indexTuple[1] * SQUARE_SIZE)
    self.__rect = pygame.Rect(self.__coordTuple,(SQUARE_SIZE, SQUARE_SIZE))
    self.__chessAlgebra = boardSquare.LETTER_LIST[indexTuple[0]] + \
                          boardSquare.NUMBER_LIST[indexTuple[1]]


  # CALL THIS BEFORE USING THE boardSquare CLASS
  # param screen - a previously initialized pygame display
  # param imageNameList - a list containing the following previously
  #       loaded images (in this order):
  #       [whiteSquare, blackSquare, selSquareWhite,
  #         selSquareBlack, selSquareGreen]
  @classmethod
  def initMe(cls, screen, imageNameList):

    boardSquare.screen = screen

    imageList = []
    for eachImage in imageNameList:
      imageList.append(pygame.image.load(eachImage).convert_alpha())
    imageTuple = tuple(imageList)
    
    (boardSquare.whiteSquare, boardSquare.blackSquare, \
     boardSquare.selSquareWhite, boardSquare.selSquareBlack, \
     boardSquare.selSquareGreen) = imageTuple

  #---------------------------------------------------------------------
  # Predicates

  # returns True if square is white, False otherwise
  def isWhiteSquare(self):
    return self.__indexTuple[0] % 2 == self.__indexTuple[1] % 2

  #---------------------------------------------------------------------  
  # Accessors
  def getIndexTuple(self):
    return self.__indexTuple
  
  def getSize(self):
    return self.__size

  def getCoordTuple(self):
    return self.__coordTuple

  def getRect(self):
    return self.__rect

  def getAlgebra(self):
    return self.__chessAlgebra
  
  #---------------------------------------------------------------------
  # Mutators
  def drawBlank(self):
    if self.isWhiteSquare():
      boardSquare.screen.blit(boardSquare.whiteSquare, self.__rect)        
    else:
      boardSquare.screen.blit(boardSquare.whiteSquare, self.__rect)        
      boardSquare.screen.blit(boardSquare.blackSquare, self.__rect)
      
  def eraseSelect(self):
    if self.isWhiteSquare():
      boardSquare.screen.blit(boardSquare.selSquareWhite, self.__rect)        
    else:
      boardSquare.screen.blit(boardSquare.selSquareWhite, self.__rect)        
      boardSquare.screen.blit(boardSquare.selSquareBlack, self.__rect)
      
  def drawGreenSelect(self):
    boardSquare.screen.blit(boardSquare.selSquareGreen, self.__rect)


  #---------------------------------------------------------------------
  # toString
  def __str__(self):
    return "The square %s is %s and has rect %s" % (self.__chessAlgebra, \
            'white' if self.isWhiteSquare() else 'black', self.__rect)
