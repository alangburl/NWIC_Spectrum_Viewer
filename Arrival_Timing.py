import matplotlib.pyplot as plt
import numpy as np
from Conversion import convert
import time
class Arrival_Spread():
    def __init__(self,file_name):
        super().__init__()
        try:
            self.time,channel=convert(file_name)
            del channel
        except:
            pass
        
    def process(self):
       #determine the theoretical time between sync pulses
#       theo_time=1/self.frequency #Hz
       #determine the deltas between each sync pulse
       s=time.time()
       delta=[self.time[i+1]-self.time[i] for i in range(1,len(self.time)-2)]
       print('Process in {:.2f}s'.format(time.time()-s))
       #determine the mean and std. deviation of the deltas
       std_dev=np.std(delta)
       mean=np.average(delta)
#       print('Theoretical mean: {:.5f}'.format(theo_time))
       print('Mean: {:.5f}us\nStd. Dev: {:.5f}us'.format(mean,std_dev))
       print(max(delta),min(delta))
       plt.hist(delta,25)
       plt.ticklabel_format(useOffset=False,style='plain')
       plt.show()
#if __name__=="__main__":
    
        