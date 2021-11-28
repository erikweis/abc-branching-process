import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt
import json

class ABCAnalysis:

    def __init__(self,foldername):

        self.dirpath = os.path.join('simulations',foldername)
        csv_path = os.path.join(self.dirpath,'trials.csv')
        self.df = pd.read_csv(csv_path)

        self.df['trial_success'] = self.df.apply(self.determine_trial_success,axis=1)

        #load params
        with open(os.path.join(self.dirpath,'hyperparams.json')) as f:
            for k,v in json.load(f).items():
                self.__setattr__(k,v)

        #hard code state for now
        self.state = 'vt'
        data_path = os.path.join('data',f'{self.state}_first_peak.csv')
        self.cumulative_cases_data = pd.read_csv(data_path).values

    def number_successful_trials(self):
        return sum(self.df['trial_success'])


    def determine_trial_success(self,row):

        trial_ID = int(row['Unnamed: 0'])
        path = os.path.join(self.dirpath,f'trial_{trial_ID}.csv')

        with open(path,'r') as f:
            text = f.read()
            if text.startswith('Failure'):
                print(text)
                return 0
            else:
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
        pass

    def plot_results(self):

        for index, row in self.df.iterrows():
            if row['trial_success']:

                path = os.path.join(self.dirpath,f'trial_{index}.csv')
                temp_df = pd.read_csv(path)
                vals = temp_df['cumulative_cases_simulated'].values
                plt.plot(vals,color='blue',alpha=0.1)

        plt.plot(self.cumulative_cases_data,color='red',linewidth = 2)
        plt.show()


if __name__ == "__main__":
    
    #specify a foldername
    #foldername = '11-28_16-13-31' #100 with wide prior tight confidence (0.5)
    #foldername = '11-28_15-39-40' #1000 with wide priors
    foldername = '11-28_17-58-26'

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername)

    #make pairplot
    #print(abca.number_successful_trials())
    #abca.plot_results()
    df = abca.df[abca.df['trial_success']==1]
    print(df.head())
    #abca.pairplot_R0_k()