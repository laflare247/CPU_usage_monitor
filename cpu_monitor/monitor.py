import tkinter as tk
from tkinter import ttk
from cpu_info import Get_cpu_info

class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('450x450')
        self.resizable(width = True, height = True)
        self.title('CPU MONITOR')
        self.on_top = tk.IntVar()
        self.show_total = tk.IntVar(value = 1)
        self.show_cores = tk.IntVar(value = 1)
        
        self.tab_control = ttk.Notebook(self)
        self.main_tab = ttk.Frame(self.tab_control)
        self.cpu_info_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.main_tab, text = 'CPU Usage')
        self.tab_control.add(self.cpu_info_tab, text = 'CPU Info')
        self.tab_control.add(self.settings_tab, text = 'Settings')
        self.tab_control.pack(expand = 1, fill = tk.BOTH)

        self.cpu_info_frame = ttk.Labelframe(self.cpu_info_tab, text = 'CPU INFO', padding = 5)
        self.cpu_info_frame.grid(sticky = 'w')

        self.total_frame = ttk.LabelFrame(self.main_tab, text = 'TOTAL CPU USAGE', padding = 5)
        self.total_frame.grid(sticky = 'w')

        self.main_frame = ttk.Labelframe(self.main_tab, text = 'CPU USAGE', padding = 5)
        self.main_frame.grid(sticky = 'w')

        self.window_settings_frame = ttk.Labelframe(self.settings_tab, text = 'WINDOW SETTINGS')
        self.window_settings_frame.pack(fill = tk.X)

        self.interface_settings_frame = ttk.Labelframe(self.settings_tab, text = 'INTERFACE SETTINGS')
        self.interface_settings_frame.pack(fill = tk.X)

        self.cpu_info = Get_cpu_info()
        self.ph_cores_count = self.cpu_info.ph_cpu_count
        self.lg_cores_count = self.cpu_info.lg_cpu_count
        self.cpu_freq = self.cpu_info.cpu_freq
        self.usage_bars = {}
        self.usage_info = {}

        self.set_ui()

        self.update_usage_bars()

    def save_settings(self):
        self.attributes('-topmost', self.on_top.get())

        if self.show_total.get():
            self.total_frame.grid()
        else:
            self.total_frame.grid_remove()

        if self.show_cores.get():
            self.main_frame.grid()
        else:
            self.main_frame.grid_remove()

    def set_ui(self):
        
        label_ph_cores_count = ttk.Label(self.cpu_info_frame, text = f'Phisycal cores - {self.ph_cores_count}')
        label_lg_cores_count = ttk.Label(self.cpu_info_frame, text = f'Logic cores - {self.lg_cores_count}')
        label_ph_cores_count.grid(column = 0, row = 1, padx = 5)
        label_lg_cores_count.grid(column = 1, row = 1)

        label_cpu_freq = ttk.Label(self.cpu_info_frame, text = f'CPU Freq - {self.cpu_freq}')
        label_cpu_freq.grid(column = 0, row = 2, pady = 5)

        check_window_on_top = ttk.Checkbutton(self.window_settings_frame, text = 'Always on top', variable = self.on_top)
        check_window_on_top.pack(anchor = 'w')

        check_show_total = ttk.Checkbutton(self.interface_settings_frame, text = 'Show total CPU usage', variable = self.show_total)
        check_show_total.pack(anchor = 'w')

        check_show_cores = ttk.Checkbutton(self.interface_settings_frame, text = 'Show CPU cores usage', variable = self.show_cores)
        check_show_cores.pack(anchor = 'w')

        save_setting_button = ttk.Button(self.settings_tab, text = 'Save', command = self.save_settings)
        save_setting_button.pack()

        self.set_usage_bars()

    def set_usage_bars(self):
        
        for index in range(self.lg_cores_count):
            self.usage_info[index] = ttk.Label(master = self.main_frame,text = f'Core {index + 1} usage is 0%:')
            self.usage_bars[index] = ttk.Progressbar(master = self.main_frame, value = 0, length = 400)
            self.usage_info[index].pack(anchor = 'w')
            self.usage_bars[index].pack(anchor = 'w')

        self.usage_info[-1] = ttk.Label(master = self.total_frame, text = f'Total CPU usage is 0%:')
        self.usage_bars[-1] = ttk.Progressbar(master = self.total_frame, value = 0, length = 400)
        self.usage_info[-1].pack(anchor = 'w')
        self.usage_bars[-1].pack(anchor = 'w')

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