import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt

class ABCAnalysis:

    def __init__(self,foldername):

        self.dirpath = os.path.join('simulations',foldername)
        csv_path = os.path.join(self.dirpath,'trials.csv')
        self.df = pd.read_csv(csv_path)

        self.df['trial_success'] = self.df.apply(self.determine_trial_success,axis=1)

    def number_successful_trials(self):
        return sum(self.df['trial_success'])


    def determine_trial_success(self,row):

        trial_ID = int(row['Unnamed: 0'])

        path = os.path.join(self.dirpath,f'trial_{trial_ID}.csv')

        with open(path,'r') as f:
            if f.read().startswith('Failure'):
                return 0
            return 1


    def pairplot_R0_k(self,successful_trials_only = True):

        """Pairplot of R0 and k"""

        if successful_trials_only:
            df = self.df[self.df['trial_success']==1]
        else:
            df = self.df
        sns.pairplot(df,vars=['R0','k'])
        plt.show()


    def plot_priors(self):

        x = 

if __name__ == "__main__":
    
    #specify a foldername
    foldername = '11-28_11-44-20'

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername)

    #make pairplot
    abca.pairplot_R0_k()