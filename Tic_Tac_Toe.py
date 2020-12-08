# 1.Importing the required libraries and setting up the required global variables.
import pygame as pg
import time
import sys
from pygame.locals import *

# Declaring the Global Variables
XO = 'x'  # this variable is for storing the value of 'x' and 'o' (we set it as x)
winner = None  # this variable for storing the winner
draw = False  # to check if the game is a draw
# To set the width and height of the display window
width = 400
height = 400
# To set the background color of the game window
game_window_bg_color = (255, 255, 255)  # as RGB or #FFFFFF (white)
# The color of the line that seperates the board
line_color = (128, 0, 0)  # as RGB or #000000 (black)
# Board that is 3 * 3
board = [[None] * 3, [None] * 3, [None] * 3]
# ------------------------------------------------------------

# 2.Designing the game display function, that will set a platform
pg.init()  # Initialize the game window
fps = 30  # Set the FPS
clock = pg.time.Clock()  # To track the time while game is displayed
# pg.display.set_mode is used to build the game screen
game_screen = pg.display.set_mode((width, height + 100), 0, 32)
# It takes the width, height , depth , then the fps

# Set the game tag (or title)
pg.display.set_caption(" X-O Game ")
# Load the images of X , O as objects in python
initial_window = pg.image.load("modified_cover.png")  # load needs the name of img and its extension
x_img = pg.image.load("X_Img.png")
o_img = pg.image.load("O_Img.png")
# But we need to optimize the display size of the images (image.load loads the image in its native size)
# so we use transform.scale >> which needs the img and the width , height u need
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
initial_window = pg.transform.scale(initial_window, (width, height + 100))


def game_initial_window():
    # To Display the Game window over the Screen
    # blit>> used to enable displaying something over another
    # (we need to display the initial window over the screen of the game)
    game_screen.blit(initial_window, (0, 0))
    # Update the Display window ( To update the display of window when called)
    pg.display.update()
    time.sleep(3)
    game_screen.fill(game_window_bg_color)

    # To Draw the Vertical Lines (Display,color,start_point,end_point,width)
    pg.draw.line(game_screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(game_screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    # To Draw the Horizontal Lines
    pg.draw.line(game_screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(game_screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()  # To update the status of the screen on each click of the user


def draw_status():
    # the variable draw (global)
    global draw
    if winner is None:  # If winner is None (which means that no one wins players continue to play)
        message = XO.upper() + "'s Turn"
    else:  # This means that there is a winner
        message = winner.upper() + " won !"
    if draw:  # This means the Game is a draw
        message = "Game Draw !!!"
    # Set a font object
    font = pg.font.Font(None, 30)
    # Set the Font Properties ( such as message ,       color and width)
    text = font.render(message, 1, game_window_bg_color)
    # Copy the message onto the board
    # To create a small part at the bottom of window
    game_screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    game_screen.blit(text, text_rect)
    pg.display.update()


# ------------------------------------------------------------------

# 3.win and draw
def check_win():
    # global variables board,winner,draw
    global board, winner, draw
    # Check for winning conditions ( row, column,diagonal)
    for row in range(0, 3):  # Start from 0 to 2
        # Rows
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            # Draw line on the matched row
            pg.draw.line(game_screen, (128, 70, 70),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6), 4)
            break
    for col in range(0, 3):
        # Columns
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            # Draw line on the matched col
            pg.draw.line(game_screen, (128, 70, 70),
                         ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break
    # Diagonal (Left to Right)
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # Diagonal from Left to Right
        winner = board[0][0]
        # Draw Line throught the Diagonal
        pg.draw.line(game_screen, (128, 70, 70), (50, 50), (350, 350), 4)
    # Diagonal (Right to Left)
    if (board[0][2] == board[1][1] == board[2][1]) and (board[0][2] is not None):
        # Diagonal from Left to Right
        winner = board[0][2]
        # Draw Line throught the Diagonal
        pg.draw.line(game_screen, (128, 70, 70), (350, 50), (50, 350), 4)
    # To check Draw condition
    if (all([all(row) for row in board]) and winner is None):
        draw = True
    draw_status()


# ------------------------------------------------------------------

# 4.Getting the user input and displaying the “X” or “O” at the proper position
# where the user has clicked his mouse.
def draw_XO(row, col):  # Row ,col represent the position
    global board, XO

    # Rows
    # The first Row the img should be pasted at x coordinate (of 30 from the left margin)
    if row == 1:
        positiony = 30
    # The Second Row the img should be pasted at x coordinate (of 30 from the first horizontal game line)
    if row == 2:
        # margin or width/3+ 30 from the left margin of window
        positiony = width / 3 + 30
    # The Third Row the img should be pasted at x coordinate (of 30 from the second horizontal game line)
    if row == 3:
        positiony = width / 3 * 2 + 30

    # Columns
    # The first Row the img should be pasted at y coordinate (of 30 from the left margin)
    if col == 1:
        positionx = 30
    # The Second Column the img should be pasted at y coordinate (of 30 from the first Vertical game line)
    if col == 2:
        # margin or height/3 + 30 from the left margin of window
        positionx = height / 3 + 30
    # The Third Row the img should be pasted at y coordinate (of 30 from the second Vertical game line)
    if col == 3:
        positionx = height / 3 * 2 + 30

    # Setting up the board
    board[row - 1][col - 1] = XO
    if (XO == 'x'):  # x Turn
        # past the x_img over the screen at the position (positionx,positiony)
        game_screen.blit(x_img, (positionx, positiony))
        # Set the XO to the new player turn
        XO = 'o'
    else:  # This means O Turn
        game_screen.blit(o_img, (positionx, positiony))
        XO = 'x'  # Set the XO to the new Player Turn
    pg.display.update()

    # User Click Function


def userClick():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    if (x < width / 3):  # Get column of mouse click (1-3)
        col = 1  # This means that mouse is on the first cell/ square of the column
    elif (x < width / 3 * 2):
        col = 2  # This means that mouse is on the middle of the column
    elif (x < width):
        col = 3  # This means that mouse is on the bottom cell/square of the column
    else:
        col = None
    if (y < height / 3):
        row = 1  # This means that mouse is on the first cell/square of the row
    elif (y < height / 3 * 2):
        row = 2  # This means that mouse is on the middle of the row
    elif (y < height):
        row = 3  # This means that mouse is on the Right square of the row
    else:
        row = None
    # Draw Imgaes at the desired positions
    if (row and col and board[row - 1][col - 1] is None):
        global XO
        draw_XO(row, col)
        check_win()


# ------------------------------------------------------------------

# 5.Running an infinite loop, and including the defined methods in it.
# reset_game() function used to reset the game in order to play another game after game is finished
def reset_game():
    global board, XO, winner, draw
    # Reset all the global Variables to their initial value
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initial_window()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


game_initial_window()
while (True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            userClick()
            if (winner or draw):
                reset_game()
    pg.display.update()
    clock.tick(fps)
# ------------------------------------------------------------
