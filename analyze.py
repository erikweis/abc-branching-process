import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt
import json
from scipy.stats import gaussian_kde
import numpy as np

class ABCAnalysis:

    def __init__(self,path,state='vt'):

        self.dirpath = os.path.join('simulations',path)
        self.df = pd.read_csv(os.path.join(self.dirpath,'trials.csv'))
        self.successful_trials_df = pd.read_csv(os.path.join(self.dirpath,'successful_trials.csv'))

        #load params
        with open(os.path.join(self.dirpath,'hyperparams.json')) as f:
            for k,v in json.load(f).items():
                self.__setattr__(k,v)

        self.state = state
        
        # load cumulative cases data
        data_path = os.path.join('data',f'{self.state}_first_peak.csv')
        self.cumulative_cases_data = pd.read_csv(data_path).values[:,1]


    def number_successful_trials(self):
        return len(self.successful_trials_df)


    def pairplot_R0_k(self):

        """Pairplot of R0 and k"""

        sns.pairplot(self.successful_trials_df,vars=['r0','k'],diag_kws=dict(bins=20))
        plt.show()


    def pairplot(self):

        sns.pairplot(self.successful_trials_df,vars=['r0','k','r'],diag_kws=dict(bins=20))
        plt.show()


    def jointplot_R0_k(self,successful_trials_only=True):

        sns.jointplot(data=self.successful_trials_df,x='r0',y='k')
        plt.show()


    def plot_priors(self):
        pass


    def plot_results(self):

        #plot error bounds
        c = np.array(self.cumulative_cases_data[:-1])
        lower_bound = c + c*0.5 
        upper_bound = c - c*0.5 
        plt.fill_between(np.arange(len(c)),lower_bound,upper_bound,alpha=0.2)

        #plot simulated results
        for index,row in self.successful_trials_df.iterrows():
            d = eval(row['cumulative_cases_simulated'])
            print(d)
            plt.plot(d,color='blue',alpha=0.1)

        plt.plot(c,color='red',linewidth = 2)
        plt.show()

    def get_MAP(self,param,test_range=(0,10)):
        
        kernel = gaussian_kde(self.successful_trials_df[param].values)
        x = np.linspace(*test_range,1000)
        index =  np.argmax(kernel(x))
        return x[index]


    def plot_data_and_error_bar(self):

        #plot error bounds
        c = np.array(self.cumulative_cases_data[:-1])
        lower_bound = c + c*self.error*2
        upper_bound = c - c*self.error*2
        plt.fill_between(np.arange(len(c)),lower_bound,upper_bound,alpha=0.2)

        #plot data
        plt.plot(c,color='red',linewidth = 2)
        plt.show()

if __name__ == "__main__":
    
    #specify a foldername
    foldername = 'state_sweep_pw/state_sweep_pw_AK'

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        foldername = max(folders,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername,state='ak')
    print(abca.number_successful_trials())

    #make pairplot
    abca.plot_results()
    #abca.plot_data_and_error_bar()
    abca.pairplot()
    abca.pairplot_R0_k()
    abca.jointplot_R0_k()
    #abca.plot_results()