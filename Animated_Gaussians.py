import matplotlib.pyplot as plt
from matplotlib import animation
from MDA_FAR import FAR_MDM 

class Movie_Maker():
    def __init__(self,raw_data_file_name,gaussian_movie_name,
                 probability_movie_name):
        self.gaussian_name=gaussian_movie_name
        self.probs_name=probability_movie_name
        f=open(raw_data_file_name,'r')
        data=f.readlines()
        f.close()
        fore,back,times,props=[],[],[],[]
        for i in range(len(data)):
            line=data[i].split(sep=',')
            fore.append(int(line[0]))
            back.append(int(line[1]))
            times.append(float(line[2]))
            props.append(float(line[3].split(sep='\n')[0]))
        self.data=[fore,back,times,props]
        
    def save_gaussian(self):
        Gaussian_Movies(self.gaussian_name, self.data)
        
    def save_probability(self):
        Probability_Movies(self.probs_name, self.data)
    
class Gaussian_Movies():
    def __init__(self,movie_name,data):
        self.gaussian_name=movie_name
        self.fore,self.back,self.times=data[0],data[1],data[2]
        self.gaussian()
        
    def gaussian(self):
        fig = plt.figure(1)
        ax1 = plt.axes(xlim=(0, 600), ylim=(0,.15))
        line, = ax1.plot([], [], lw=2)
        plt.xlabel('Counts')
        plt.ylabel('Probability')
        
        def init():
            plotlays, plotcols = [2], ["black","red"]
            self.lines = []
            self.annotation=ax1.annotate('Mean foreground counts:',xy=(100,0.05))
            self.annotation1=ax1.annotate('Mean background counts:',xy=(100,0.05))
            self.annotation2=ax1.annotate('Time:',xy=(350,0.12))

            for index in range(2):
                lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
                self.lines.append(lobj)
            
            for line in self.lines:
                line.set_data([],[])
                
            return self.lines,self.annotation,self.annotation1,self.annotation2
        
        def animate(i):
            a=FAR_MDM(self.fore[i],self.back[i])    
            self.annotation.set_position((self.fore[i]+.1*self.fore[i],max(a.pdf_fore)))
            self.annotation1.set_position((self.back[i]+.1*self.back[i],max(a.pdf_back)))
            self.annotation.set_text('Mean forground counts: {}'.format(self.fore[i]))
            self.annotation1.set_text('Mean background counts: {}'.format(self.back[i]))
            self.annotation2.set_text('Time: {:.2f}s'.format(self.times[i]))
            
            x1=a.counts
            y1=a.pdf_fore
            x2=a.counts
            y2=a.pdf_back
            xlist = [x1, x2]
            ylist = [y1, y2]
        
            #for index in range(0,1):
            for lnum,line in enumerate(self.lines):
                line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 
        
            return self.lines,self.annotation,self.annotation1,self.annotation1
        fig.tight_layout()
        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=180, interval=50, 
                                       blit=False,repeat=False)
        
        ffwriter=animation.FFMpegFileWriter()
        anim.save(self.gaussian_name,writer=ffwriter)
        
        
class Probability_Movies():
    def __init__(self,movie_name,data):
        self.probability_name=movie_name
        self.times,self.prob=data[2],data[3]
        self.probs()
        
    def probs(self):
        fig = plt.figure(2)
        ax1 = plt.axes(xlim=(0, max(self.times)+0.05*max(self.times)), ylim=(0,105))
        line, = ax1.plot([], [], lw=2,marker='*',linestyle='None')
        plt.xlabel('Time (s)')
        plt.ylabel('Detection Probability (%)')
        x,y=[],[]
        
        def init1():
            self.annotation1=ax1.annotate('Detection Probability:',
                                          xy=(max(self.times)*.63,15))
            self.annotation2=ax1.annotate('Time:',xy=(max(self.times)*.63,10))
            line.set_data([],[])
                
            return line,self.annotation1,self.annotation2
        
        def animate1(i):
            self.annotation1.set_text('Detection Probability: {:.2f}%'.format(self.prob[i]))
            self.annotation2.set_text('Time: {:.2f}s'.format(self.times[i]))
            x.append(self.times[i])
            y.append(self.prob[i])
            line.set_data(x,y)
            return line,self.annotation1,self.annotation1
        
        fig.tight_layout()
        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim1 = animation.FuncAnimation(fig, animate1, init_func=init1,
                                       frames=180, interval=50, 
                                       blit=True,repeat=False)
        
        ffwriter=animation.FFMpegFileWriter()
        anim1.save(self.probability_name,writer=ffwriter)
        # plt.show()
