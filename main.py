from reader import read_db
from solver import solve


## Option 1
# Introduce Sudoku manually (0 in empty cells)

initial = [[6,0,0,0,0,4,0,0,0],
           [0,0,0,0,8,0,1,0,0],
           [0,3,7,0,0,6,0,9,4],
           [0,0,9,0,0,0,4,1,2],
           [0,1,3,0,0,9,0,0,5],
           [5,0,6,1,0,0,7,0,9],
           [0,0,2,3,9,0,0,0,0],
           [0,0,4,0,7,5,0,2,0],
           [3,0,8,4,0,0,9,0,0]]


## Option 2
# Read Sudoku from text file

#file = 'db.txt'
#number = 4

#initial,solution = read_db(file,number)


## Option 3
# Introduce Sudoku manually GUI

from GUI import draw

size = 9
draw(size)

# initial = ...


## Option 4
# Read Sudoku from image

# initial = ...


## Solve sudoku
final,loops,possible = solve(initial)

# Print result
print("Result in",loops,"loops:")
print(final)

#if (final == solution).all():
#    print("\nSolved!")
