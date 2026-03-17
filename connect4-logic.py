# the 6X7 board can be looked at as a matrix 

import numpy as np

# creating the board for the game 
def create_board():
  board = np.zeros((6,7))
  return board

board = create_board()
# the game will begin with the game_over being false 
game_over = False

#to diferentiate whose turn it is
turn = 1

# dynamics of the game 
while not game_over:
  # ask for player 1 input
  if turn == 1:
    selected_column = int(input("Player 1, choose a column (0-6): ")) - 1 # takes in the answer from the player and converts it to a number 
   
    for row in range(board.shape[0] - 1, -1, -1):   # go through each row
      if board[row][selected_column] == 0:     # check if the value is 0
          board[row][selected_column] = 1      # replace it with 1
          break                        # stop after replacing the first 0

    for row in board:
        print(row)
    
    turn = 2

    for row in range(board.shape[0]):          # go through each row
      for col in range(board.shape[1] - 3):  # check groups of 4
        if (board[row][col] == 1 and
            board[row][col+1] == 1 and
            board[row][col+2] == 1 and
            board[row][col+3] == 1):
              game_over = True


    for col in range(board.shape[1]):          # go through each column
      for row in range(board.shape[0] - 3):  # check groups of 4 vertically
        if (board[row][col] == 1 and
            board[row+1][col] == 1 and
            board[row+2][col] == 1 and
            board[row+3][col] == 1):
              game_over = True


  # Only check top-left 3 rows and first 4 columns
    for row in range(3):           # 0, 1, 2 → top 3 rows
      for col in range(4):       # 0, 1, 2, 3 → first 4 columns
        # Check diagonal down-right (↘)
        if (row + 3 < board.shape[0] and col + 3 < board.shape[1]):
          if (board[row][col] == 1 and
              board[row+1][col+1] == 1 and
              board[row+2][col+2] == 1 and
              board[row+3][col+3] == 1):
                game_over = True

        # Check diagonal down-left (↙)
        if (row + 3 < board.shape[0] and col - 3 >= 0):
          if (board[row][col] == 1 and
              board[row+1][col-1] == 1 and
              board[row+2][col-2] == 1 and
              board[row+3][col-3] == 1):
                game_over = True
    
    # make the turn 2
    
# ask for player 2 input 
  if turn == 2:
    selected_column = int(input("Player 2, choose a column (0-6): ")) - 1
    for row in range(board.shape[0] - 1, -1, -1):   # go through each row
      if board[row][selected_column] == 0:     # check if the value is 0
          board[row][selected_column] = 2      # replace it with 1
          break                        # stop after replacing the first 0


    for row in board:
        print(row)

    turn = 1
    
    for row in range(board.shape[0]):          # go through each row
      for col in range(board.shape[1] - 3):  # check groups of 4
        if (board[row][col] == 2 and
            board[row][col+1] == 2 and
            board[row][col+2] == 2 and
            board[row][col+3] == 2):
              game_over = True


    for col in range(board.shape[1]):          # go through each column
      for row in range(board.shape[0] - 3):  # check groups of 4 vertically
        if (board[row][col] == 2 and
            board[row+1][col] == 2 and
            board[row+2][col] == 2 and
            board[row+3][col] == 2):
              game_over = True


  # Only check top-left 3 rows and first 4 columns
    for row in range(3):           # 0, 1, 2 → top 3 rows
      for col in range(4):       # 0, 1, 2, 3 → first 4 columns
        # Check diagonal down-right (↘)
        if (row + 3 < board.shape[0] and col + 3 < board.shape[1]):
          if (board[row][col] == 2 and
              board[row+1][col+1] == 2 and
              board[row+2][col+2] == 2 and
              board[row+3][col+3] == 2):
                game_over = True

        # Check diagonal down-left (↙)
        if (row + 3 < board.shape[0] and col - 3 >= 0):
          if (board[row][col] == 2 and
              board[row+1][col-1] == 2 and
              board[row+2][col-2] == 2 and
              board[row+3][col-3] == 2):
                game_over = True
  
 
