import numpy as np

def get_subgrid_matrix(matrix,i,j):
    subgrid_size = int(np.sqrt(np.sqrt(matrix.size)))
    
    subgrid_i = int(i/subgrid_size)*subgrid_size
    subgrid_j = int(j/subgrid_size)*subgrid_size
    
    return matrix[subgrid_i:subgrid_i+subgrid_size,subgrid_j:subgrid_j+subgrid_size]
    
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

rowcol_size = int(np.sqrt(solution.size))
subgrid_size = int(np.sqrt(rowcol_size))

current = initial.copy()
previous = np.zeros_like(current)
loops = 0

while not (current == solution).all():
    # Check forever loop
    if (previous == current).all():
        print("Exiting infinite loop")
        break
    previous = current.copy()
    
    # Count loops
    loops+=1
    
    # Get possible numbers for every cell
    possible = np.empty(solution.size, dtype=object)
    possible[...] = [[] for _ in range(solution.size)]
    possible = possible.reshape(rowcol_size,rowcol_size)
    
    for n in range(1,rowcol_size+1):
        for j in range(rowcol_size):
            # Check column
            if n in current[:,j]:
                continue
            
            for i in range(rowcol_size):
                # Check row
                if n in current[i,:]:
                    continue
                
                # Already solved
                if current[i,j] != 0:
                    continue
                
                # Check subgrid
                if n in get_subgrid_matrix(current,i,j):
                    continue
                
                possible[i,j].append(n)
    
    # Solve sure numbers
    for j in range(rowcol_size):
        for i in range(rowcol_size):
            p = possible[i,j]
            lenp = len(p)
            
            if lenp==0:
                continue
            
            if lenp==1:
                current[i,j] = p[0]
                #print(i,j,current[i,j])
                continue
            
            possible_neighbours = possible.copy()
            possible_neighbours[i,j] = []
            
            subgrid_possible = get_subgrid_matrix(possible_neighbours,i,j)
            subgrid_possible = np.unique(np.concatenate(subgrid_possible.flatten()))
            #subgrid_possible_numbers,subgrid_possible_counts = np.unique(np.concatenate(subgrid_possible.flatten()),return_counts=True)
            #subgrid_secure_numbers = subgrid_possible_numbers[subgrid_possible_counts==1]
            
            for pn in p:
                if not pn in subgrid_possible:
                    current[i,j] = pn
                    #print(i,j,current[i,j])
 
print("Solved in",loops,"loops!")
print(current)
