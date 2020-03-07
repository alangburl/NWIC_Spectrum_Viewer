import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
class List_Mode():
    def __init__(self,delta_time,file_location=None,sync_file_location=None,
                 num_channels=8192):
        super().__init__()
        self.file_location=sync_file_location
        self.location=file_location
        self.delta_time=delta_time
        self.num_channels=num_channels
        
    def read_file(self,file_location):
        '''Open and read the file into memory
        '''
#        dty=np.dtype([('Time','f8'),('Heigt','f8')])
#        lis=np.loadtxt(self.file_location,delimiter=';',usecols=(0,1),dtype=dty,skiprows=1)
        s=time.time()
        f=open(file_location,'r')
        data=f.readlines()
        f.close()
        print('File read in {:.2f}s'.format(time.time()-s))
        s=time.time()
        timing=[]
        channel=[]
        for i in range(1,len(data)):
            vals=data[i].split(sep=';')
            timing.append(float(vals[0])*1e-6)
            channel.append(float(vals[1]))
        print('Loaded in {:.2f} s'.format(time.time()-s))
        return timing,channel
    
    def timing(self):
        #get the sync pulse information
        s_time,s_channels=self.read_file(self.file_location)
        #create two dictionaries: 1 for region one  and the other for region 2
        region1_spectrum={}
        region2_spectrum={}
        for i in range(self.num_channels):
            region1_spectrum[i]=0
            region2_spectrum[i]=0
        #create two floats, for the region 1 gross counts and region 2 gross counts
        region1_counts=0
        region2_counts=0
        #get the spectral data 
        d_time,d_channels=self.read_file(self.location)
        
        #loop through the sync pulse times
        d_loc=0
        for i in range(0,1000):
            #loop through the spectral data until the next sync pulse occurs
            while d_time[d_loc]<s_time[i]+self.delta_time:
                region1_counts+=1
                region1_spectrum[d_channels[d_loc]]+=1
                d_loc+=1
            while d_time[d_loc]<s_time[i+1]:
                region2_counts+=1
                region2_spectrum[d_channels[d_loc]]+=1
                d_loc+=1
        return region2_spectrum,region2_counts,region1_spectrum,region1_counts
             
if __name__=="__main__":
        loc=os.path.join(os.getcwd(),'Test_Data')
        file=os.path.join(loc,'sync1.csv')
        file1=os.path.join(loc,'spectrum1.csv')
        a=List_Mode(10,file1,file)
        spec2,coun2,spec1,coun1=a.timing()
#        time2,channel2=a.read_file(file)
#        time1,channel1=a.read_file(file1)
#        print('Time between arrival: {:.2f} ms'.format((time[2]-time[1])*1e3))