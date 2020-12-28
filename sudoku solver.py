import numpy as np
s = np.array([[5, 3, '.', '.', 7, '.', '.', '.', '.'],
                [6, '.', '.', 1, 9, 5, '.', '.', '.'],
                ['.', 9, 8, '.', '.', '.', '.', 6, '.'],
                [8, '.', '.', '.', 6, '.', '.', '.', 3],
                [4, '.', '.', 8, '.', 3, '.', '.', 1],
                [7, '.', '.', '.', 2, '.', '.', '.', 6],
                ['.', 6, '.', '.', '.', '.', 2, 8, '.'],
                ['.', '.', '.', 4, 1, 9, '.', '.', 5],
                ['.', '.', '.', '.', 8, '.', '.', 7, 9]])

def condition_checking(row,col,key,mat):
    for i in range(0,9):
        if(mat[row][i]==str(key)):
            return False
    for i in range(0,9):
        if(mat[i][col]==str(key)):
            return False
    box_row=(row//3)*3
    box_col=(col//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if(mat[box_row+i][box_col+j]==str(key)):
                return False
    return True
def check_empty(s):
    for i in range(9):
        for j in range(9):
            if(s[i][j]=='.'):
                l=[i,j]
                return l
    l=[-1,-1]
    return l
def solve_sudoku(s):
    l=check_empty(s)
    if(l[0]=-1):
        return True
            
    row=l[0]
    col=l[1]
    for key in range(1,10):
        if(condition_checking(row,col,key,s)):
                s[row][col]=str(key)
                if(solve_sudoku(s)):
                        return True
                s[row][col]='.'
    return False

def print_sudoku(s):
    for i in range(9):
        for j in range(9):
            print(s[i][j], end='')
            if (j + 1) % 3 == 0 and j != 8:
                print('|', end='')
        print()
        if (i + 1) % 3 == 0 and i != 8:
            print('-' * 11)
if(solve_sudoku(s)):
    print_sudoku(s)
            