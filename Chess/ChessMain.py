"""
Handle user input, display game state.
"""

import pygame as p
from Chess import ChessEngine

p.init()

WIDTH = HEIGHT = 512
DIMENSIONS = 8  #8x8 board
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15   #for move animations
IMAGES = {} #dict of pieces/images for display

"""
Initialize global dict of images. Call only once for efficiency
"""
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bN', 'bR', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
Main driver, input and graphics
'''

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    running = True
    selected_square = () #keep track of last click (row, col)
    clicked_squares = [] #two tuples, keep track of clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #mouse location
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    clicked_squares = []
                else:
                    selected_square = (row, col)
                    clicked_squares.append(selected_square)
                if len(clicked_squares) == 2:
                    move = ChessEngine.Move(clicked_squares[0], clicked_squares[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    selected_square = ()
                    clicked_squares = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #call undo if z is pressed
                    gs.undo_move()
                    selected_square = ()
                    clicked_squares = []
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_board(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Draw the squares on the board
'''
def draw_board(screen, gs):
    board = gs.board
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(0, DIMENSIONS):
        for col in range(0, DIMENSIONS):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()