import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
import Timing

class List_Mode():
    def __init__(self,num_channels=8192):
        '''Delta time: offset after the sync pulse used to define regions 1 &2
                        in micro seconds
        '''
        super().__init__()
        self.num_channels=num_channels
        
    def read_file(self,file_location):
        '''Open and read the file into memory
        '''
        s=time.time()
        f=open(file_location,'r')
        data=f.readlines()
        f.close()
        print('File read in {:.2f}s'.format(time.time()-s))
        s=time.time()
        timing=[]
        channel=[]
#        n_data=np.asarray(data)
#        n_len=n_data.size
#        scalar=1e-6
#        timing,channel=Conversion.convert(n_data,n_len,scalar,1)
        for i in range(1,len(data)):
            vals=data[i].split(sep=';')
            timing.append(float(vals[0])*1e-6)
            channel.append(float(vals[1]))
        del data
        print('Loaded in {:.2f} s'.format(time.time()-s))
        return timing,channel
    
    def timing(self,delta_time,s_time,d_time,d_channels):
        self.delta_time=delta_time
        #get the sync pulse information
#        s_time,s_channels=self.read_file(self.file_location)
        #create two dictionaries: 1 for region one  and the other for region 2
        self.region1_spectrum={}
        self.region2_spectrum={}
        for i in range(self.num_channels):
            self.region1_spectrum[i]=0
            self.region2_spectrum[i]=0
        #convert the lists in np arrays for cython to work with
        
        sync_time=np.asarray(s_time)
        detec_time=np.asarray(d_time)
        detec_channels=np.asarray(d_channels)
        sync_num=sync_time.size
        #loop through the sync pulse times
#        d_loc=0
#        split_loc=0
        s=time.time()
        try:
            r1,r2=Timing.channel_timing(sync_time,sync_num,detec_time,
                                        detec_channels,delta_time,
                                        self.num_channels)
        except:
            sync_num-=1
            r1,r2=Timing.channel_timing(sync_time,sync_num,detec_time,
                                        detec_channels,delta_time,
                                        self.num_channels)
            
        for i in range(len(r1)):
            self.region1_spectrum[i]=r1[i]
            self.region2_spectrum[i]=r2[i]

        print('Process time {:.2f}'.format(time.time()-s))
        s=time.time()
        #convert the sync time and pulse times to np arrays for cython
        pulse_bins=100
        pulse_timing=np.linspace(0,(s_time[2]-s_time[1]),pulse_bins)

        pulse_times=Timing.time_point(sync_time,detec_time,sync_num,
                                      pulse_timing,pulse_bins)
        print('Process timing in: {:.2f}s'.format(time.time()-s))
        del sync_time
        del detec_time
        del s_time
        del d_time
        del d_channels
        return [self.region1_spectrum,self.region2_spectrum,
                [pulse_times,pulse_timing]]
