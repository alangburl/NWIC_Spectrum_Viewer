#generate a CDF from a given array
import numpy as np

def CDF_Generator(double[:] fore,double[:] counts):
    cdef double[:] integral=np.zeros(len(counts))
    cdef int i=0
    cdef int ende=len(counts)
    
    for i in range(ende):
        integral[i]=np.trapz(fore[0:i])
    return integral