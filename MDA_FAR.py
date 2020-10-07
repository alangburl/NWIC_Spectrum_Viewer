import numpy as np
import matplotlib.pyplot as plt
class FAR_MDM():
    def __init__(self,fore_cts,back_cts,FAR=1):
        #first genrate a range of counts to consider
        self.counts=np.linspace(0,75,76)
        self.far=FAR
        pdf_fore,pdf_back=self.generate_pdf(fore_cts,back_cts)
        cdf_fore,cdf_back=self.generate_cdf(pdf_fore,pdf_back)
#        detection_probability=1-cdf_fore[self.find_CI(FAR,cdf_back)]
#        print(detection_probability)
        
    def generate_pdf(self,fore,back):
        bkg=[]
        fgd=[]
        for i in self.counts:
            fgd.append(fore**i*np.exp(-fore)/np.math.factorial(i))
            bkg.append(back**i*np.exp(-back)/np.math.factorial(i))
            
        self.generate_plot([self.counts,self.counts],[fgd,bkg],
                           ['Foreground','Background'],'','Counts',
                           'Probability')
        return fgd,bkg
    
    def generate_cdf(self,fore,back):
        fore1=[]
        back1=[]
        for i in range(len(self.counts)):
            fore1.append(np.trapz(fore[0:i]))
            back1.append(np.trapz(back[0:i]))
        ind=self.find_CI(self.far,back1)
        self.generate_plot([self.counts,self.counts],[fore1,back1],
                           ['Foreground','Background'],'','Counts',
                           'Probability',2,[self.counts[ind]])
        return fore1, back1
    
    def find_CI(self,far,back):
        far1=far/(8*3600) #number of acceptable false alarms in an 8 hours day
        ind=0 #find the first position where the value exceeds the CI
        for i in range(len(back)):
            if back[i]>=(1-far1):
                ind=i
                break
        return ind
        
    def generate_plot(self,xs,ys,labels,title,xlabel,ylabel,f_num=1,
                      vert_lines=None):
        plt.figure(f_num)
        for i in range(len(xs)):
            plt.plot(xs[i],ys[i],label=labels[i])
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.xlim(0,75)

        if vert_lines!=None:
            for j in vert_lines:
                plt.axvline(j,label='Threshold',color='r')        
        plt.legend()
        plt.show()
        
    def find_MDM(self,FNR,back,detection_threshold):
        '''Used to find the false negative rate from the average counts'''
        false_negative_thresh=back
        fore_mdm=back
        while false_negative_thresh<detection_threshold:
            mdmpdf,b=self.generate_pdf(fore_mdm,1) #generate the pdf
            mdmcdf,bk=self.generate_cdf(mdmpdf,b)
            
if __name__=="__main__":
    a=FAR_MDM(25,14)
    
        
        