"""
Board info, calculate valid moves at each state, move log.
"""


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "--"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "--"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves,
                               'N': self.get_knight_moves, 'B': self.get_bishop_moves,
                               'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.knight_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
        self.king_moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.bishop_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.white_turn = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn

    '''
    Undo the last move made
    '''
    def undo_move(self):
        if len(self.move_log) == 0:
            return
        last_move = self.move_log.pop()
        self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
        self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
        self.white_turn = not self.white_turn

    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    '''
    All moves not considering checks
    '''
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                label = self.board[row][col]
                turn = label[0]
                if (turn == 'w' and self.white_turn) or (turn == 'b' and not self.white_turn):
                    piece = label[1]
                    self.move_functions[piece](row, col, moves)
        return moves


    def verify_move_bounds(self, row, col):
        if row > 7 or row < 0 or col > 7 or col < 0:
            return False
        return True

    def get_pawn_moves(self, row, col, moves):
        if self.white_turn:
            if self.board[row-1][col] == "--": #advance pawn 1 square
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--": #advance 2 squares
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1 >= 0: #left capture
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7: #right capture
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else:
            if self.board[row+1][col] == "--":
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col - 1 >= 0: #left capture
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col + 1 <= 7: #right capture
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))


    def get_rook_moves(self, row, col, moves):
        enemy = "b" if self.white_turn else "w"
        for row_increment in range(1, 8-row):
            new_row = row + row_increment
            next_square = self.board[new_row][col]
            if next_square == "--":
                moves.append(Move((row, col), (new_row, col), self.board))
            elif next_square[0] == enemy:
                moves.append(Move((row, col), (new_row, col), self.board))
                break
            else:
                break

        for row_increment in range(1, row+1):
            new_row = row - row_increment
            next_square = self.board[new_row][col]
            if next_square == "--":
                moves.append(Move((row, col), (new_row, col), self.board))
            elif next_square[0] == enemy:
                moves.append(Move((row, col), (new_row, col), self.board))
                break
            else:
                break

        for col_increment in range(1, 8-col):
            new_col = col + col_increment
            next_square = self.board[row][new_col]
            if next_square == "--":
                moves.append(Move((row, col), (row, new_col), self.board))
            elif next_square[0] == enemy:
                moves.append(Move((row, col), (row, new_col), self.board))
                break
            else:
                break

        for col_increment in range(1, col+1):
            new_col = col - col_increment
            next_square = self.board[row][new_col]
            if next_square == "--":
                moves.append(Move((row, col), (row, new_col), self.board))
            elif next_square[0] == enemy:
                moves.append(Move((row, col), (row, new_col), self.board))
                break
            else:
                break



    def get_knight_moves(self, row, col, moves):
        enemy = "b" if self.white_turn else "w"
        for element in self.knight_moves:
            new_square = (row + element[0], col + element[1])
            if not self.verify_move_bounds(new_square[0], new_square[1]):
                continue
            new_square_piece = self.board[new_square[0]][new_square[1]]
            if new_square_piece == "--" or new_square_piece[0] == enemy:
                moves.append(Move((row, col), new_square, self.board))

    def get_bishop_moves(self, row, col, moves):
        enemy = "b" if self.white_turn else "w"
        for element in self.bishop_moves:
            new_square = (row+element[0], col+element[1])
            keep_going = True
            while self.verify_move_bounds(new_square[0], new_square[1]) and keep_going:
                piece = self.board[new_square[0]][new_square[1]]
                if piece == "--":
                    moves.append(Move((row, col), new_square, self.board))
                elif piece[0] == enemy:
                    moves.append(Move((row, col), new_square, self.board))
                    keep_going = False
                else:
                    keep_going = False
                new_square = (new_square[0] + element[0], new_square[1] + element[1])


    def get_king_moves(self, row, col, moves):
        enemy = "b" if self.white_turn else "w"
        for element in self.king_moves:
            new_square = (row + element[0], col + element[1])
            if not self.verify_move_bounds(new_square[0], new_square[1]):
                continue
            new_square_piece = self.board[new_square[0]][new_square[1]]
            if new_square_piece == "--" or new_square_piece[0] == enemy:
                moves.append(Move((row, col), new_square, self.board))

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)




# takes a move as a param and executes - does not work for castling/en passant/promotions
class Move():
    # dicts to map rows/cols to ranks/files for printing
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        #move id to be used in equals method, like a hash
        self.id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    Override equals for equivalent objects
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.id == other.id
        return False

    def get_chess_notation(self):
        rank_file = self.get_rank_file(self.start_row, self.start_col)
        move = rank_file + self.get_rank_file(self.end_row, self.end_col)
        return move

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
