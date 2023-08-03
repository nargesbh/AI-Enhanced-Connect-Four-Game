import numpy as np
import tensorflow as tf

# Define the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(42,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Define the game board
board = np.zeros((6,7))

# Define a function to convert the board to a 1-dimensional array
def flatten_board(board):
    return np.reshape(board, 42)

# Define a function to display the board in the terminal
def display_board(board):
    for row in board:
        print(" ".join(["." if x == 0 else "O" if x == 1 else "X" for x in row]))

# Define a function to play a move
def play_move(board, column, player):
    for row in range(6):
        if board[5-row][column] == 0:
            board[5-row][column] = player
            break
    return board


# Define a function to check if the game is over
def is_game_over(board):
    for row in range(6):
        for col in range(7):
            if board[row][col] == 0:
                continue
            if col <= 3 and np.all(board[row][col:col+4] == board[row][col]):
                return True
            if row <= 2 and np.all(board[row:row+4,col] == board[row][col]):
                return True
            if col <= 3 and row <= 2 and np.all(np.diag(board[row:row+4,col:col+4]) == board[row][col]):
                return True
            if col >= 3 and row <= 2 and np.all(np.diag(np.fliplr(board)[row:row+4,col-3:col+1]) == board[row][col]):
                return True
    if np.count_nonzero(board) == 42:
        return True
    return False


# Define a function to play the game
def play_game():
    board = np.zeros((6,7))
    player = 1
    while not is_game_over(board):
        display_board(board)
        if player == 1:
            column = int(input("Player 1's turn (column 0-6): "))
        else:
            inputs = np.expand_dims(flatten_board(board), axis=0)
            prediction = model.predict(inputs)[0][0]
            column = int(round(prediction * 6))
        if board[0][column] != 0:
            print("Column is full, choose another column.")
            continue
        play_move(board, column, player)
        player = 2 if player == 1 else 1
    display_board(board)
    print("Game over!")

# Start the game
play_game()