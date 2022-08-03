import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Window')
root.geometry('600x600')

tab_control = ttk.Notebook()
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text = "Первая вкладка")
tab_control.add(tab2, text = "Вторая вкладка")

label1 = ttk.Label(tab1, text = 'Привет! Я в первой вкладке')
label1.pack()
label2 = ttk.Label(tab2, text = 'Привет! Я во второй вкладке')
label2.pack()

tab_control.pack(fill = tk.BOTH, expand = 1)


root.mainloop()