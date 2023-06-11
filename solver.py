import numpy as np


## Solver
def solve(initial):
    
    initial = np.array(initial)
    rowcol_size = int(np.sqrt(initial.size))

    current = initial.copy()
    previous = np.zeros_like(current)
    loops = 0
    
    
    while (current == 0).any():
        # Check forever loop
        if (previous == current).all(): # or not any(map(len,possible.flatten())):
            print("Exiting infinite loop")
            # DO SMTH
            break
        previous = current.copy()
        
        # Count loops
        loops+=1
        
        # Get possible numbers for every cell                                   #!!! sacarlo del bucle
        possible = get_possible_numbers(current)
        
        # Filter possible numbers
        possible = filter_possible_numbers(possible)
        
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
                    add_number(current,i,j,p[0],possible)
                    continue
                
                # Neighbours
                possible_neighbours = possible.copy()
                possible_neighbours[i,j] = []
                
                for pn in p:
                    
                    # Unique position in row, col, subgrid
                    possible_row = np.unique(np.concatenate(possible_neighbours[i,:].flatten())) # unique not needed
                    possible_col = np.unique(np.concatenate(possible_neighbours[:,j].flatten()))
                    possible_subgrid = np.unique(np.concatenate(get_subgrid_matrix(possible_neighbours,i,j).flatten()))
                    if (not pn in possible_row) or (not pn in possible_col) or (not pn in possible_subgrid):
                        add_number(current,i,j,pn,possible)
                        break
                
    return current,loops,possible

#############################################################################

## Get small grid mask to which cell i,j belongs
def get_subgrid_mask(matrix,i,j):
    grid_size = int(np.sqrt(matrix.size))
    subgrid_size = int(np.sqrt(grid_size))
    
    #si,sj = get_subgrid_index(i,j,subgrid_size)
    si = int(i/subgrid_size)*subgrid_size
    sj = int(j/subgrid_size)*subgrid_size

    mask_i = np.zeros(grid_size,dtype=bool)
    mask_j = np.zeros(grid_size,dtype=bool)
    mask_i[si:si+subgrid_size] = 1
    mask_j[sj:sj+subgrid_size] = 1
    
    return mask_i,mask_j

## Get small grid i,j
def get_subgrid_matrix(matrix,i,j):
    mask_i,mask_j = get_subgrid_mask(matrix,i,j)
    
    return matrix[np.ix_(mask_i,mask_j)]

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

## Delete possible number
def del_possible_number(matrix,num):
    np.vectorize(lambda x: x.remove(num) if(num in x) else None)(matrix)
    return matrix

## Add number and delete from possible
def add_number(matrix,i,j,num,possible):
    matrix[i,j] = num
    
    del_possible_number(possible[i,:],num)
    del_possible_number(possible[:,j],num)
    del_possible_number(get_subgrid_matrix(possible,i,j),num)
    
    return matrix,possible

## Filter possible numbers
def filter_possible_numbers(matrix):
    grid_size = matrix.shape[0]
    subgrid_size = int(np.sqrt(grid_size))
    
    for j in range(grid_size):
        for i in range(grid_size):
            p = matrix[i,j]
            lenp = len(p)
            
            if lenp==0:
                continue

            # Cell assured
            if lenp==1:
                pn = p[0]
                del_possible_number(matrix[i,:],pn)
                del_possible_number(matrix[:,j],pn)
                del_possible_number(get_subgrid_matrix(matrix,i,j),pn)
                
                matrix[i,j] = [pn]
                continue
            
            # Neighbours
            mask_col,mask_row = get_subgrid_mask(matrix,i,j)
            mask_col_neigh = mask_col.copy()
            mask_col_neigh[i] = False
            mask_row_neigh = mask_row.copy()
            mask_row_neigh[j] = False
            #mask = mask_col.reshape(grid_size,1) @ mask_row.reshape(1,grid_size)
            
            # Row
            pos_row = np.concatenate(matrix[i,:][~mask_row].flatten())
            pos_row_sg = np.concatenate(matrix[np.ix_(mask_col_neigh,mask_row)].flatten())
            
            # Col
            pos_col = np.concatenate(matrix[:,j][~mask_col].flatten())
            pos_col_sg = np.concatenate(matrix[np.ix_(mask_col,mask_row_neigh)].flatten())
            

            for pn in p:
                
                # Row assured
                if (not pn in pos_row_sg) and (pn in pos_row):
                    del_possible_number(matrix[i,:][~mask_row],pn)
                    
                # Col assured
                if (not pn in pos_col_sg) and (pn in pos_col):
                    del_possible_number(matrix[:,j][~mask_col],pn)
                    
                # Pairs
                if lenp==2:
                    
                    matrix_neigh = matrix.copy()
                    matrix_neigh[i,j] = []
                    
                    # Subgrid
                    matrix_sg = get_subgrid_matrix(matrix,i,j)
                    matrix_neigh_sg = get_subgrid_matrix(matrix_neigh,i,j)
                    
                    if p in np.ndarray.tolist(matrix_neigh_sg.flatten()):
                        sg_indexes = np.where([[0 if matrix_sg[ii,jj]==p else 1 for jj in range(subgrid_size)] for ii in range(subgrid_size)])
                        del_possible_number(matrix_sg[sg_indexes],pn)
                        
                    # Row
                    matrix_row = matrix[i,:]
                    matrix_neigh_row = matrix_neigh[i,:]
                    
                    if p in np.ndarray.tolist(matrix_neigh_row.flatten()):
                        row_indexes = np.where([0 if y==p else 1 for y in matrix_row])
                        del_possible_number(matrix_row[row_indexes],pn)
                    
                    # Col
                    matrix_col = matrix[:,j]
                    matrix_neigh_col = matrix_neigh[:,j]
                    
                    if p in np.ndarray.tolist(matrix_neigh_col.flatten()):
                        col_indexes = np.where([0 if x==p else 1 for x in matrix_col])
                        del_possible_number(matrix_col[col_indexes],pn)
                            
    return matrix