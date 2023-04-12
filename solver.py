import numpy as np


## Get small grid index to which cell i,j belongs
def get_subgrid_index(i,j,size):
    
    subgrid_i = int(i/size)*size
    subgrid_j = int(j/size)*size
    
    return subgrid_i,subgrid_j

## Get small grid mask to which cell i,j belongs
def get_subgrid_mask(matrix,i,j):
    grid_size = int(np.sqrt(matrix.size))
    subgrid_size = int(np.sqrt(grid_size))
    
    si,sj = get_subgrid_index(i,j,subgrid_size)
    
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

## Delete possible number 
def filter_possible_numbers(matrix):
    rowcol_size = matrix.shape[0]
    
    for j in range(rowcol_size):
        for i in range(rowcol_size):
            p = matrix[i,j]
            lenp = len(p)
            
            if lenp==0:
                continue
            
            # Subgrid
            mask_col,mask_row = get_subgrid_mask(matrix,i,j)
            mask_col_neigh = mask_col.copy()
            mask_col_neigh[i] = False
            mask_row_neigh = mask_row.copy()
            mask_row_neigh[j] = False
            #mask = mask_col.reshape(rowcol_size,1) @ mask_row.reshape(1,rowcol_size)
            
            # Row
            pos_row = np.concatenate(matrix[i,:][~mask_row].flatten())
            pos_row_sg = np.concatenate(matrix[np.ix_(mask_col_neigh,mask_row)].flatten())
            
            # Col
            pos_col = np.concatenate(matrix[:,j][~mask_col].flatten())
            pos_col_sg = np.concatenate(matrix[np.ix_(mask_col,mask_row_neigh)].flatten())
            
            for pn in p:
                
                # Cell assured
                if lenp==1:
                    #del subgrid
                    del_possible_number(matrix[np.ix_(mask_col,mask_row)],pn)
                    del_possible_number(matrix[i,:],pn)
                    del_possible_number(matrix[:,j],pn)
                    matrix[i,j] = [pn]
                    continue
                
                # Row assured
                if (not pn in pos_row_sg) and (pn in pos_row):
                    del_possible_number(matrix[i,:][~mask_row],pn)
                    
                # Col assured
                if (not pn in pos_col_sg) and (pn in pos_col):
                    del_possible_number(matrix[:,j][~mask_col],pn)
                    
                # Pairs
                if lenp==2:
                    matrix_sg = matrix[np.ix_(mask_col,mask_row)]
                    matrix_neigh = matrix.copy()
                    matrix_neigh[i,j] = []
                    matrix_neigh_sg = matrix_neigh[np.ix_(mask_col,mask_row)]
                    
                    # Subgrid
                    if p in np.ndarray.tolist(matrix_neigh_sg.flatten()):
                        sg_indexes = np.where([[0 if matrix[np.ix_(mask_col,mask_row)][ii,jj]==p else 1 for jj in range(3)] for ii in range(3)])
                        del_possible_number(matrix_sg[sg_indexes],pn)
                            
    return matrix


## Solver
def solve(initial):
    
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
                    current[i,j] = p.pop(0)
                    continue
                
                # # Neighbours
                # possible_neighbours = possible.copy()
                # possible_neighbours[i,j] = []
                
                # for pn in p:
                    
                #     # Unique position in row, col, subgrid
                #     possible_row = np.unique(np.concatenate(possible_neighbours[i,:].flatten()))
                #     possible_col = np.unique(np.concatenate(possible_neighbours[:,j].flatten()))
                #     possible_subgrid = np.unique(np.concatenate(get_subgrid_matrix(possible_neighbours,i,j).flatten()))
                #     if (not pn in possible_row) or (not pn in possible_col) or (not pn in possible_subgrid):
                #         current[i,j] = pn
                #         #p.remove(pn)
                        
                    # Blocks number in other submatrix
                    #current.copy()
                    #possible_
                    #for sij in get_complementary_subgrid_index(i,j,int(np.sqrt(rowcol_size))):
                    #    current_subgrid = get_subgrid_matrix(possible,*sij)
                        #if True:
                        #    p.pop(ipn)
                
    return current,loops,possible