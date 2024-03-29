# Sudoku solver

A Sudoku is a popular logic-based number puzzle consisting of a squared grid divided into square regions. The grid is filled with numbers ensuring each row, column and region contains all possible numbers without repetition. The grid typically is 9x9, divided into 3x3 regions and filled with digits from 1-9, but other sizes and variations exist as well.

A partially filled Sudoku puzzle is provided as the initial setup, and the goal is to completely fill the remaining empty cells using deduction and logical reasoning according to the rules.

<img src="/initial.png" width="300" height="300" /> <img src="/solution.png" width="300" height="300" /> 

This project implements a simple algorithm to solve Sudoku puzzles of many sizes and difficulties.

## Requirements
- Python 3.x
- Numpy
- Tkinter (GUI)
- Functools (GUI)

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/cheesy94/Sudoku-solver
   ```

2. Navigate to the project directory:
   ```
   cd Sudoku-solver
   ```

3. Edit the main file to choose an input option
   ```
   nano main.py
   ```

4. Run the main file
   ```
   python main.py
   ```

5. The algorithm will display the solution and the number of loops it took.

## Roadmap

- [x] Read from text file
- [ ] Read from image (openCV lib)
    - [ ] Pool of images to test
    - [ ] Detect Sudoku bounds
    - [ ] Detect Sudoku grid
    - [ ] Number recognition
- [x] GUI
    - [x] Draw Sudoku
    - [x] Change numbers clicking
    - [x] Config solve button
    - [x] Show solution

