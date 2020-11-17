'''create several different ways in which to calibrate detectors
'''
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class Detector_Calibration():
    def __init__(self,channels):
        super().__init__()
        self.channels=channels
        
    def linear_least_squares_fit(self,cal_channels,cal_energies,internal=False,
                                 live_plotter=False):
        '''Use a straight first order linear least squares regression
        to fit the channels and energies
        '''
#        print(cal_channels,cal_energies)
        bins=np.asarray(cal_channels).reshape((-1,1))
        energies=np.asarray(cal_energies)
        
        reg=LinearRegression().fit(bins,energies)
        m=reg.coef_[0]
        b=reg.intercept_
        if not internal:
            calibrated=[m*i+b for i in self.channels]
            if live_plotter:
                return calibrated,m,b
            elif live_plotter==False:
                return calibrated
        else:
            return m,b
        
    def external_calibration(self,m,b):
        '''Takes a slope and intercept to calibrate the 
        channels and returns a list of energies
        '''
        return [m*i+b for i in self.channels]
    
    def deviation_pairs(self,cal_channels,cal_energies):
        '''Use the deviation pairs to look at the linear deviations
        '''
        cal_channels=sorted(cal_channels)
        cal_energies=sorted(cal_energies)
        #get a least squares fit for all the data
        m,b=self.linear_least_squares_fit(cal_channels,cal_energies,True)
        #make sure the channels are integers
        channels=[int(i) for i in self.channels]
        line=[m*x+b for x in channels]
        
        segs=self.segmented_linear_least_squares(cal_channels,cal_energies)
        self.dev=[line[i]-segs[i] for i in range(len(line))]
        return segs
            
    def segmented_linear_least_squares(self,cal_channels,cal_energies):
        '''Do a linear fit between each of the cal_channels and 
        cal_energies to try and alleviate the nonlinearity
        '''
        #sort the channels and energies into ascending order
        channel_ordered=sorted(cal_channels)
        energies_ordered=sorted(cal_energies)
        #get a slope and intercept for each of the possible pairs
        slopes=[]
        intercepts=[]
        for i in range(len(channel_ordered)-1):
            x=[channel_ordered[i],channel_ordered[i+1]]
            y=[energies_ordered[i],energies_ordered[i+1]]
            vals=self.linear_least_squares_fit(x,y,internal=True)
            slopes.append(vals[0])
            intercepts.append(vals[1])
            
        #apply the calibration only to the specific part of the energy range
        calibrate_values=[]
        for h in self.channels:
            if h<=channel_ordered[0]:
#                print(slopes[0])
                calibrate_values.append(h*slopes[0]+intercepts[0])
#        print(len(calibrate_values))
        for i in range(len(channel_ordered)-1):
            for j in self.channels:
                if j>channel_ordered[i] and j<=channel_ordered[i+1]:
                    calibrate_values.append(j*slopes[i]+intercepts[i])
#        print(len(calibrate_values))
        for k in self.channels:
            if k>channel_ordered[-1]:
                calibrate_values.append(k*slopes[-1]+intercepts[-1])
#        print(len(calibrate_values))        
        return calibrate_values
                    
                
if __name__=="__main__":
    b=np.linspace(0,1024,1025)
    e=np.linspace(0,3000,1025)
    tester=Detector_Calibration(b)
    lin=tester.linear_least_squares_fit([226,400,453],[662, 1173,1330])
    plt.plot(b,lin,label='Linear')
    lin2=tester.segmented_linear_least_squares([226,400,700,800],[662, 1173,1330,2500])
    plt.plot(b,lin2,label='Segemented')
    lin3,deva=tester.deviation_pairs([226,400,700,800],[662, 1173,1330,2500])
    plt.plot(b,lin3,label='Deviation')
    plt.legend()
    plt.show()
    plt.figure(2)
    plt.plot([226,400,700,800],deva)
    plt.show()