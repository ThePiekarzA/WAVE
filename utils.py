

def getInx(ar1, len):
    elems = 0
    for i in range(ar1.size):
        if ar1[i] == 0.0:
            elems += 1
            if elems == len:
                return i-len+1
        else:
            elems = 0
