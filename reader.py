import numpy as np

def str2arr(txt):
    return np.array(list(map(int,txt.split(","))))

def arr2mat(arr):
    rowcol_size = int(np.sqrt(arr.size))
    return arr.reshape(rowcol_size,rowcol_size)

def read_db(file,n):
    with open(file,'r') as fp:
        for index, line in enumerate(fp):
            ini,sol,_ = line.split(";")
            #print(ini,sol)
            if index==n:
                break;
    
    return arr2mat(str2arr(ini)),arr2mat(str2arr(sol))