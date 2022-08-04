from GPUtil import getGPUs

class Get_gpu_info:

    def __init__(self):
        self.gpu_info = getGPUs()

        for gpu in self.gpu_info:
                self.gpu_name = gpu.name
                self.gpu_free_memory = gpu.memoryFree
                self.gpu_used_memory = gpu.memoryUsed
                self.gpu_total_memory = gpu.memoryTotal

    def get_gpu_usage(self):
        self.return_gpu_usage = getGPUs()

        for gpu in self.return_gpu_usage:
            self.gpu_usage = gpu.load * 100
        
        return self.gpu_usage

    def get_gpu_temp(self):
        self.return_gpu_temp = getGPUs()

        for gpu in self.return_gpu_temp:
            self.gpu_temp = gpu.temperature
        
        return self.gpu_temp