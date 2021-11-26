import pandas as pd
from datetime import datetime
import os

class ABCAnalysis:

    def __init__(self,foldername):

        self.dirpath = os.path.join('simulations',foldername)
        csv_path = os.path.join(self.dirpath,'trials.csv')
        self.df = pd.read_csv(csv_path,sep='|')

        print(self.df.head(10))

if __name__ == "__main__":
    
    foldername = ''

    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    sa = ABCAnalysis(foldername)