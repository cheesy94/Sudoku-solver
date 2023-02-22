import numpy as np


## Get small grid to which number i,j belongs
def get_subgrid_matrix(matrix,i,j):
    subgrid_size = int(np.sqrt(np.sqrt(matrix.size)))
    
    subgrid_i = int(i/subgrid_size)*subgrid_size
    subgrid_j = int(j/subgrid_size)*subgrid_size
    
    return matrix[subgrid_i:subgrid_i+subgrid_size,subgrid_j:subgrid_j+subgrid_size]


## Get possible numbers for every cell
def get_possible_numbers(matrix):
    rowcol_size = int(np.sqrt(matrix.size))
    
    possible = np.empty(matrix.size, dtype=object)
    possible[...] = [[] for _ in range(matrix.size)]
    possible = possible.reshape(rowcol_size,rowcol_size)
    
    for n in range(1,rowcol_size+1):
            for j in range(rowcol_size):
                # Check column
                if n in matrix[:,j]:
                    continue
                
                for i in range(rowcol_size):
                    # Check row
                    if n in matrix[i,:]:
                        continue
                    
                    # Already solved
                    if matrix[i,j] != 0:
                        continue
                    
                    # Check subgrid
                    if n in get_subgrid_matrix(matrix,i,j):
                        continue
                    
                    possible[i,j].append(n)
    
    return possible


## Solver
def solve(initial):
    
    rowcol_size = int(np.sqrt(initial.size))

    current = initial.copy()
    previous = np.zeros_like(current)
    loops = 0 
    
    
    while (current == 0).any():
        # Check forever loop
        if (previous == current).all():
            print("Exiting infinite loop")
            # DO SMTH
            break
        previous = current.copy()
        
        # Count loops
        loops+=1
        
        # Get possible numbers for every cell
        possible = get_possible_numbers(current)
        
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
                        
    return current,loops,possible