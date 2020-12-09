class Rebins():
    def __init__(self,counts, rebin):
        self.counts, self.rebin=counts,rebin
        
    def rebinner(self):
        new_bins=[]
        for i in range(0,len(self.counts),self.rebin):
            new=0
            try:
                for j in range(self.rebin):
                    new+=self.counts[i+j]
            except:
                new+=0
            new_bins.append(new)
        return new_bins