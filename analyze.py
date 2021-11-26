import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt

class ABCAnalysis:

    def __init__(self,foldername):

        self.dirpath = os.path.join('simulations',foldername)
        csv_path = os.path.join(self.dirpath,'trials.csv')
        self.df = pd.read_csv(csv_path,sep='|')

        print(self.df.head(10))


    def pairplot_R0_k(self):

        """Pairplot of R0 and k"""

        sns.pairplot(self.df,vars=['R0','k'])
        plt.show()


    ### other functions for analyzing the data, making plots,etc. #####################


if __name__ == "__main__":
    
    #specify a foldername
    foldername = ''

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername)

    #make pairplot
    abca.pairplot_R0_k()