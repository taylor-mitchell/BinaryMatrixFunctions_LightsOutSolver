import numpy as np
import random as rand

#makes a random lights out board
def random_board(width, height):
    to_return = []
    for i in range(0, width):
        row = []
        for j in range(0, height):
            row.append(rand.randint(0, 1))
        to_return.append(row)
    return to_return

#adds two rows together
def add_row(row1, row2):
    to_return = []
    for i in range(0, len(row1)):
        if row1[i] == 1 and row2[i] == 1:
            to_return.append(0)
        else:
            to_return.append(row1[i] + row2[i])

#switches two rows
def switch_rows(board, row1_num, row2_num):
    row1 = board[row1_num]
    row2 = board[row2_num]
    board.insert(row1_num, row2)
    board.pop(row1_num + 1)
    board.insert(row2_num, row1)
    board.pop(row2_num + 1)

#subtracts two rows
def subtract_row(row1, row2):
    to_return = []
    for i in range(0, len(row1)):
        if row1[i] == 0 and row2[i] == 1:
            to_return.append(1)
        else:
            to_return.append(row1[i] - row2[i])
    return to_return

#peforms gaussian elimination on matrix
def rref(board):
    for j in range(0, len(board)):
        leading_row = j
        for i in range(j, len(board)):
            if board[i][j] != 0:
                leading_row = i
                break
        switch_rows(board, leading_row, j)
        for i in range(0, len(board)):
            if board[i][j] == 1 and i != j:
                board[i] = subtract_row(board[i], board[j])
    return board

#combines a column and a matrix
def augment_column(board, column):
    for j in range(0, len(board)):
           board[j].append(column[j])

#combines two boards
def augment_board(board1, board2):
    for j in range(0, len(board1)):
        for i in range(0, len(board2[j])):
            board1[j].append(board2[j][i])

#makes an identity matrix of given size
def make_identity(width, height):
    to_return = []
    for i in range(0, width):
        row = []
        for j in range(0, height):
            if j == i:
                row.append(1)
            else:
                row.append(0)
        to_return.append(row)
    return to_return

#prints out the matrix
def print_board(board):
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 1:
                ch = '*'
            else:
                ch = ' '
            print("|" + ch, end = "")
        print('|')
        for j in range(0, len(board[i])):
            print("--", end = "")
        print('-')

#perform a toggle of a value at the given location on the given matrix
def press_light(board, x, y):
    for i in range(-1, 2):
        if y + i >= 0 and y + i < len(board):
                if board[y + i][x] == 1:
                    board[y + i][x] = 0
                else:
                    board[y + i][x] = 1        
    for j in range(-1, 2):
         if x + j >= 0 and x + j < len(board) and j != 0:
                if board[y][x + j] == 1:
                    board[y][x + j] = 0
                else:
                    board[y][x + j] = 1
    print_board(board)

#turn the matrix into a 1d vector
def flatten_board(board):
    to_return = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            to_return.append(board[i][j])
    return to_return

#turn a 1d vector into a matrix
def unflatten_board(flat_board):
    return_board = []
    width = int(len(flat_board) ** (1/2))
    for i in range(0, width):
        row = []
        for j in range(0, width):
            row.append(flat_board[i * width + j])
        return_board.append(row)
    return return_board

#makes a list of all possible board states
def make_all_possible_board(width, height):
    to_return = []
    for i in range(0, width):
        for j in range(0, height):
            to_return.append(flatten_board(make_possible_board(i, j, width, height)))
    return to_return

	
def make_possible_board(x, y, width, height):
    to_return = []
    for i in range(0, width):
        row = []
        for j in range(0, height):
            if i == x and j == y or i + 1 == x and j == y or i - 1 == x and j == y or i == x and j + 1 == y or i == x and j - 1 == y:
                row.append(1)
            else:
                row.append(0)            
        to_return.append(row)
    return to_return

#returns the sequence of moves in the game lights out that dont change the board
def get_quiet_patterns(width, height):
    to_return = []
    p_board = make_all_possible_board(width, height)
    i_board = make_identity(width ** 2, height ** 2)
    augment_board(p_board, i_board)
    r_board = rref(p_board)
    for i in range(len(r_board) - 1, 0, -1):
        is_quiet = True
        for j in range(0, width ** 2):
            if r_board[i][j] != 0:
                is_quiet = False
                break
        if is_quiet:
            row = []
            for j in range(width**2, width ** 2 * 2):
                row.append(r_board[i][j])
            to_return.append(row)
    return to_return

#determines if a game of lights out is solvable
def is_solvable(board):
    width = len(board)
    height = width
    q_patterns = get_quiet_patterns(width, height)
    f_board = flatten_board(board)
    solvable = True
    for i in range(0, len(q_patterns)):
        common_number = 0
        for j in range(0, len(q_patterns[i])):
            if f_board[j] == 1 and q_patterns[i][j] == 1:
                common_number += 1
        if common_number % 2 == 1:
            solvable = False
            break
    return solvable

#returns a solution to a game of lights out
def solve(board):
    width = len(board)
    f_board = flatten_board(board)
    quiet_patterns = get_quiet_patterns(width, width)

    if not is_solvable(board):
        print("not solvable")
        return
    
    p_board = make_all_possible_board(width, width)
    augment_column(p_board, f_board)
    r_board = rref(p_board)

    solution_list = []
    for i in range(0, width ** 2):
        solution_list.append(0)
         
    for i in range(len(p_board) - 1, -1, -1):
        x_positions = []
        right_side = p_board[i][width**2]
        for j in range(width ** 2 - 1, -1, -1):
            if p_board[i][j] == 1:
                x_positions.append(j)
        if len(x_positions) != 0:
            for i in range(0, len(x_positions) - 1):
                if solution_list[x_positions[i]] == 1:
                    if right_side == 1:
                        right_side == 0
                    else:
                        right_side == 1 
            solution_list[x_positions[len(x_positions) - 1]] = right_side

    return unflatten_board(solution_list)

def main(width = 3):
    board = random_board(width, width)
    while is_solvable(board) == False:
        board = random_board(width, width)
    print("Starting board...")
    print_board(board)
    
    f_board = flatten_board(board)
    print("Flattened:")
    print(f_board)
    
    p_board = make_all_possible_board(width, width)
    print("Matrix of all possible moves:")
    print_board(p_board)

    print("Augmented matrix:")
    augment_column(p_board, f_board)
    print_board(p_board)
        
    s_board = rref(p_board)    
    print("Augmented and reduced:")
    print_board(s_board)

    solution = solve(board)
    print("Solution")
    print_board(solution)

    
def main2(width = 3):
    board = random_board(width, width)
    while is_solvable(board) == False:
        board = random_board(width, width)
    print("Starting board...")
    print_board(board)
    
    f_board = flatten_board(board)

    p_board = make_all_possible_board(width, width)
      
    s_board = rref(p_board)    

    solution = solve(board)
    print("Solution")
    print_board(solution)

        


    
    
