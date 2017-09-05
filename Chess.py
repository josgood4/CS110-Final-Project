'''
Joseph Osgood and Kevin Chen
josgood2@bing
kchen107@bing
CS 110, Final Project
'''

'''
Some miscellaneaous notes:
Only works with Python 2.7 (on a Mac)
Make sure to have pygame installed
The coordinate system in pygame has (0,0) in the top left
  positive x values are to the right of that
  POSITIVE Y VALUES are BELOW that
If you're using a device with a retina display,
  be sure to set pygame to run in low resolution mode
'''

# Collaborative
# ALWAYS call these guys:
import pygame
import sys
from boardSquare import *
from chessBoard import *
from pieceClass import *

BACKGROUND_COLOR = (255,255,255)

PIECE_IMAGE_NAME_LIST = ['selectedSquareGreen.png','bishopWhite.png', \
                 'bishopBlack.png', 'kingBlack.png', 'kingWhite.png',
                 'knightWhite.png', 'knightBlack.png', 'pawnWhite.png', \
                 'pawnBlack.png', 'queenWhite.png', 'queenBlack.png',
                 'rookWhite.png', 'rookBlack.png']

BOARD_IMAGE_NAME_LIST = ['whiteSquare.png', 'blackSquare.png', \
                      'selectedSquareWhite.png', 'selectedSquareBlack.png',\
                      'selectedSquareGreen.png']
 
class GUIClass:

  def __init__(self):
      
    pygame.init()
    
    # make a screen:
    screen = pygame.display.set_mode((600, 600))
    screen.fill(BACKGROUND_COLOR)
    
    boardSquare.initMe(screen, BOARD_IMAGE_NAME_LIST)

    GUIClass.myBoard = chessBoard(screen, PIECE_IMAGE_NAME_LIST)

    self.__lock = False
    self.__turn = WHITE
    self.__isInCheck = False

    # loop of game
    while True:
      
      # how to quit loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.quitGame()
          
        # so this checks to see if the mouse button went up       
        if event.type == pygame.MOUSEBUTTONUP:
          
          # then it gets the mouse's position                     
          mousePos = pygame.mouse.get_pos()
          
          # so long as you're NOT in check...
          if not(GUIClass.myBoard.isCheck(self.__turn)):
            # and for all the pieces of your color...
            if not(self.__lock):
              self.firstClick(mousePos)
              

            # the self.__lock is flipped after someone clicks  
            #   on one of their own pieces
            #   for the first time on their self.__turn
            if self.__lock:
              # You can sill click on your own pieces
              self.firstClick(mousePos)

              self.clickPossibleMoveNoCheck(mousePos)


          
          # if you ARE in check...
          if self.__isInCheck:        
            ##print('lower part of loop now')
            self.firstClick(mousePos)
              

            # the self.__lock is flipped after someone clicks  
            #   on one of their own pieces
            #   for the first time on their self.__turn
            if self.__lock:
              # You can sill click on your own pieces
              self.firstClick(mousePos)

              self.clickPossibleMoveIsCheck(mousePos)



  def quitGame(self):
    # pygame.QUIT refers to the X at the top-left of the window
    # pygame.KEYDOWN refers to any key being pressed
    # if you use: from pygame.locals import *    ...
    #   you won't need the 'pygame.'
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    # do all three of the above for things to close properly

  def firstClick(self, mousePos):
    for eachPiece in GUIClass.myBoard.getPieceDictOneColor(self.__turn).values():
      # if a specific square was clicked...
      if eachPiece.getRect().collidepoint(mousePos):
        ##print('piece clicked')
        # display the possible moves
        eachPiece.drawPossibleMoves()
        pygame.display.update()
        self.__lock = True
        self.__clickedPiece = eachPiece
        ##pygame.time.delay(1000)
        
  def clickPossibleMoveNoCheck(self, mousePos):
    # or you can click on a possible move
    for eachNewPos in self.__clickedPiece.getMoves():
      ##print(eachNewPos)
      # so long as the place you're going isn't already occupied...
      if GUIClass.myBoard.getRectDict()[eachNewPos].getRect().\
         collidepoint(mousePos): #and \
         #not(GUIClass.myBoard.isOccupied(eachNewPos)):

        # move the piece and flip self.__turns
        self.__clickedPiece.movePiece(eachNewPos)
        # see if you put yourself in check
        if GUIClass.myBoard.isCheck(self.__clickedPiece.getColor()):
          # if so, undo that move
          ##print('you just moved into check')
          self.__clickedPiece.undoMove()
        # if not, proceed
        else:
          ##print("you're good move on")
          self.__turn = not(self.__clickedPiece.getColor())
          # see if you put your opponent in check
        if GUIClass.myBoard.isCheck(not(self.__clickedPiece.getColor())):
          ##print('you put your opponent in check!')
          self.__isInCheck = True

          
        pygame.display.update()
        self.__lock = False
        pygame.time.delay(1000)

  def clickPossibleMoveIsCheck(self, mousePos):
    # or you can click on a possible move
    for eachNewPos in self.__clickedPiece.getMoves():
      ##print(eachNewPos)
      # so long as the place you're going isn't already occupied...
      if GUIClass.myBoard.getRectDict()[eachNewPos].getRect().\
         collidepoint(mousePos): # and \
         #not(GUIClass.myBoard.isOccupied(eachNewPos)):

        # move the piece and flip self.__turns
        self.__clickedPiece.movePiece(eachNewPos)
        if GUIClass.myBoard.isCheck(self.__turn):
          self.__isInCheck = True
          self.__clickedPiece.undoMove()
        else:
          self.__isInCheck = False
          self.__turn = not(self.__clickedPiece.getColor())
        
        pygame.display.update()
        self.__lock = False
        pygame.time.delay(1000)

            
GUIClass()
