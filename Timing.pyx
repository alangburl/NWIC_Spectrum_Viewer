import numpy as np
def time_point(double[:] sync_time, double[:] detector_time, int s, double[:] bins, int b):
    '''Used to find the time spread of the pulses'''
    cdef int i,j
    cdef int dd=0
    cdef double[:] output= np.zeros(b)
    
    for i in range(s-1):
        try:
            while detector_time[dd]<sync_time[i+1]:
                for j in range(b-1):
                    if detector_time[dd]-sync_time[i]>=bins[j] and detector_time[dd]-sync_time[i]<bins[j+1]:
                        output[j]+=1
                dd+=1
        except:
            a=True

    return output

def channel_timing(double[:] sync_time,int s, double[:] detector_time, 
                   double[:] channels,double delta_time,int num_channels):
    '''Used to split the total into different regions'''
    cdef int d_loc=0
    cdef int split_loc=0
    cdef int i
    cdef double[:] region1_output=np.zeros(num_channels)
    cdef double[:] region2_output=np.zeros(num_channels)
    cdef int a=0
    for i in range(s):
        try:
            while detector_time[d_loc]<sync_time[i]+delta_time:
                region1_output[int(channels[d_loc])]+=1
                d_loc+=1
            while detector_time[d_loc]<sync_time[i+1]:
                region2_output[int(channels[d_loc])]+=1
                d_loc+=1
        except:
            a+=1
    print(a)
    return region1_output, region2_output 

def channel_timing_roi(double[:] sync_time,int s, double[:] detector_time, 
                   double[:] channels,double delta_time,int num_channels):
    cdef int d_loc=0
    cdef int split_loc=0
    cdef int i
    cdef double[:] region1_output=np.zeros(num_channels)
    cdef double[:] region2_output=np.zeros(num_channels)
    cdef int a=0
    for i in range(s):
        try:
            while detector_time[d_loc]<sync_time[i]+delta_time:
                region1_output[int(channels[d_loc])]+=1
                d_loc+=1
            while detector_time[d_loc]<sync_time[i+1]:
                region2_output[int(channels[d_loc])]+=1
                d_loc+=1
        except:
            a+=1
    print(a)
    return region1_output, region2_output

def ROI_Timing(double[:] sync_time,int s, double[:] detector_time, 
               double[:] channels,double delta_time,int num_channels,
               double[:] calibration, double upper, double lower):
    '''Used to seperate the raw data into region 1 and 2 then keep the 
    associated time stamp with the raw pulse for detection probability 
    calculations'''
    cdef int d_loc=0
    cdef int split_loc=0
    cdef int i,j
    cdef int calib_len=len(calibration)
    j=0
    # cdef double[:] region1_output=np.zeros(num_channels)
    # cdef double[:] region2_output=np.zeros(num_channels)
    cdef int num_pulses=len(detector_time)
    cdef double[:] calibrated_pulse=np.zeros(num_pulses)
    
    #calibrate the raw spectrum
    for i in range(num_pulses):
        if int(channels[i]) < calib_len:
            calibrated_pulse[i]=calibration[int(channels[i])]
    
    cdef int num_roi_pulses=0
    #first determine the number of pulses that are in the ROI
    for i in range(num_pulses):
        if calibrated_pulse[i]>=lower and calibrated_pulse[i]<=upper:
            num_roi_pulses+=1
    
    cdef double[:] roi_pulses=np.zeros(num_roi_pulses)
    cdef double[:] roi_times=np.zeros(num_roi_pulses)
    #split into two regions and keep the associate detector time with the pulse
    for i in range(s):
        try:
            while detector_time[d_loc]<sync_time[i]+delta_time:
                # region1_output[int(channels[d_loc])]+=1
                d_loc+=1
            while detector_time[d_loc]<sync_time[i+1]:
                # region2_output[int(channels[d_loc])]+=1
                if calibrated_pulse[d_loc]>=lower and calibrated_pulse[d_loc]<=upper:
                    roi_pulses[j]=calibrated_pulse[d_loc]
                    roi_times[j]=detector_time[d_loc]
                    j+=1
                d_loc+=1
        except:
            a=True

    return roi_pulses[0:j-1], roi_times[0:j-1]