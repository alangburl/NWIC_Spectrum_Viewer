#take the  file and load in the timing and channels
from List_Mode_Reader import List_Mode as LMR
import numpy as np
class Background_Decay():
    def __init__(self, file_name,num_bins):
        self.timing,self.channels=LMR().read_file(file_name)
        
        #calculate the total run time in microseconds
        total_time=self.timing[-1]-self.timing[0]
        #create the bins
        self.bins=np.linspace(0,num_bins,num_bins+1)
        self.timing_cutoff_points=np.linspace(self.timing[0],total_time,num_bins+1)
        
    def process_data(self):
        i=0
        bin_dic={}
        for k in self.bins:
            bin_dic[k]=0
        for j in range(1,len(self.timing_cutoff_points)):
            while self.timing[i]<self.timing_cutoff_points[j]:
                bin_dic[j]+=1
                i+=1
        return bin_dic, self.timing_cutoff_points