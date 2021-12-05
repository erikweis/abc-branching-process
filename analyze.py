import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt
import json

class ABCAnalysis:

    def __init__(self,foldername,state='vt'):

        self.dirpath = os.path.join('simulations',foldername)
        csv_path = os.path.join(self.dirpath,'trials.csv')
        self.df = pd.read_csv(csv_path)

        #load params
        with open(os.path.join(self.dirpath,'hyperparams.json')) as f:
            for k,v in json.load(f).items():
                self.__setattr__(k,v)

        #hard code state for now
        self.state = state
        data_path = os.path.join('data',f'{self.state}_first_peak.csv')
        self.cumulative_cases_data = pd.read_csv(data_path).values[:,1]

    def number_successful_trials(self):
        return len(self.successful_trials_df)


    def determine_trial_success(self,row):

        trial_ID = int(row['Unnamed: 0'])
        path = os.path.join(self.dirpath,f'trial_{trial_ID}.csv'    )

        try:
            with open(path,'r') as f:
                text = f.read()
                if text.startswith('Failure'):
                    return 0
                else:
                    return 1
        except:
            return 0

    def plot_distribution_failures(self):
        pass

    def pairplot_R0_k(self,successful_trials_only = True):

        """Pairplot of R0 and k"""

        df = self.successful_trials_df if successful_trials_only else self.df

        sns.pairplot(df,vars=['R0','k'],diag_kws=dict(bins=20))
        plt.show()

    def pairplot(self,successful_trials_only = True):

        df = self.successful_trials_df if successful_trials_only else self.df

        sns.pairplot(df,vars=['R0','k','recovery'],diag_kws=dict(bins=20))
        plt.show()
        

    def jointplot_R0_k(self,successful_trials_only=True):

        df = self.successful_trials_df if successful_trials_only else self.df

        sns.jointplot(data=df,x='R0',y='k')
        plt.show()

    def plot_priors(self):
        pass

    def plot_results(self):

        for index,row in self.successful_trials_df.iterrows():

            trial_id = int(row['Unnamed: 0'])

            try:
                path = os.path.join(self.dirpath,f'trial_{trial_id}.csv')
                temp_df = pd.read_csv(path)
                vals = temp_df['cumulative_cases_simulated'].values
                plt.plot(vals,color='blue',alpha=0.1)

            except:
                continue

        print(self.cumulative_cases_data)
        plt.plot(self.cumulative_cases_data,color='red',linewidth = 2)
        plt.show()

    @property
    def successful_trials_df(self):
        
        if not hasattr(self,'_successful_trials_df'):
            fpath = os.path.join(self.dirpath,'successful_trials.csv')
            if os.path.isfile(fpath):
                self._successful_trials_df = pd.read_csv(fpath)
            else:
                self.df['trial_success'] = self.df.apply(self.determine_trial_success,axis=1)
                self._successful_trials_df = self.df[self.df['trial_success']==1]
                self._successful_trials_df.to_csv(fpath)
        return self._successful_trials_df


if __name__ == "__main__":
    
    #specify a foldername
    foldername = 'None'

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername)
    print(abca.number_successful_trials())

    #make pairplot
    #print(abca.number_successful_trials())
    abca.plot_results()
    abca.pairplot_R0_k()
    #abca.jointplot_R0_k()
    #abca.plot_results()