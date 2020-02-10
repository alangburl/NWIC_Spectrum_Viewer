import numpy as np
import matplotlib.pyplot as plt
import os
class Spectra_Analysis():
    figure_number=1
    def __init__(self,foreground_location, 
                 background_location=None,
                 zero_offset_fore=6,zero_offset_back=6,
                 save_folder=None):
        '''
        Used to analyze various spectral features:
            Takes as arguements:
                foreground_location- string of the full path to uncalibrated
                                     spectrum files. Expects to only have 
                                     a single column of the counts
                                     having length of number of bins
               background_location- string of full path to uncalibrated
                                    background spectrum. Expects same 
                                    information as foreground_location  
               zero_offset_fore- int indicating start line in the 
                                   foreground spectrum
               zero_offset_back- int indicating start line in the 
                                   background spectrum
               save_folder- full path to the folder to save images in 
        '''
        super().__init__()
        #read in the foreground spectrum and create an associated bins
        #array  to go with it
        f=open(foreground_location,'r')
        f_data=f.readlines()
        f.close()
        self.fore_bins=[]
        self.fore_counts=[]
        for i in range(zero_offset_fore,len(f_data)):
            self.fore_bins.append(i)
            self.fore_counts.append(float(f_data[i]))
        #if a background file exists read in the data 
        self.back_bins=[]
        self.back_counts=[]
        if background_location!=None:
            g=open(background_location,'r')
            b_data=g.readlines()
            g.close()
            for j in range(zero_offset_back,len(b_data)):
                self.back_bins.append(j)
                self.back_counts.append(float(b_data[j]))
        if save_folder==None:
            self.save_folder=os.getcwd()
        else:
            self.save_folder=save_folder
                
    def average_count_rate(self,foreground_duration, background_duration=None):
        '''Calculate the average count rate for the foreground and 
        backgound if included.
            Takes as arguments:
                foreground_duration- float of foreground accumulation time
                background_duration- float of background accumulation time
                                        defaults to None
        '''
        fore_sum=np.sum(self.fore_counts)
        fore_rate=fore_sum/foreground_duration
        if len(self.back_counts)!=0:
            back_sum=np.sum(self.back_counts)        
            back_rate=back_sum/background_duration
            return fore_rate,back_rate
        else:
            return fore_rate,0
        
    def background_subtraction(self):
        '''
        Subtract the background from the foreground to see the total signature
        '''
        if len(self.back_bins)!=len(self.fore_bins):
            raise ValueError('Background of length {}, can\'t be substracted from Foreground of length {}'.format(len(self.back_bins),len(self.fore_bins)))
        else:
            self.subtracted_counts=[]
            for h in range(len(self.back_bins)):
                self.subtracted_counts.append(
                        self.fore_counts[h]-self.back_counts[h])
                
    def rate_normalization(self,fore_duration,back_duration):
        '''Used to rate normalize the two spectrum
            Takes as arguments:
                    fore_duration- float duration of foreground accumulation
                    back_duration- float duration of background accumulation
        '''
        self.fore_rates=[i/fore_duration for i in self.fore_counts]
        self.back_rates=[j/back_duration for j in self.back_counts]
        
    def raw_spectrum_plotter(self, first_label,title,second_label=None,yscale='linear'):
        '''
        Plot the raw foreground and background on top of each other 
        Takes as arguments:
            first_label: string of first spectrum label
            second_label: string of second spectrum label
            title: descriptive title of the graph
        '''
        plt.figure(self.figure_number,figsize=[12,12])
        self.figure_number+=1
        if second_label!=None:
            plt.plot(self.back_bins,self.back_counts,label=second_label)
        plt.plot(self.fore_bins,self.fore_counts,label=first_label)
        plt.xlabel('Bins')
        plt.ylabel('Counts')
        plt.yscale(yscale)
        plt.title(title)
        plt.legend()
        plt.savefig(os.path.join(self.save_folder,
                                 '{}_{}.jpg'.format(title,yscale)),dpi=600)
        plt.show()
        
    def rate_spectrum_plotter(self, first_label, second_label,title):
        '''
        Plot the raw foreground and background on top of each other 
        Takes as arguments:
            first_label: string of first spectrum label
            second_label: string of second spectrum label
            title: descriptive title of the graph
        '''
        plt.figure(self.figure_number)
        self.figure_number+=1
        plt.plot(self.back_rates,self.back_counts,label=first_label)
        plt.plot(self.fore_rates,self.fore_counts,label=second_label)
        plt.xlabel('Bins')
        plt.ylabel('Counts Rates')
        plt.title(title)
        plt.show()
        
    def calibrated_spectrum_plotter(self, first_label, title,calibrate,
                                    second_label=None,yscale='linear',
                                    energies=None,zoomed=None,
                                    back_calibration=None,
                                    xtick_remove=None,
                                    calibration_lines=None):
        plt.figure(self.figure_number,figsize=[12,5.5])
        self.figure_number+=1
        zoomer=[]
        zoomed_calibrate=[]
        zoomer_back=[]
        zoomed_back2=[]
        zoomed_back=[]
        if zoomed!=None:
            for j in range(len(calibrate)):
                if calibrate[j]>= min(zoomed) and calibrate[j]<=max(zoomed):
                    zoomer.append(calibrate[j])
                    zoomed_calibrate.append(self.fore_counts[j])
                    if second_label!=None:
                        zoomed_back.append(self.back_counts[j])
            if back_calibration!=None and second_label!=None:
                for k in range(len(back_calibration)):
                    if back_calibration[k]>=min(zoomed) and back_calibration[k]<=max(zoomed):
                        zoomer_back.append(back_calibration[k])
                        zoomed_back2.append(self.back_counts[k])
                        
        if len(zoomer)>0:
            if second_label!=None:
                if back_calibration==None:
                    plt.plot(zoomer,zoomed_back,label=second_label)
                else:
                    plt.plot(zoomer_back,zoomed_back2,label=second_label)
            plt.plot(zoomer,zoomed_calibrate,label=first_label)
            plt.xlim(zoomed[0],zoomed[1])
        else:
            if second_label!=None:
                if back_calibration==None:
                    plt.plot(calibrate,self.back_counts,label=second_label)
                else:
                    plt.plot(back_calibration,self.back_counts,label=second_label)
                    
            plt.plot(calibrate,self.fore_counts,label=first_label)
            
        #add the energy lines to the graph
        if energies!=None:
            for i in energies:
                plt.axvline(x=i,linestyle='--',color='k',linewidth=0.5)
            loc,label=plt.xticks()
            for i in range(len(loc)-1):
                if loc[i]>=0:
                    if round(loc[i],3)!=xtick_remove:
                        energies.append(loc[i])
            plt.xticks(energies,fontsize=10, rotation=90)
        if calibration_lines!=None:
            for i in calibration_lines:
                plt.axvline(x=i, linestyle='-',color='r',linewidth=0.8)
        plt.xlabel('Energy [MeV]')
        plt.ylabel('Counts')
        plt.yscale(yscale)
        plt.title(title)
        plt.legend()
        plt.savefig(os.path.join(self.save_folder,
                                 'calibrated{}_{}.jpg'.format(title,yscale)),
                                    dpi=500)
        plt.show()
        
    def subtracted_spectrum_plotter(self,title):
        '''Plot the background subtracted spectrum
            Takes as arguement:
                title- descriptive title of the graph
        '''
        plt.figure(self.figure_number)
        self.figure_number+=1
        plt.plot(self.back_bins,self.subtracted_counts,
                 label='No target subtracted spectrum')
        plt.xlabel('Bins')
        plt.ylabel('Counts')
        plt.title(title)
        plt.show()        
        
    def HPGE_calibration(self, energy_per_bin=0.003, background_calibration=None):
        '''Used to calibrate the HPGE detector using a linear fit
            energy_per_bin:  float
            background_calibration: boolean, true to calibrate background 
                                    spectrum'''
        if background_calibration==None:
            calibrated=[i*energy_per_bin for i in self.fore_bins]
        elif background_calibration!=None:
            calibrated=[i*energy_per_bin for i in self.back_bins]
        return calibrated
    
    def KNIFE_calibration(self, bins, energies, background_calibration=None,
                          scalar=1,m=None,b=None):
        '''used to calibrate the KNIFE detector
        Takes as arguements:
            bins: a list of bins associated with each energy found in energies
            energies: a list of energies based on the bins
            background_calibration: boolean, true to calibrate background 
                                    spectrum
        '''
        bins=np.asarray(bins)
        energies=np.asarray(energies)
#        x_2=[i**2 for i in bins]
#        xy=[bins[i]*energies[i] for i in range(len(bins))]
        if m==None:
            n=np.size(bins)
            m_x,m_y=np.mean(bins),np.mean(energies)
            xy=np.sum(bins*energies)-n*m_y*m_x
            xx=np.sum(bins*bins)-n*m_x*m_x
            m=xy/xx
            b=m_y-m*m_x

        if background_calibration==None:
            calibrated=[scalar*(m*i+b) for i in self.fore_bins]
        elif background_calibration!=None:
            calibrated=[scalar*(m*i+b) for i in self.back_bins]
        return calibrated
    
    def counts_scaling(self,scale_factor):
        '''Used to scale the number of counts from foreground to 
        background
        '''
        self.back_counts=[i*scale_factor for i in self.back_counts]
    
    def calibration_saving(self,calib,name):
        save_location=os.path.join(os.getcwd(),'Calibrations')
        file_name=os.path.join(save_location,name+'.txt')
        f=open(file_name,'w')
        for i in calib:
            f.write('{}\n'.format(i))
        f.close()
        
        
#if __name__ =="__main__":   
#    b_loc8=os.path.join(loc8,'histogram_15-37-05.txt')
#    f_loc8=os.path.join(loc8,'histogram_16-44-29.txt')
#    #have to read in each text file, then create a new file to write just the 
#    #counts to
#    b=open(b_loc8,'r')
#    b_data=b.readlines()
#    b.close()
#    bo=open(os.path.join(loc8,'KNIFE_back.txt'),'w')
#    for i in range(len(b_data)):
#        bo.write('{}\n'.format(float(b_data[i].split(sep=',')[1])))
#    bo.close()
#    f=open(f_loc8,'r')
#    f_data=f.readlines()
#    f.close()
#    fo=open(os.path.join(loc8,'KNIFE_fore.txt'),'w')
#    for i in range(len(f_data)):
#        fo.write('{}\n'.format(float(f_data[i].split(sep=',')[1])))
#    fo.close()     #get 
#    
#    #spectral analysis for the KNIFE detector
#    b_loc8=os.path.join(loc8,'KNIFE_back.txt')
#    f_loc8=os.path.join(loc8,'KNIFE_fore.txt')
#    knife_90505=Spectra_Analysis(f_loc8,b_loc8,0,0)
#    fore_90505,back_90509=knife_90505.average_count_rate(25*60,15*60)
#    knife_90505.counts_scaling(1)
#    cali=knife_90505.KNIFE_calibration([642,220],[2.22325,7.64],m=0.00348,b=-0.011291)
##    back_cali=knife_90505.KNIFE_calibration([450],[1.436],
##                                            background_calibration=True)
##    knife_90505.calibrated_spectrum_plotter('905-05 in beam','KNIFE with 905-05 in beam',
##                                            cali,second_label='No target',
##                                            yscale='log',
##                                            energies=[10.829,6.322,5.269,1.885,
##                                                      5.53,4.51,3.68,
##                                                      4.95,1.26,3.68],
##                                            xtick_remove=[2])
##                                            back_calibration=back_cali)
#    
#    #put the knife and 2x4 on top of each other
#    fore_loc8=os.path.join(loc8,'2x4LaBr_Digitizer_90505.txt')    
##    f_loc8=os.path.join(loc8,'histogram_16-44-29.txt')
#    labr_knife=Spectra_Analysis(fore_loc8,f_loc8,0,0)
#    la_fore,la_back=labr_knife.average_count_rate(15*60,15*60)
#    labr_knife.calibrated_spectrum_plotter('2x4 w/KSU digitizer','905-05 in beam KNIFE and 2x4LaBr',
#                                           labr_with,second_label='KNIFE',
#                                           yscale='log',
#                                           back_calibration=cali,
#                                           zoomed=[0,14],
#                                           energies=[10.829,6.322,5.269,1.885,
#                                                      5.53,4.51,3.68,
#                                                      4.95,1.26,3.68,10.318,9.807],
#                                            xtick_remove=[2],
#                                            calibration_lines=[2.2232,7.645])
#