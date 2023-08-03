import numpy as np
import random
import pygame
import sys
import math

PLAYER = 0
AI = 1
ROW_NUM = 6
COLUMN_NUM = 7
SIZE_W = 4
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0,0,139)
AZUR = (131,139,139)
BLACK = (0,0,0)
AQUA = (118,238,198)




def Boar_init():
	board = np.zeros((ROW_NUM,COLUMN_NUM))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def check_loc_validity(board, col):
	return board[ROW_NUM-1][col] == 0

def find_empty_r(board, col):
  for r in range(ROW_NUM):
	  if board[r][col] == 0:
		  return r

def print_board(board):
	print(np.flip(board, 0))

def win_pos_finder(board, piece):
    # Check horizontal locations for win
  for row in range(ROW_NUM):
    for col in range(COLUMN_NUM - SIZE_W + 1):
      if (board[row][col] == piece and
          board[row][col + 1] == piece and
          board[row][col + 2] == piece and
          board[row][col + 3] == piece):
          return True

    # Check vertical locations for win
  for col in range(COLUMN_NUM):
    for row in range(ROW_NUM - SIZE_W + 1):
      if (board[row][col] == piece and
          board[row + 1][col] == piece and
          board[row + 2][col] == piece and
          board[row + 3][col] == piece):
          return True

    # Check positively sloped diagonals
  for row in range(ROW_NUM - SIZE_W + 1):
    for col in range(COLUMN_NUM - SIZE_W + 1):
      if (board[row][col] == piece and
          board[row + 1][col + 1] == piece and
          board[row + 2][col + 2] == piece and
          board[row + 3][col + 3] == piece):
          return True

    # Check negatively sloped diagonals
  for row in range(SIZE_W - 1, ROW_NUM):
    for col in range(COLUMN_NUM - SIZE_W + 1):
      if (board[row][col] == piece and
          board[row - 1][col + 1] == piece and
          board[row - 2][col + 2] == piece and
          board[row - 3][col + 3] == piece):
          return True

  return False



# Function that scores a given window based on the number of pieces belonging to the current player and the opponent. 
# The function is used to evaluate the strength of the current player's position on the board.
#
# Args:
#   window: A list of integers representing the pieces in a specific row, column, or diagonal.
#   current_piece: An integer representing the piece of the current player (either PLAYER_PIECE or AI_PIECE).
#
# Returns:
#   score: An integer score for the given window, reflecting the strength of the current player's position.
#
def window_score(window, current_piece):
  # Initialize the score to 0
  score = 0
  # Determine the opponent piece based on the current player's piece
  opponent_piece = PLAYER_PIECE
  if current_piece == PLAYER_PIECE:
    opponent_piece = AI_PIECE

  # Increase the score if there are four of the current player's pieces in the window
  if window.count(current_piece) == 4:
    score += 100
  # Increase the score if there are three of the current player's pieces and one empty space in the window
  elif window.count(current_piece) == 3 and window.count(EMPTY) == 1:
    score += 5
  # Increase the score if there are two of the current player's pieces and two empty spaces in the window
  elif window.count(current_piece) == 2 and window.count(EMPTY) == 2:
    score += 2

  # Decrease the score if there are three of the opponent's pieces and one empty space in the window
  if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
    score -= 4

  # Return the final score
  return score



# find_score function calculates the score of the given game board and current piece.
# This score is used to determine the best move for the current player in the Connect Four game.

# game_board: A 2D numpy array that represents the current state of the game board.
# current_piece: The current piece of the player whose score is being calculated.

# The function starts by scoring the center column of the game board. 
# It counts the number of occurrences of the current piece in the center column and multiplies it by 3. 
# This is because having pieces in the center column is generally more advantageous.

# The function then scores the game board by evaluating all the horizontal, vertical, and diagonal windows of length 4.
# It does this by passing each window to the window_score function, which calculates the score of the window.

# The score is calculated for both positive sloped diagonals, which are diagonals with a positive slope from left to right.

# The function returns the final calculated score, which is used to determine the best move for the current player.
def find_score(game_board, current_piece):
  score = 0
  ## Score center column
  center_column = [int(i) for i in list(game_board[:, COLUMN_NUM//2])]
  center_count = center_column.count(current_piece)
  score += center_count * 3

  ## Score Horizontal
  for row in range(ROW_NUM):
    row_elements = [int(i) for i in list(game_board[row,:])]
    for col in range(COLUMN_NUM-3):
      window = row_elements[col:col+SIZE_W]
      score += window_score(window, current_piece)

  ## Score Vertical
  for col in range(COLUMN_NUM):
    col_elements = [int(i) for i in list(game_board[:,col])]
    for row in range(ROW_NUM-3):
      window = col_elements[row:row+SIZE_W]
      score += window_score(window, current_piece)

  ## Score positive sloped diagonal
  for row in range(ROW_NUM-3):
    for col in range(COLUMN_NUM-3):
      window = [game_board[row+i][col+i] for i in range(SIZE_W)]
      score += window_score(window, current_piece)

  for row in range(ROW_NUM-3):
    for col in range(COLUMN_NUM-3):
      window = [game_board[row+3-i][col+i] for i in range(SIZE_W)]
      score += window_score(window, current_piece)

  return score

def terminal_node(board):
	return win_pos_finder(board, PLAYER_PIECE) or win_pos_finder(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# The function minimax implements the minimax algorithm to determine the best move for the AI player in a Connect 4 game. It takes in the current game board, the current depth in the search tree, the alpha-beta pruning parameters alpha and beta, and a flag to indicate whether the current player is the maximizing player or not.

# The function first gets all the valid locations on the board where a piece can be placed, and checks if the game is already in a terminal state (i.e., either the AI wins, the player wins, or the game is a draw). If the game is in a terminal state or the depth of the search has reached 0, the function returns a score representing the value of the terminal state. If the game is won by the AI, the score is set to a large positive number. If the game is won by the player, the score is set to a large negative number. If the game is a draw, the score is set to 0.

# If the current player is the maximizing player, the function sets the value to negative infinity, selects a random column from the list of valid locations, and then loops through all the valid locations. For each column, it calculates the score for the next state of the game after placing a piece in the column by calling the minimax function recursively with a reduced depth. If the score for the next state is higher than the current value, the function updates the value and the column. The function also updates the alpha parameter to be the maximum of the current value and the alpha parameter. If the alpha parameter is greater than or equal to the beta parameter, the function breaks out of the loop as the current branch of the search tree can be pruned.

# Finally, the function returns the selected column and the calculated value.

# The minimax function implements the classic minimax algorithm with alpha-beta pruning for improved performance. The algorithm calculates the best move for the AI player by searching the game tree and evaluating the terminal states of the game. The use of alpha-beta pruning helps reduce the number of nodes in the search tree and increase the efficiency of the algorithm.

# The function takes in 5 parameters:

# board is the current state of the game board
# depth is the maximum search depth
# alpha and beta are the values used in alpha-beta pruning
# maximizingPlayer is a boolean value that indicates whether it is the AI's turn to make a

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if win_pos_finder(board, AI_PIECE):
				return (None, 100000000000000)
			elif win_pos_finder(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, find_score(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = find_empty_r(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = find_empty_r(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


# This function get_valid_locations takes a game board as an input and returns a list of valid move columns. It does this by checking
#  if the next open row in each column is a valid location using the function check_loc_validity. If the next open row in a column is a 
#  valid location, the column is added to the valid_move_columns list. Finally, the list of valid move columns is returned.
def get_valid_locations(game_board):
	valid_move_columns = []
	for column in range(COLUMN_NUM):
		if check_loc_validity(game_board, column):
			valid_move_columns.append(column)
	return valid_move_columns


# Function to pick the best move for the AI player
def pick_best_move(board, piece):

	# Get the list of valid move locations on the board
	valid_locations = get_valid_locations(board)
 
 # Initialize the best score as a low value and best column as a random valid location
	best_score = -10000
	best_col = random.choice(valid_locations)
 
 # Iterate through each valid location on the board
	for col in valid_locations:

		# Get the next open row in the current column
		row = find_empty_r(board, col)
	
	# Make a copy of the board to make temporary changes
		temp_board = board.copy()
	
	# Place the AI piece on the temporary board
		drop_piece(temp_board, row, col, piece)
	
	# Calculate the score of the position after placing the AI piece
		score = find_score(temp_board, piece)
	
	# If the score is better than the current best score, update the best score and best column
		if score > best_score:
			best_score = score
			best_col = col

	# Return the best column to place the AI piece
	return best_col

 

def draw_board(game_board):
# Loop through each column and row of the board
	for col in range(COLUMN_NUM):
		for row in range(ROW_NUM):
# Draw a blue square at the current row and column
			pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
# Draw a black circle in the center of the square
			pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	# Loop through each column and row of the board again
	for col in range(COLUMN_NUM):
		for row in range(ROW_NUM):		
			# Check if the current space is occupied by the player
			if game_board[row][col] == PLAYER_PIECE:
				# Draw a red circle in the center of the square if the space is occupied by the player
				pygame.draw.circle(screen, AQUA, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			# Check if the current space is occupied by the AI
			elif game_board[row][col] == AI_PIECE: 
				# Draw a AZUR circle in the center of the square if the space is occupied by the AI
				pygame.draw.circle(screen, AZUR, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	# Update the display
	pygame.display.update()







board = Boar_init()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_NUM * SQUARESIZE
height = (ROW_NUM+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, AQUA, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if check_loc_validity(board, col):
					row = find_empty_r(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if win_pos_finder(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, AQUA)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		#col = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if check_loc_validity(board, col):
			#pygame.time.wait(500)
			row = find_empty_r(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if win_pos_finder(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, AZUR)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)