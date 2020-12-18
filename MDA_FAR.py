import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import CDF

class FAR_MDM():
    def __init__(self,fore_cts,back_cts,FAR=1):
        # first genrate a range of counts to consider
        self.counts=np.linspace(0,6*fore_cts,6*fore_cts+1)
        self.far=FAR
        pdf_fore,pdf_back=self.generate_pdf(fore_cts,back_cts)
        cdf_fore,cdf_back=self.generate_cdf(pdf_fore,pdf_back)
        # self.detection_probability(FAR,cdf_back, cdf_fore)
        self.FAR=FAR
        self.cdf_back=cdf_back
        self.cdf_fore=cdf_fore
        self.pdf_fore,self.pdf_back=pdf_fore,pdf_back
        
    def generate_pdf(self,fore,back):
        bkg=[]
        fgd=[]
        for i in self.counts:
            if fore<=20:
                fgd.append(fore**i*np.exp(-fore)/np.math.factorial(i))
                bkg.append(back**i*np.exp(-back)/np.math.factorial(i))
        if fore>20:
            fgd=self.gaussian_distribution(fore, np.sqrt(fore))
            bkg=self.gaussian_distribution(back, np.sqrt(back))
        # label_p=['Mean Foreground: {}'.format(fore),[fore+.1*fore,max(fgd)],
        #          'Mean Background: {}'.format(back),[back+.1*back,max(bkg)]]
        # self.generate_plot([self.counts,self.counts],[fgd,bkg],
        #                     ['Foreground','Background'],'','Counts',
        #                     'Probability',label_points=label_p)
        return fgd,bkg
    
    def generate_cdf(self,fore,back):
        fore1=[]
        back1=[]
        fore=np.asarray(fore)
        back=np.asarray(back)
        counts=np.asarray(self.counts)
        fore1=CDF.CDF_Generator(fore,counts)
        back1=CDF.CDF_Generator(back,counts)
        # for i in range(len(self.counts)):
        #     fore1.append(np.trapz(fore[0:i]))
        #     back1.append(np.trapz(back[0:i]))
            
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
                      vert_lines=None,label_points=None):
        plt.figure(f_num)
        for i in range(len(xs)):
            plt.plot(xs[i],ys[i],label=labels[i])
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)

        if vert_lines!=None:
            for j in vert_lines:
                plt.axvline(j,label='Threshold',color='r')
        if label_points!=None:
            #foreground
            plt.annotate(label_points[0],label_points[1])
            plt.annotate(label_points[2],label_points[3])
        plt.legend()
        plt.show()
        
    def gaussian_distribution(self,mu,sigma):
        '''Generatee a Probability density function
        '''
        # array=np.linspace(mu-6*sigma,mu+6*sigma,1000)
        pdf=[1/np.sqrt(2*np.pi*sigma**2)*np.exp(-(i-mu)**2/(2*sigma**2)) \
             for i in self.counts]
        # self.generate_plot([array], [pdf], [''], 'title', 'xlabel', 'ylabel')
        return pdf
    
    def detection_probability(self):
        detection_probability=1-self.cdf_fore[self.find_CI(self.FAR,self.cdf_back)]
        return detection_probability
        
if __name__=="__main__":
    # a=FAR_MDM(75,37)
    # print(a.detection_probability())
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [])
    def init():
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, .1)
        return ln,

    def update(frame):
        a=FAR_MDM(frame,frame/3)
        xdata=a.counts
        ydata=a.pdf_fore
        ln.set_data(xdata, ydata)
        return ln,
    
    ani = FuncAnimation(fig, update, frames=100,
                    init_func=init, blit=True)
    plt.show()
    
        
        