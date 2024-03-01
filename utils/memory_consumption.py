import psutil
import os

def get_memory_consumption():
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_use = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
    return memory_use

def tell_memory_consumption():
    memory = get_memory_consumption()
    print("I use {0:.2f} GB..".format(memory))

# Call the function
tell_memory_consumption()
