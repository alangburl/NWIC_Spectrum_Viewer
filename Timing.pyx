import numpy as np
def time_point(double[:] sync_time, double[:] detector_time, int s, double[:] bins, int b):
    '''Used to find the time spread of the pulses'''
    cdef int i,j
    cdef int dd=0
    cdef double[:] output= np.zeros(b)
    
    for i in range(s-1):
        while detector_time[dd]<sync_time[i+1]:
            for j in range(b-1):
                if detector_time[dd]-sync_time[i]>=bins[j] and detector_time[dd]-sync_time[i]<bins[j+1]:
                    output[j]+=1
            dd+=1
    
    return output

def channel_timing(double[:] sync_time,int s, double[:] detector_time, 
                   double[:] channels,double delta_time,int num_channels):
    cdef int d_loc=0
    cdef int split_loc=0
    cdef int i
    cdef double[:] region1_output=np.zeros(num_channels)
    cdef double[:] region2_output=np.zeros(num_channels)
    
    for i in range(s-1):
        while detector_time[d_loc]<sync_time[i]+delta_time:
            region1_output[int(channels[d_loc])]+=1
            d_loc+=1
        while detector_time[d_loc]<sync_time[i+1]:
            region2_output[int(channels[d_loc])]+=1
            d_loc+=1
    return region1_output, region2_output  