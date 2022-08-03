import tkinter as tk
from tkinter import ttk
from cpu_info import Get_cpu_info

class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x600')
        self.resizable(width = True, height = True)
        self.title('CPU MONITOR')
        self.attributes('-topmost', True)

        self.cpu_info = Get_cpu_info()
        self.ph_cores_count = self.cpu_info.ph_cpu_count
        self.lg_cores_count = self.cpu_info.lg_cpu_count
        self.usage_bars = {}
        self.usage_info = {}

        self.set_ui()

        self.update_usage_bars()


    def set_ui(self):
        top_frame = ttk.Labelframe(text = 'CPU INFO', padding = 5)
        top_frame.pack(fill = tk.X)

        label_ph_cores_count = ttk.Label(top_frame, text = f'Phisycal cores - {self.ph_cores_count}')
        label_lg_cores_count = ttk.Label(top_frame, text = f'Logic cores - {self.lg_cores_count}')
        label_ph_cores_count.grid(column = 1, row = 1, padx = 5)
        label_lg_cores_count.grid(column = 2, row = 1, padx = 15)

        self.set_usage_bars()

    
    def set_usage_bars(self):
        total_frame = ttk.LabelFrame(text = 'TOTAL CPU USAGE', padding = 5)
        total_frame.pack(fill = tk.X)

        main_frame = ttk.Labelframe(text = 'CPU USAGE', padding = 5)
        main_frame.pack(fill = tk.X)

        for index in range(self.lg_cores_count):
            self.usage_info[index] = ttk.Label(master = main_frame,text = f'Core {index + 1} usage is 0%:')
            self.usage_bars[index] = ttk.Progressbar(master = main_frame, value = 0, length = 400)
            self.usage_info[index].pack(anchor = 'w', padx = 7, pady = 5)
            self.usage_bars[index].pack(anchor = 'w', padx = 8)

        self.usage_info[-1] = ttk.Label(master = total_frame, text = f'Total CPU usage is 0%:')
        self.usage_bars[-1] = ttk.Progressbar(master = total_frame, value = 0, length = 400)
        self.usage_info[-1].pack(anchor = 'w', padx = 7)
        self.usage_bars[-1].pack(anchor = 'w', padx= 7)

    def update_usage_bars(self):
        usage = self.cpu_info.get_cpu_percent()
        total_usage = self.cpu_info.get_total_cpu_percent()

        self.usage_info[-1].configure(text = f'Total CPU usage is {total_usage}%:')
        self.usage_bars[-1].configure(value = total_usage)

        for index in range(len(self.usage_bars) - 1):
            self.usage_info[index].configure(text = f'Core {index + 1} usage is {usage[index]}%:')
            self.usage_bars[index].configure(value = usage[index])

        self.after(ms = 1000, func = self.update_usage_bars)

if __name__ == '__main__':
    root = Application()
    root.mainloop()