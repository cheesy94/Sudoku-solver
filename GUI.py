import tkinter as tk
from functools import partial

def draw(size=9, scale=60):
    
    window = tk.Tk()
    window.title("Sudoku")
    
    frm_sudoku = tk.Frame(
        master=window,
        width=scale*size,
        height=scale*size
        )
    
    num = []
    for j in range(size):
        num.append([None]*size)
        
        for i in range(size):
            num[j][i] = tk.StringVar()
            
            tk.Button(
                master = frm_sudoku,
                #text = "0",
                textvariable = num[j][i],
                width=5,
                height=2,
                command=partial(increase,num[j][i])
            ).grid(row=i, column=j)
            
        
    btn_solve = tk.Button(
        text = "Solve",
        width = 20,
        height = 4,
        command = window.quit
    )
    
    frm_sudoku.pack()
    btn_solve.pack()
    
    #window.update()
    window.mainloop()
    #window.destroy()
    
    return gui2int(num),num,window

def increase(text):
    num = text.get()
    num = int(num) if num!="" else 0
    next_num = (num+1)%10
    text.set(str(next_num) if next_num else "")
    return

def gui2int(arr):
    ret = [] # copy would only shallowcopy not deepcopy
    for j,row in enumerate(arr):
        ret.append(list())
        for i,col in enumerate(row):
            num = col.get()
            ret[j].append(int(num) if num!="" else 0)
    return ret

def int2gui(sol,arr):
    for j,row in zip(sol,arr):
        for i,col in zip(j,row):
            col.set(str(i))
    return arr