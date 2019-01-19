import numpy as np

# returns number of probes corresponding to the given time interval
def getIntervalSize(time_s, frequency):
    return np.uint16(time_s * frequency)

# looks for a given number of zeros in array and returns index of first occurrence
def getInx(ar1, len):
    elems = 0
    for i in range(ar1.size):
        if ar1[i] == 0.0:
            elems += 1
            if elems == len:
                return i-len+1
        else:
            elems = 0
