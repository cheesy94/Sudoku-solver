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
                height=3,
                command=partial(increase,num[j][i])
            ).grid(row=i, column=j)
            
        
    btn_solve = tk.Button(
        text = "Solve",
        width = 25,
        height = 5,
        #command=
    )
    
    frm_sudoku.pack()
    btn_solve.pack()
    
    #window.update()
    window.mainloop()
    
    
    
    return

def increase(text):
    num = text.get()
    num = int(num) if num!="" else 0
    next_num = (num+1)%10
    text.set(str(next_num) if next_num else "")
    return

#def