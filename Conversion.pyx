import numpy as np

def convert(data,int data_len,float scalar,int offset):
    cdef int i
    cdef double[:] times=np.zeros(data_len)
    cdef double[:] channel=np.zeros(data_len)
    for i in range(offset,data_len):
        times[i]=float(data[i].split(sep=';')[0])*scalar
        channel[i]=float(data[i].split(sep=';')[1])
    return times, channel