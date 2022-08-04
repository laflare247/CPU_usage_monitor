import tkinter as tk
from tkinter import ttk
from cpu_info import Get_cpu_info
from gpu_info import Get_gpu_info

class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('450x450')
        self.resizable(width = True, height = True)
        self.title('CPU GPU MONITOR')

        self.on_top = tk.IntVar()
        self.show_total = tk.IntVar(value = 1)
        self.show_cores = tk.IntVar(value = 1)
        self.show_gpu_usage = tk.IntVar(value = 1)
        self.show_gpu_temp = tk.IntVar(value = 1)
        self.show_temp_color = tk.IntVar(value = 1)
        self.show_temp_color_int = 1
        
        self.tab_control = ttk.Notebook(self)

        self.cpu_usage_tab = ttk.Frame(self.tab_control)

        self.gpu_usage_tab = ttk.Frame(self.tab_control)

        self.cpu_info_tab = ttk.Frame(self.tab_control)

        self.gpu_info_tab = ttk.Frame(self.tab_control)

        self.settings_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.cpu_usage_tab, text = 'CPU Usage')
        self.tab_control.add(self.gpu_usage_tab, text = 'GPU Usage')
        self.tab_control.add(self.cpu_info_tab, text = 'CPU Info')
        self.tab_control.add(self.gpu_info_tab, text = 'GPU Info')
        self.tab_control.add(self.settings_tab, text = 'Settings')
        self.tab_control.pack(expand = 1, fill = tk.BOTH)

        self.cpu_info_frame = ttk.Labelframe(self.cpu_info_tab, text = 'CPU INFO', padding = 5)
        self.cpu_info_frame.grid(sticky = 'w')

        self.total_frame = ttk.LabelFrame(self.cpu_usage_tab, text = 'TOTAL CPU USAGE', padding = 5)
        self.total_frame.grid(sticky = 'w')

        self.cpu_usage_frame = ttk.Labelframe(self.cpu_usage_tab, text = 'CPU USAGE', padding = 5)
        self.cpu_usage_frame.grid(sticky = 'w')

        self.gpu_info_frame = ttk.Labelframe(self.gpu_info_tab, text = 'GPU INFO', padding = 5)
        self.gpu_info_frame.grid(sticky = 'w')

        self.gpu_usage_frame = ttk.Labelframe(self.gpu_usage_tab, text = 'TOTAL GPU USAGE', padding = 5)
        self.gpu_usage_frame.grid(sticky = 'w')

        self.gpu_temp_frame = ttk.Labelframe(self.gpu_usage_tab, text = 'TOTAL GPU TEMP', padding = 5)
        self.gpu_temp_frame.grid(sticky = 'w')

        self.window_settings_frame = ttk.Labelframe(self.settings_tab, text = 'WINDOW SETTINGS')
        self.window_settings_frame.pack(fill = tk.X)

        self.cpu_interface_settings_frame = ttk.Labelframe(self.settings_tab, text = 'CPU INTERFACE SETTINGS')
        self.cpu_interface_settings_frame.pack(fill = tk.X)

        self.gpu_interface_settings_frame = ttk.Labelframe(self.settings_tab, text = 'GPU INTERFACE SETTINGS')
        self.gpu_interface_settings_frame.pack(fill = tk.X)

        self.cpu_info = Get_cpu_info()
        self.gpu_info = Get_gpu_info()
        self.ph_cores_count = self.cpu_info.ph_cpu_count
        self.lg_cores_count = self.cpu_info.lg_cpu_count
        self.cpu_freq = self.cpu_info.cpu_freq
        self.usage_bars = {}
        self.usage_info = {}
        self.gpu_usage_list = []
        self.gpu_temp_list = []

        self.set_ui()

        self.update_usage_bars()

    def save_settings(self):
        self.attributes('-topmost', self.on_top.get())

        if self.show_total.get():
            self.total_frame.grid()
        else:
            self.total_frame.grid_remove()

        if self.show_cores.get():
            self.cpu_usage_frame.grid()
        else:
            self.cpu_usage_frame.grid_remove()

        if self.show_gpu_usage.get():
            self.gpu_usage_frame.grid()
        else:
            self.gpu_usage_frame.grid_remove()

        if self.show_gpu_temp.get():
            self.gpu_temp_frame.grid()
        else:
            self.gpu_temp_frame.grid_remove()

        self.show_temp_color_int = self.show_temp_color.get()

    def set_ui(self):
        
        label_ph_cores_count = ttk.Label(self.cpu_info_frame, text = f'Phisycal cores - {self.ph_cores_count}')
        label_lg_cores_count = ttk.Label(self.cpu_info_frame, text = f'Logic cores - {self.lg_cores_count}')
        label_ph_cores_count.grid(sticky = 'w')
        label_lg_cores_count.grid(sticky = 'w')

        label_cpu_freq = ttk.Label(self.cpu_info_frame, text = f'CPU Freq - {self.cpu_freq}')
        label_cpu_freq.grid(sticky = 'w')

        self.set_gpu_ui()
        self.set_settings_ui()
        self.set_usage_bars()

    def set_gpu_ui(self):
        label_gpu_name = ttk.Label(self.gpu_info_frame, text = f'Name - {self.gpu_info.gpu_name}')
        label_gpu_name.grid(sticky = 'w')

        label_gpu_total_memory = ttk.Label(self.gpu_info_frame, text = f'Total memory - {self.gpu_info.gpu_total_memory} MB')
        label_gpu_total_memory.grid(sticky = 'w')

        label_gpu_used_memory = ttk.Label(self.gpu_info_frame, text = f'Used memory - {self.gpu_info.gpu_used_memory} MB')
        label_gpu_used_memory.grid(sticky = 'w')

        label_gpu_free_memory = ttk.Label(self.gpu_info_frame, text = f'Free memory - {self.gpu_info.gpu_free_memory} MB')
        label_gpu_free_memory.grid(sticky = 'w')

        gpu_usage_label = ttk.Label(self.gpu_usage_frame, text = 'Total GPU usage is 0%:')
        gpu_usage_label.grid(sticky = 'w')

        gpu_usage_bar = ttk.Progressbar(self.gpu_usage_frame, length = 400)
        gpu_usage_bar.grid(sticky = 'w')

        gpu_temp_label = ttk.Label(self.gpu_temp_frame, text = 'Total GPU temp is 0°C')
        gpu_temp_label.grid(sticky = 'w')

        self.gpu_usage_list.append(gpu_usage_label)
        self.gpu_usage_list.append(gpu_usage_bar)
        self.gpu_temp_list.append(gpu_temp_label)

    def set_settings_ui(self):
        check_window_on_top = ttk.Checkbutton(self.window_settings_frame, text = 'Always on top', variable = self.on_top)
        check_window_on_top.pack(anchor = 'w')

        check_show_total = ttk.Checkbutton(self.cpu_interface_settings_frame, text = 'Show total CPU usage', variable = self.show_total)
        check_show_total.pack(anchor = 'w')

        check_show_cores = ttk.Checkbutton(self.cpu_interface_settings_frame, text = 'Show CPU cores usage', variable = self.show_cores)
        check_show_cores.pack(anchor = 'w')

        check_show_gpu_usage = ttk.Checkbutton(self.gpu_interface_settings_frame, text = 'Show total GPU usage', variable = self.show_gpu_usage)
        check_show_gpu_usage.pack(anchor = 'w')

        check_show_gpu_temp = ttk.Checkbutton(self.gpu_interface_settings_frame, text = 'Show total GPU temp', variable = self.show_gpu_temp)
        check_show_gpu_temp.pack(anchor = 'w')

        check_show_temp_color = ttk.Checkbutton(self.gpu_interface_settings_frame, text = 'Show GPU temp color', variable = self.show_temp_color)
        check_show_temp_color.pack(anchor = 'w')

        save_setting_button = ttk.Button(self.settings_tab, text = 'Save', command = self.save_settings)
        save_setting_button.pack()

    def set_usage_bars(self):
        
        for index in range(self.lg_cores_count):
            self.usage_info[index] = ttk.Label(master = self.cpu_usage_frame,text = f'Core {index + 1} usage is 0%:')
            self.usage_bars[index] = ttk.Progressbar(master = self.cpu_usage_frame, value = 0, length = 400)
            self.usage_info[index].pack(anchor = 'w')
            self.usage_bars[index].pack(anchor = 'w')

        self.usage_info[-1] = ttk.Label(master = self.total_frame, text = f'Total CPU usage is 0%:')
        self.usage_bars[-1] = ttk.Progressbar(master = self.total_frame, value = 0, length = 400)
        self.usage_info[-1].pack(anchor = 'w')
        self.usage_bars[-1].pack(anchor = 'w')

    def update_usage_bars(self):
        usage = self.cpu_info.get_cpu_percent()
        total_usage = self.cpu_info.get_total_cpu_percent()

        total_gpu_usage = self.gpu_info.get_gpu_usage()
        total_gpu_temp = self.gpu_info.get_gpu_temp()

        self.usage_info[-1].configure(text = f'Total CPU usage is {total_usage}%:')
        self.usage_bars[-1].configure(value = total_usage)

        self.gpu_usage_list[0].configure(text = f'Total GPU usage is {round(total_gpu_usage)}%:')
        self.gpu_usage_list[1].configure(value = total_gpu_usage)

        for index in range(len(self.usage_bars) - 1):
            self.usage_info[index].configure(text = f'Core {index + 1} usage is {usage[index]}%:')
            self.usage_bars[index].configure(value = usage[index])

        if self.show_temp_color_int:
            if total_gpu_temp < 50:
                self.gpu_temp_list[0].configure(text = f'Total GPU temp is {total_gpu_temp}°C', background = '#BDECB6')
            elif total_gpu_temp > 50 and total_gpu_temp < 75:
                self.gpu_temp_list[0].configure(text = f'Total GPU temp is {total_gpu_temp}°C', background = '#EDFF21')
            else:
                self.gpu_temp_list[0].configure(text = f'Total GPU temp is {total_gpu_temp}°C', background = '#C41E3A')
        else:
            self.gpu_temp_list[0].configure(text = f'Total GPU temp is {total_gpu_temp}°C', background = '')

        self.after(ms = 1000, func = self.update_usage_bars)

if __name__ == '__main__':
    root = Application()
    root.mainloop()