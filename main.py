import numpy as np
from solver import solve
from reader import read_db

number = 0
file = 'db.txt'

# Read sudoku
initial,solution = read_db(file,number)


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
