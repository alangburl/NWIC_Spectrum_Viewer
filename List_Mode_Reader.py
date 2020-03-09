import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
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
        #two different lists one to go from the sync pulse to the 
        #region divider time and the other from the region divider time
        #to the next sync pulse
#        region_1_timing_splits=np.linspace(0,self.delta_time,10)
#        region_2_timing_splits=np.linspace(self.delta_time,
#                                           s_time[1]-s_time[0],10)
#        region_1_counts=[0]*len(region_1_timing_splits)
#        region_2_counts=[0]*len(region_2_timing_splits)
        #get the spectral data 
#        d_time,d_channels=self.read_file(self.location)
        #loop through the sync pulse times
        d_loc=0
        s=time.time()
        for i in range(len(s_time)-1):
            #loop through the spectral data until the next sync pulse occurs
            while d_time[d_loc]<s_time[i]+self.delta_time:
#                for j in range(len(region_1_timing_splits)-1):
#                    if d_time[d_loc]<region_1_timing_splits[j+1]+s_time[i] \
#                    and d_time[d_loc]>=region_1_timing_splits[j]+s_time[i]:
#                        region_1_counts[j]+=1
#                        break
                self.region1_spectrum[d_channels[d_loc]]+=1
                d_loc+=1
                
            while d_time[d_loc]<s_time[i+1]:
#                for j in range(len(region_2_timing_splits)-1):
#                    if d_time[d_loc]<region_2_timing_splits[j+1]+s_time[i] \
#                    and d_time[d_loc]>=region_2_timing_splits[j]+s_time[i]:
#                        region_2_counts[j]+=1
#                        break
                self.region2_spectrum[d_channels[d_loc]]+=1
                d_loc+=1
        print('Process time {:.2f}'.format(time.time()-s))
#        self.save_spectrum()
        del s_time
        del d_time
        del d_channels
        return [self.region1_spectrum,self.region2_spectrum]
             
    def save_spectrum(self):
        '''save the spectrum in region one and two
        '''
        f=open('region1_.csv','w')
        h=open('region2_.csv','w')
        for i in range(len(list(self.region1_spectrum.values()))-1):
            f.write('{}\n'.format(self.region1_spectrum[i]))
            h.write('{}\n'.format(self.region2_spectrum[i])) 
        f.close()
        h.close()
#if __name__=="__main__":
#        loc=os.path.join(os.getcwd(),'Test_Data')
#        file=os.path.join(loc,'905_1.csv')
#        file1=os.path.join(loc,'905_3.csv')
#        a=List_Mode(file1,file)
#        spec2,coun2,spec1,coun1,t1,t2=a.timing(70)
#        plt.figure(1)
#        plt.plot(list(spec2.keys())[0:2000],list(spec2.values())[0:2000])
#        plt.yscale('log')
#        plt.ylabel('Counts')
#        plt.xlabel('Channels')
#        plt.title('Region 2 Spectrum')
#        plt.savefig('Region2.png',dpi=600,figsize=(6,6))
#        plt.show()
#        plt.figure(2)
#        plt.plot(list(spec1.keys())[0:2000],list(spec1.values())[0:2000])
#        plt.yscale('log')
#        plt.ylabel('Counts')
#        plt.xlabel('Channels')
#        plt.title('Region 1 Spectrum')
#        plt.savefig('Region1.png',dpi=600,figsize=(6,6))
#        plt.show()