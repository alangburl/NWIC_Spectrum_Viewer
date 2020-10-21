from MDA_FAR import FAR_MDM as detect

class Detection_Probability():
    def __init__(self,fore_file,back_file,analysis_times=[600,1200,1800]):
        super().__init__()
        #open and read the two files into memory
        fore_energy,fore_time=self.read_file(fore_file)
        back_energy,back_time=self.read_file(back_file)
        #sum the fore ground and back ground up
        fore_sums=self.time_sum(fore_time,analysis_times)
        back_sums=self.time_sum(back_time,analysis_times)
        #initialize the mdm class with each of the points
        points=[0]*len(analysis_times)
        for i in range(len(analysis_times)):
            points[i]=detect(fore_sums[i],back_sums[i])
        self.f_sums,self.b_sums,self.a_times=fore_sums,back_sums,analysis_times
        #save the accumulated times to create an animation showing the gaussians
        # f=open('sums.csv','w')
        # for i in range(len(fore_sums)):
        #     f.write('{},{},{}\n'.format(fore_sums[i],back_sums[i],analysis_times[i]))
        # f.close()
        #evaluate the different points to get the detection probabilities and 
        #store as an attribute of the class
        self.probs=[0]*len(analysis_times)
        for j in range(len(points)):
            self.probs[j]=points[j].detection_probability()
    def read_file(self,file_name):
        f=open(file_name,'r')
        data=f.readlines()
        f.close()
        
        time=[]
        energy=[]
        for i in range(1,len(data)):
            line=data[i].split(sep=',')
            energy.append(float(line[0]))
            time.append(float(line[1].split(sep='\n')[0]))
        return energy,time
    
    def time_sum(self,time, evaluation_points):
        bins=[0]*len(evaluation_points)
        
        for i in range(len(evaluation_points)):
            count=0
            j=0
            while time[j]<=evaluation_points[i] and j<=len(time)-2:
                count+=1
                j+=1
            bins[i]=j
        # print(bins)
        return bins