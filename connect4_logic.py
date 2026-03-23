
# the 6X7 board can be looked at as a matrix 

import numpy as np

#size of the board
column_count = 7
row_count = 6

# creating the board for the game 
def create_board():
  board = np.zeros((row_count,column_count))
  return board

board = create_board()

# The game will begin with the game_over being false 
game_over = False

# Differentiating whose turn it is 
turn = 1

# Function that checks if the move is valid (is there a column to drop it in)
def is_valid_existing_column(column):
   if column <= 7 :
      return True
   else:
      return False
   
def is_valid_filled__column(column):
  for row in board:
      if row[column] == 0:
         return True
   
  return False
   
   
# Function that moves the piece
def moving_pieces(colums, player) :
   for row in range(row_count - 1, -1, -1):   # go through each row
      if board[row][colums] == 0:     # check if the value is 0
          board[row][colums] = player      # replace it with 1
          return True 
   return False  
      
# Fuction that checks if the game has been won
def check_win(player):
   game_over = False
   for row in range(row_count):          # go through each row
      for col in range(column_count - 3):  # check groups of 4
        if (board[row][col] == player and
            board[row][col+1] == player and
            board[row][col+2] == player and
            board[row][col+3] == player):
              game_over = True


   for col in range(column_count):          # go through each column
      for row in range(row_count - 3):  # check groups of 4 vertically
        if (board[row][col] == player and
            board[row+1][col] == player and
            board[row+2][col] == player and
            board[row+3][col] == player):
              game_over = True

  
  # Check the positevely Sloped diagonals 
   for col in range(column_count-3):
      for row in range(row_count-3):
        if( board[row][col]==player and
            board[row+1][col+1]==player and
            board[row+2][col+2]==player and
            board[row+3][col+3]==player ):
              game_over = True

   for col in range(column_count - 3):
        for row in range(3, row_count):
           if( board[row][col]==player and
            board[row-1][col+1]==player and
            board[row-2][col+2]==player and
            board[row-3][col+3]==player ):
              game_over = True
            
   if game_over:
      return True
   else:
      return False

