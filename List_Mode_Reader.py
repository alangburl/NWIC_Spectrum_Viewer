import numpy as np
import matplotlib.pyplot as plt
import os,sys
class List_Mode():
    def __init__(self,file_location):
        super().__init__()
        self.file_location=file_location
        
    def read_file(self):
        '''Open and read the file into memory
        '''
        
#        dty=np.dtype([('Time','f8'),('Heigt','f8')])
#        lis=np.loadtxt(self.file_location,delimiter=';',usecols=(0,1),dtype=dty,skiprows=1)
        f=open(self.file_location,'r')
        data=f.readlines()
        f.close()
        print('read')
        timing=[]
        channel=[]
        for i in range(1,len(data)):
            vals=data[i].split(sep=';')
            timing.append(float(vals[0])*1e-12)
            channel.append(float(vals[1]))
        return timing,channel
if __name__=="__main__":
        loc=os.path.join(os.getcwd(),'Test_Data')
        file=os.path.join(loc,'sync_pulse.csv')
        a=List_Mode(file)
        time,channel=a.read_file()
        print('Time between arrival: {:.2f} ms'.format((time[2]-time[1])*1e3))