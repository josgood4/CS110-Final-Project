# Joseph Osgood

import pygame
from boardSquare import *
from chessBoard import *

WHITE = 1
BLACK = 0

class Piece(object):
  
  def __init__(self, color, position, pType, name):
    self.__color = color
    self.__type = pType
    self.__position = position   # THIS IS INDEX TUPLE ( (0-7), (0-7) )
    self.__name = name
    self.__lastMove = None
    self.__lastTakenPiece = None
    self.__rect = pygame.Rect(((X_BORDER + self.__position[0] * SQUARE_SIZE),\
                       (Y_BORDER + self.__position[1] * SQUARE_SIZE)), \
                        (SQUARE_SIZE, SQUARE_SIZE))

  # Call this guy first
  @classmethod
  def initMe(cls, screen, board, selSq):
    Piece.screen = screen
    Piece.board = board
    Piece.selSq = selSq

  def isWhite(self):
    return self.__color == WHITE
  
  def drawMe(self):
    Piece.screen.blit(self.getImage(), self.__rect)

  def drawPossibleMoves(self):
    Piece.board.clearSelected()
    for eachPossMove in self.getMoves():
      Piece.screen.blit(Piece.selSq, \
                       Piece.board.getCoordFromIndex(eachPossMove))

  def drawSpecificMoves(self, givenMoves):
    Piece.board.clearSelected()
    for eachPossMove in givenMoves:
      Piece.screen.blit(Piece.selSq, \
                        Piece.board.getCoordFromIndex(eachPossMove))


  def getCurrentPosition(self):
    return self.__position

  def getRect(self):
    return self.__rect

  def getColor(self):
    return self.__color

  def getName(self):
    return self.__name

  def getType(self):
    return self.__type

  def getMoves(self):
    # Accumlate a list of possible moves
    possibleMoveList = []
    # First, pick a direction to iterate through
    for eachMove in self.getDirections():
      # Validation-loop-style, go through eachSquare in that direction
      counter = 1
      newPos = (eachMove[0]*counter + self.__position[0], \
                eachMove[1]*counter + self.__position[1])
      lock = True
      while lock and (self.inBounds(newPos) and \
            (not(Piece.board.isOccupied(newPos)) or \
            self.isOtherPiece(newPos))):
        possibleMoveList.append(newPos)
        newPos = (eachMove[0]*counter + self.__position[0], \
                  eachMove[1]*counter + self.__position[1])
        counter += 1
        # If the square in question has a piece of the other color on it,
        #   add that to the possibleMoveList
        if self.isOtherPiece(newPos) and self.__type != PAWN:
          possibleMoveList.append(newPos)
          lock = False

        # If it's a pawn, king, or knight, only iterate once per 'direction'
        if self.__type in (KING, KNIGHT):
          lock = False

    return possibleMoveList

  def inBounds(self, givenPos):
    return givenPos[0] >= 0 and givenPos[0] < 8 and \
           givenPos[1] >= 0 and givenPos[1] < 8

  def isOtherPiece(self, givenPos):
    pieceList = Piece.board.getPieceDict().values()
    isOtherPiece = False
    for eachPiece in pieceList:
      if givenPos == eachPiece.getCurrentPosition() and \
         eachPiece.getColor() != self.__color:
          isOtherPiece = True
    return isOtherPiece

  def movePiece(self, clickedSq):
    self.__lastMove = self.__position
    Piece.board.clearSelected()
    Piece.board.getRectDict()[self.__position].drawBlank()
    ##print('%s was moved to %s' % (self, self.__position))
    if Piece.board.isOccupied(clickedSq):
      if Piece.board.isOccupiedBy(clickedSq).getColor() != self.getColor():        
        takenPiece = Piece.board.isOccupiedBy(clickedSq)
        self.__lastTakenPiece = takenPiece
        ##print('%s was taken by %s' % (takenPiece, self))
        Piece.board.delPiece(takenPiece)
    else:
      self.__lastTakenPiece = None
    self.__position = clickedSq
    self.updateRect()
    self.drawMe()


  def undoMove(self):
    Piece.board.clearSelected()
    Piece.board.getRectDict()[self.__position].drawBlank()
    
    self.__position = self.__lastMove
    self.updateRect()
    self.drawMe()
    if self.__lastTakenPiece:
      ##print('putting %s back' % self.__lastTakenPiece)
      Piece.board.getPieceDict()[self.__lastTakenPiece.getName()]\
                                    = self.__lastTakenPiece
      self.__lastTakenPiece.drawMe()

  def canMove(self):
    canMove = False
    for eachMove in self.getMoves():
      self.movePiece(eachMove)
      if Piece.board.isCheck(self.getColor()):
        canMove = True
      self.undoMove()
    return canMove

  def updateRect(self):
    self.__rect = pygame.Rect(((X_BORDER + self.__position[0] * SQUARE_SIZE),\
                       (Y_BORDER + self.__position[1] * SQUARE_SIZE)), \
                        (SQUARE_SIZE, SQUARE_SIZE))


  def __str__(self):
    return self.__name + ' is a ' + ('White' if self.__color == WHITE \
            else 'Black') + str(type(self))


    

class Rook(Piece):
  @classmethod
  def initMe(cls, screen, rookW, rookB):
    Rook.__rookWhite = rookW
    Rook.__rookBlack = rookB

  def getImage(self):
    return Rook.__rookWhite if self.isWhite() else Rook.__rookBlack

  def getDirections(self):
    return [(-1,+0),(+1,+0),(+0,-1),(+0,+1)]

class Bishop(Piece):
  @classmethod
  def initMe(cls, screen, bishopW, bishopB):
    Bishop.__bishopWhite = bishopW
    Bishop.__bishopBlack = bishopB

  def getImage(self):
    return Bishop.__bishopWhite if self.isWhite() else Bishop.__bishopBlack

  def getDirections(self):
    return [(-1,-1),(+1,-1),(-1,+1),(+1,+1)]

class Queen(Piece):
  @classmethod
  def initMe(cls, screen, queenW, queenB):
    Queen.__queenWhite = queenW
    Queen.__queenBlack = queenB

  def getImage(self):
    return Queen.__queenWhite if self.isWhite() else Queen.__queenBlack

  def getDirections(self):
    return [(-1,-1),(+1,-1),(-1,+1),(+1,+1),(-1,+0),(+1,+0),(+0,-1),(+0,+1)]

class Knight(Piece):
  @classmethod
  def initMe(cls, screen, knightW, knightB):
    Knight.__knightWhite = knightW
    Knight.__knightBlack = knightB

  def getImage(self):
    return Knight.__knightWhite if self.isWhite() else Knight.__knightBlack

  def getDirections(self):
    return [(-1,-2),(+1,-2),(-2,-1),(+2,-1),(-1,+2),(+1,+2),(-2,+1),(2,+1)]

class King(Piece):
  @classmethod
  def initMe(cls, screen, kingW, kingB):
    King.__kingWhite = kingW
    King.__kingBlack = kingB

  def getImage(self):
    return King.__kingWhite if self.isWhite() else King.__kingBlack

  def getDirections(self):
    return [(-1,-1),(+1,-1),(-1,+1),(+1,+1),(-1,+0),(+1,+0),(+0,-1),(+0,+1)]

class Pawn(Piece):
  
  @classmethod
  def initMe(cls, screen, pawnW, pawnB):
    Pawn.__pawnWhite = pawnW
    Pawn.__pawnBlack = pawnB

  def getImage(self):
    return Pawn.__pawnWhite if self.isWhite() else Pawn.__pawnBlack

  def getMoves(self):
    multiplier = 1
    initialRow = 1
    if self.isWhite():
      multiplier = -1
      initialRow = 6
          
    directionList = [(0,+1*multiplier)]
    
    numOfMoves = 1
    counter = 1

    # check if pawn hasn't moved yet
    if self.getCurrentPosition()[1] == initialRow:
      numOfMoves = 2
    
    # Accumlate a list of possible moves
    possibleMoveList = []
    # First, pick a direction to iterate through
    for eachMove in directionList:
      newPos = (eachMove[0]*counter + self.getCurrentPosition()[0], \
                eachMove[1]*counter + self.getCurrentPosition()[1])
      while self.inBounds(newPos) and not(Piece.board.isOccupied(newPos)) \
            and counter <= numOfMoves:
        possibleMoveList.append(newPos)
        counter += 1
        newPos = (eachMove[0]*counter + self.getCurrentPosition()[0], \
                  eachMove[1]*counter + self.getCurrentPosition()[1])

    diagonalMoves = [(+1,1*multiplier),(-1,1*multiplier)]
    # see if pawn can take diagonally
    for eachMove in diagonalMoves:
      newPos = (eachMove[0] + self.getCurrentPosition()[0], \
                 eachMove[1] + self.getCurrentPosition()[1])
      if  self.inBounds(newPos) and Piece.board.isOccupied(newPos):
        if Piece.board.isOccupiedBy(newPos).getColor() != self.getColor():
          possibleMoveList.append(newPos)

    return possibleMoveList

