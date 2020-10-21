import numpy as np

def ROI_Arrival(double[:] sync_time, double[:] detector_time, int s, 
               double[:] pulse_height, int num_pulses, 
               double lower, double upper, double[:] calibration):
    '''Used to find the time spread of the pulses'''
    cdef int i,j
    cdef int dd=0
    cdef int num_roi_pulses=0
    cdef int calib_len=len(calibration)
    #convert the pulse heights to energy
    cdef double[:] calibrated_pulse=np.zeros(num_pulses)
    for i in range(num_pulses):
        if int(pulse_height[i]) < calib_len:
            calibrated_pulse[i]=calibration[int(pulse_height[i])]
        
    #first determine the number of pulses that are in the ROI
    for i in range(num_pulses):
        if calibrated_pulse[i]>=lower and calibrated_pulse[i]<=upper:
            num_roi_pulses+=1
    #create a numpy array for the arrival times of the pulses
    cdef double[:] roi_pulse_arrival=np.zeros(num_roi_pulses)
    cdef double[:] roi_arrival_raw=np.zeros(num_roi_pulses)
    cdef double[:] roi_pulse_heights=np.zeros(num_roi_pulses)
    cdef int roi_processed=0
    cdef double init=detector_time[0]
    for i in range(s-1):
        while detector_time[dd]<sync_time[i+1]:
            if roi_processed<=num_roi_pulses:
                if calibrated_pulse[dd]>=lower and calibrated_pulse[dd]<=upper:
                    roi_pulse_arrival[roi_processed]=detector_time[dd]-sync_time[i]
                    roi_arrival_raw[roi_processed]=detector_time[dd]-init
                    roi_pulse_heights[roi_processed]=calibrated_pulse[dd]
                    roi_processed+=1
                dd+=1
            else:
                break
    return roi_pulse_arrival, roi_pulse_heights,roi_arrival_raw

def ROI_Location(double[:] times, double[:] bins, int b,int s):
    cdef double[:] output=np.zeros(b)
    cdef int i,j
    for i in range(s):
        for j in range(b-1):
            if times[i]>=bins[j] and times[i]<bins[j+1]:
                output[j]+=1    
            
    return output
    
    
