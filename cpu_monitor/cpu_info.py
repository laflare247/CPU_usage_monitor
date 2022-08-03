import psutil

class Get_cpu_info:

    def __init__(self):
        self.ph_cpu_count = psutil.cpu_count(logical = False)
        self.lg_cpu_count = psutil.cpu_count(logical = True)

    def get_cpu_percent(self):
        return psutil.cpu_percent(percpu = True)

    def get_total_cpu_percent(self):
        return psutil.cpu_percent(percpu = False)