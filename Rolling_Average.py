class Rolling_Average():
    def __init__(self,desired_average,probs,times):
        '''Used to calculate the rolling average of the probabilities'''
        self.probs,self.desired,self.times=probs,desired_average,times
        
    def rolling(self):
        current_average=0
        