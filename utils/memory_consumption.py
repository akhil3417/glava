import psutil
import os


def get_memory_consumption():
    """
    Get the memory consumption of the current process in gigabytes.

    :return: The memory consumption of the current process in gigabytes.
    :rtype: float
    """
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_use = py.memory_info()[0] / 2.0**30  # memory use in GB...I think
    return memory_use


def tell_memory_consumption():
    """
    Function to retrieve memory consumption and print the result in gigabytes.
    No parameters.
    No return value.
    """
    memory = get_memory_consumption()
    print("I use {0:.2f} GB..".format(memory))
