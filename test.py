import GPUtil
from time import sleep

gpu = GPUtil.getGPUs()

for i in gpu:
    print(i.load*100)