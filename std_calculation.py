'''Steps to determine the net count rate uncertainty:
    1.) Calculate foreground and background rate uncertainties in the ROI
    2.) RSS the two 
'''
class net_std():
    def __init__(self,foreground_count_rate,background_count_rate):
        self.fore_cr=foreground_count_rate
        self.back_cr=background_count_rate
    def calculate_uncertainties(self):
        net_un=(self.fore_cr+self.back_cr)**0.5
        return net_un
        
        