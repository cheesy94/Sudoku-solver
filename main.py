import numpy as np
from solver import solve

# Read sudoku
solution = np.array([[7,3,4,6,8,9,5,2,1],
                     [6,8,5,1,2,7,3,4,9],
                     [1,9,2,3,4,5,6,7,8],
                     [9,5,1,4,3,6,7,8,2],
                     [4,6,7,8,9,2,1,5,3],
                     [8,2,3,5,7,1,4,9,6],
                     [3,7,8,9,1,4,2,6,5],
                     [2,1,6,7,5,8,9,3,4],
                     [5,4,9,2,6,3,8,1,7]])

initial = np.array([[7,0,0,0,8,0,0,2,0],
                    [0,0,0,1,0,0,3,4,0],
                    [0,9,2,3,0,0,6,0,0],
                    [0,5,1,0,0,6,0,0,0],
                    [0,0,0,8,0,2,0,5,3],
                    [0,2,3,0,0,0,0,9,0],
                    [3,0,0,9,1,0,0,0,0],
                    [0,0,6,7,0,0,0,0,4],
                    [5,4,0,0,0,0,8,0,7]])

# initial = np.array([[7,2,0,0,4,9,0,0,3],
#                     [0,0,0,0,0,0,2,0,0],
#                     [0,0,0,7,6,2,0,0,5],
#                     [9,0,1,3,0,0,0,7,0],
#                     [2,0,6,0,0,0,3,0,1],
#                     [0,3,0,0,0,7,5,0,9],
#                     [8,0,0,1,7,5,0,0,0],
#                     [0,0,3,0,0,0,0,0,0],
#                     [5,0,0,2,9,0,0,1,4]])

# initial = np.array([[6,0,0,0,0,4,0,0,0],
#                     [0,0,0,0,8,0,1,0,0],
#                     [0,3,7,0,0,6,0,9,4],
#                     [0,0,9,0,0,0,4,1,2],
#                     [0,1,3,0,0,9,0,0,5],
#                     [5,0,6,1,0,0,7,0,9],
#                     [0,0,2,3,9,0,0,0,0],
#                     [0,0,4,0,7,5,0,2,0],
#                     [3,0,8,4,0,0,9,0,0]])

# Solve sudoku
final,loops,possible = solve(initial)

# Print result
print("Result in",loops,"loops:")
print(final)

if (final == solution).all():
    print("\nSolved!")
