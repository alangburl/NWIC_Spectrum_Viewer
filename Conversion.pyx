import numpy as np

def convert(str file_name):
    f=open(file_name, 'r')
    data=f.readlines()
    f.close()
    cdef int l=len(data)
    cdef double[:] timer=np.zeros(l)
    cdef double[:] channel=np.zeros(l)
    
    cdef int i
#    cdef str[4] d
    
    for i in range(1,l):
        d=data[i].split(sep=';')
        timer[i]=float(d[0])*1e-6
        channel[i]=float(d[1])
    return timer, channel