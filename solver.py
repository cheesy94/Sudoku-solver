import numpy as np


## Get small grid index to which cell i,j belongs
def get_subgrid_index(i,j,size):
    
    subgrid_i = int(i/size)*size
    subgrid_j = int(j/size)*size
    
    return subgrid_i,subgrid_j

## Get indexes of complementary small grids
def get_complementary_subgrid_index(i,j,size):
    
    si,sj = get_subgrid_index(i,j,size)
    
    return [(i*size,j*size) for i in range(size) for j in range(size) if bool(i==si) ^ bool(j==sj)]

## Get small grid i,j
def get_subgrid_matrix(matrix,i,j):
    subgrid_size = int(np.sqrt(np.sqrt(matrix.size)))
    
    si,sj = get_subgrid_index(i,j,subgrid_size)
    
    return matrix[si:si+subgrid_size,sj:sj+subgrid_size]


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
                    # Already solved
                    if matrix[i,j] != 0:
                        continue
                    
                    # Check row
                    if n in matrix[i,:]:
                        continue
                    
                    # Check subgrid
                    if n in get_subgrid_matrix(matrix,i,j):
                        continue
                    
                    possible[i,j].append(n)
    
    return possible


## Check if possible number prevents other subgrid from

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
        
        # Filter possible numbers
        
        # Solve sure numbers
        for j in range(rowcol_size):
            for i in range(rowcol_size):
                p = possible[i,j]
                lenp = len(p)
                
                # Already solved
                if current[i,j] != 0: #lenp==0:
                    continue
                
                # Unique number in cell
                if lenp==1:
                    current[i,j] = p[0]
                    #print(i,j,current[i,j])
                    continue
                
                # Neighbours
                possible_neighbours = possible.copy()
                possible_neighbours[i,j] = []
                
                for ipn,pn in enumerate(p):
                    
                    # Unique position in row, col, subgrid
                    possible_row = np.unique(np.concatenate(possible_neighbours[i,:].flatten()))
                    possible_col = np.unique(np.concatenate(possible_neighbours[:,j].flatten()))
                    possible_subgrid = np.unique(np.concatenate(get_subgrid_matrix(possible_neighbours,i,j).flatten()))
                    if (not pn in possible_row) or (not pn in possible_col) or (not pn in possible_subgrid):
                        current[i,j] = pn
                        #p.pop(ipn)
                        
                    # Blocks number in other submatrix
                    #current.copy()
                    #possible_
                    #for sij in get_complementary_subgrid_index(i,j,int(np.sqrt(rowcol_size))):
                    #    current_subgrid = get_subgrid_matrix(possible,*sij)
                        #if True:
                        #    p.pop(ipn)
                
    return current,loops,possible