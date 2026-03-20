
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

def is_valid(column):
   if column <= 7 :
      return True
   else:
      return False

def moving_pieces(colums, player) :
   for row in range(board.shape[0] - 1, -1, -1):   # go through each row
      if board[row][colums] == 0:     # check if the value is 0
          board[row][colums] = player      # replace it with 1
          break 
      

def check_win(player):
   game_over = False
   for row in range(board.shape[0]):          # go through each row
      for col in range(board.shape[1] - 3):  # check groups of 4
        if (board[row][col] == player and
            board[row][col+1] == player and
            board[row][col+2] == player and
            board[row][col+3] == player):
              game_over = True


   for col in range(board.shape[1]):          # go through each column
      for row in range(board.shape[0] - 3):  # check groups of 4 vertically
        if (board[row][col] == player and
            board[row+1][col] == player and
            board[row+2][col] == player and
            board[row+3][col] == player):
              game_over = True

  
  # Only check top-left 3 rows and first 4 columns
   for row in range(3):           # 0, 1, 2 → top 3 rows
      for col in range(4):       # 0, 1, 2, 3 → first 4 columns
        # Check diagonal down-right (↘)
        if (row + 3 < board.shape[0] and col + 3 < board.shape[1]):
          if (board[row][col] == player and
              board[row+1][col+1] == player and
              board[row+2][col+2] == player and
              board[row+3][col+3] == player):
                game_over = True

        # Check diagonal down-left (↙)
        if (row + 3 < board.shape[0] and col - 3 >= 0):
          if (board[row][col] == player and
              board[row+1][col-1] == player and
              board[row+2][col-2] == player and
              board[row+3][col-3] == player):
                game_over = True
   
   if game_over:
      return True
   else:
      return False





# dynamics of the game 
while game_over == False:
  # ask for player 1 input
  if turn == 1:
    selected_column = int(input("Player 1, choose a column (0-6): ")) - 1 # takes in the answer from the player and converts it to a number

    is_valid(selected_column)
   
    moving_pieces(selected_column, 1)

    for row in board:
        print(row)
    
    turn = 2

    
    game_over = check_win(1) 
    
    if game_over:
        print("Player 1 wins!")
        break
    
# ask for player 2 input 
  if turn == 2:
    selected_column_second = int(input("Player 2, choose a column (0-6): ")) - 1

   # is it valid
    is_valid(selected_column_second)
    
    # move the piece 
    moving_pieces(selected_column_second, 2)

    for row in board:
        print(row)

    turn = 1
    
    game_over = check_win(2) 
    
    if game_over:
        print("Player 2 wins!")
        break
   
  

 
