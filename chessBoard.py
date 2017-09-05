# Kevin Chen

import pygame
from boardSquare import *
from pieceClass import *


class chessBoard():
  def __init__(self, screen, imageNameList):
    rectDict = {}
    pieceDict = {}

    imageList = []
    for eachName in imageNameList:
      imageList.append(pygame.image.load(eachName).convert_alpha())

    imageTuple = tuple(imageList)

    # Assign the following variables to images using tuple assignment
    (selSquareGrn, bishopWhite, bishopBlack, kingBlack, kingWhite, \
     knightWhite, knightBlack, pawnWhite, pawnBlack, queenWhite, \
     queenBlack, rookWhite, rookBlack) = imageTuple


    # Populate a dictionary with boardSquares that have indexTuples
    #   as their keys
    for columnIndex in range(8):
      for rowIndex in range(8):
        eachSquare = boardSquare((rowIndex, columnIndex))
        rectDict[(rowIndex, columnIndex)] = eachSquare
        eachSquare.drawBlank()

        rectDict[(rowIndex,columnIndex)] = eachSquare

    # Init each piece class      
    Piece.initMe(screen, self, selSquareGrn)
    
    Rook.initMe(screen, rookWhite, rookBlack)
    Bishop.initMe(screen, bishopWhite, bishopBlack)
    Knight.initMe(screen, knightWhite, knightBlack)
    Pawn.initMe(screen, pawnWhite, pawnBlack)
    King.initMe(screen, kingWhite, kingBlack)
    Queen.initMe(screen, queenWhite, queenBlack)

    # Substantiate eachPiece
    pieceDict['rookBlackA'] = Rook(BLACK, (0,0), ROOK, 'rookBlackA')
    pieceDict['rookBlackB'] = Rook(BLACK, (7,0), ROOK, 'rookBlackB')
    pieceDict['knightBlackA'] = Knight(BLACK, (1,0), KNIGHT, 'knightBlackA')
    pieceDict['knightBlackB'] = Knight(BLACK, (6,0), KNIGHT, 'knightBlackB')
    pieceDict['bishopBlackA'] = Bishop(BLACK, (2,0), BISHOP, 'bishopBlackA')
    pieceDict['bishopBlackB'] = Bishop(BLACK, (5,0), BISHOP, 'bishopBlackB')
    pieceDict['queenBlack'] = Queen(BLACK, (3,0), QUEEN, 'queenBlack')
    pieceDict['kingBlack'] = King(BLACK, (4,0), KING, 'kingBlack')

    pieceDict['rookWhiteA'] = Rook(WHITE, (0,7), ROOK, 'rookWhiteA')
    pieceDict['rookWhiteB'] = Rook(WHITE, (7,7), ROOK, 'rookWhiteB')
    pieceDict['knightWhiteA'] = Knight(WHITE, (1,7), KNIGHT, 'knightWhiteA')
    pieceDict['knightWhiteB'] = Knight(WHITE, (6,7), KNIGHT, 'knightWhiteB')
    pieceDict['bishopWhiteA'] = Bishop(WHITE, (2,7), BISHOP, 'bishopWhiteA')
    pieceDict['bishopWhiteB'] = Bishop(WHITE, (5,7), BISHOP, 'bishopWhiteB')
    pieceDict['queenWhite'] = Queen(WHITE, (3,7), QUEEN, 'queenWhite')
    pieceDict['kingWhite'] = King(WHITE, (4,7), KING, 'kingWhite')

    pawnNameList = ['pawnBlackA', 'pawnBlackB', 'pawnBlackC', 'pawnBlackD', \
                    'pawnBlackE', 'pawnBlackF', 'pawnBlackG', 'pawnBlackH', \
                    'pawnWhiteA', 'pawnWhiteB', 'pawnWhiteC', 'pawnWhiteD', \
                    'pawnWhiteE', 'pawnWhiteF', 'pawnWhiteG', 'pawnWhiteH']
    
    for column in range(8):
      pieceDict[pawnNameList[column]] = Pawn(BLACK, (column,1), PAWN, \
                                             pawnNameList[column])

    for column in range(8):
      pieceDict[pawnNameList[column+8]] = Pawn(WHITE, (column,6), PAWN, \
                                               pawnNameList[column+8])

    piecePosDict = {}
    for eachPiece in pieceDict.items():
      eachPiece[1].drawMe()
      piecePosDict[eachPiece[0]] = eachPiece[1].getCurrentPosition()
      

    pygame.display.update()
    ##print('rectDict: %s \nType: %s' % (rectDict,type(rectDict)))
    self.__rectDict = rectDict
    self.__pieceDict = pieceDict
    self.__piecePosDict = piecePosDict

  # param givenIndex (tuple)
  def getIndexFromCoord(self, givenIndex):
    return self.__rectDict[givenIndex].getIndexTuple()

  # param givenIndex (tuple)
  def getCoordFromIndex(self, givenIndex):
    return self.__rectDict[givenIndex].getCoordTuple()

  def getRectDict(self):
    return self.__rectDict

  def getBoardSquareDict(self):
    return self.__rectDict

  def getBoardSquareList(self):
    return self.__rectDict.values()

  def getPieceDict(self):
    return self.__pieceDict

  def getPieceDictOneColor(self, color):
    newPieceDict = {}
    for (k,v) in self.__pieceDict.items():
      if v.getColor() == color:
        newPieceDict[k] = v
    return newPieceDict

  def getPiecePosDict(self):
    return self.__piecePosDict

  def clearSelected(self):
    for eachSq in self.getBoardSquareList():
      eachSq.eraseSelect()

  def delPiece(self, piece):
    piecePos = piece.getCurrentPosition()
    self.__rectDict[piecePos].drawBlank()
    del self.__pieceDict[piece.getName()]
    ##print('deleting piece now')

  def isOccupied(self, pos):
    isOccupied = False
    for eachPiece in self.__pieceDict.values():
      if eachPiece.getCurrentPosition() == pos:
        isOccupied = True
    return isOccupied

  def isOccupiedBy(self, pos):
    occupyingPiece = None
    for eachPiece in self.__pieceDict.values():
      if eachPiece.getCurrentPosition() == pos:
        occupyingPiece = eachPiece
    return occupyingPiece

  def isCheck(self, color):
    isCheck = False
    kingName = 'king' + ('White' if color==WHITE else 'Black')
    for eachPiece in self.getPieceDictOneColor(not(color)).values():
      for eachMove in eachPiece.getMoves():
        if eachMove == self.__pieceDict[kingName].getCurrentPosition():
          isCheck = True
    return isCheck

  def canMoveWhileInCheck(self, color):
    canMove = False
    for eachPiece in self.getPieceDictOneColor(color).values():
      if eachPiece.canMove():
        canMove = True
    return canMove





 
