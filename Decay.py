#take the  file and load in the timing and channels
from List_Mode_Reader import List_Mode as LMR
import numpy as np
import scipy as sp
import time
class Background_Decay():
    def __init__(self, file_name,num_bins):
        self.timing,self.channels=LMR().read_file(file_name)
        print('Here')
        #calculate the total run time in microseconds
        total_time=self.timing[-1]-self.timing[0]
        #create the bins
        self.bins=np.linspace(0,num_bins,num_bins+1)
        self.timing_cutoff_points=np.linspace(self.timing[0],total_time,num_bins+1)
        
    def process_data(self):
        def exp_fit(x,tau):
            return np.exp(-x/tau)
        i=0
        bin_dic=[0]*len(self.bins)
        print('Begin processing:')
        s=time.time()
        for j in range(1,len(self.timing_cutoff_points)):
            while self.timing[i]<self.timing_cutoff_points[j]:
                bin_dic[j]+=1
                i+=1
        print('Processes in {:.2f}s'.format(time.time()-s))
        b_width=(self.timing_cutoff_points[1]-self.timing_cutoff_points[0])*1e-6
        print('Bin width of {:.3f}s'.format(b_width))
        rescale=[i*1e-6 for i in self.timing_cutoff_points] #convert to seconds from microseconds
        bins=[i/b_width for i in bin_dic] #convert to count rate by dividing the integrated counts by bin width
        print('Max count rate: {:.3f}'.format(max(bins)))
        print('Min count rate: {:.3f}'.format(min(bins[1::])))
        return bins, rescale
    
         