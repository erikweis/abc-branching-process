import pandas as pd
from datetime import datetime
import os
import seaborn as sns
import matplotlib
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import json
from scipy.stats import gaussian_kde
import numpy as np

class ABCAnalysis:

    def __init__(self,path,state='vt',sv = 15):

        self.dirpath = os.path.join('simulations',path)
        self.df = pd.read_csv(os.path.join(self.dirpath,'trials.csv'),index_col=0)

        #load params
        with open(os.path.join(self.dirpath,'hyperparams.json')) as f:
            for k,v in json.load(f).items():
                self.__setattr__(k,v)

        self.state = state
        self.sv = sv
 
        # load cumulative cases data
        data_path = os.path.join('data',f'{self.state}_first_peak.csv')
        self.cumulative_cases_data = pd.read_csv(data_path).values[:,1]

        #successful trials df
        self.successful_trials_df = pd.read_csv(os.path.join(self.dirpath,'successful_trials.csv'))

        def func(x):
            return self.strict_check(eval(x['cumulative_cases_simulated']))
        self.successful_trials_df['strict'] = self.successful_trials_df.apply(func, axis=1)
        


    def number_successful_trials(self,strict=False):
        if strict:
            return sum(self.successful_trials_df['strict'].values)
        return len(self.successful_trials_df)


    def pairplot_R0_k(self):

        """Pairplot of R0 and k"""

        sns.pairplot(self.successful_trials_df,vars=['r0','k'],diag_kws=dict(bins=20))
        plt.show()


    def pairplot(self,save=False,strict=False):

        df = self.successful_trials_df
        if strict:
            df = df[df['strict']==True]

        g = sns.pairplot(
            df,
            vars=['r0','k','r','res'],
            plot_kws={'alpha': 0.25}
        ) #,diag_kws=dict(bins=20))

        replacements = {
            'r0':'$R_0$',
            'k':'$k$',
            'r':'$r$',
            'res':'$I_{res}$'
        }

        for i in range(4):
            for j in range(4):
                xlabel = g.axes[i][j].get_xlabel()
                ylabel = g.axes[i][j].get_ylabel()
                if xlabel in replacements.keys():
                    g.axes[i][j].set_xlabel(replacements[xlabel])
                if ylabel in replacements.keys():
                    g.axes[i][j].set_ylabel(replacements[ylabel])

        if save:
            plt.savefig(f'figures/{self.state}_pairplot.png')
        plt.title(self.state)
        plt.show()

    def jointplot_R0_k(self,successful_trials_only=True):

        sns.jointplot(data=self.successful_trials_df,x='r0',y='k')
        plt.show()


    def plot_priors(self):
        pass

    
    def get_bounds(self):

        c = np.array(self.cumulative_cases_data[:-1])
        return c - c*self.error, c + c*self.error

    def strict_check(self,cumulative_cases_simulated):

        lower_bound, upper_bound = self.get_bounds()

        add = True
        for v in np.arange(self.sv,len(cumulative_cases_simulated)-1):
            if not lower_bound[v] < cumulative_cases_simulated[v] < upper_bound[v]:
                add = False
                break

        return add

    def plot_results(self,save=False,strict=False):

        #plot error bounds
        c = np.array(self.cumulative_cases_data[:-1])
        lower_bound, upper_bound = self.get_bounds()
        plt.fill_between(np.arange(len(c)),lower_bound,upper_bound,alpha=0.2)

        #plot simulated results
        for index,row in self.successful_trials_df.iterrows():

            d = eval(row['cumulative_cases_simulated'])
            
            if strict:
                if self.strict_check(d):
                    plt.plot(d,color='blue',alpha=0.1)
            else:
                plt.plot(d,color='blue',alpha=0.1)

        plt.plot(c,color='red',linewidth = 2)
        plt.xlabel('Days Since Start of First Wave')
        plt.ylabel('Cumulative Case Count')
        if save:
            plt.savefig(f'figures/{self.state}_results.png')
        plt.title(self.state)
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
    foldername = 'custom_wi3'

    #if no foldername specified, use the most recent dated folder
    if not foldername:
        folders = [f for f in os.listdir('simulations/') if not f.startswith('.')]
        
        dts = []
        for f in folders:
            try:
                dts.append(datetime.strptime(f,"%m-%d_%H-%M-%S"))
            except:
                continue
        foldername = datetime.strftime(max(dts),"%m-%d_%H-%M-%S")  #max(dts,key=lambda f: datetime.strptime(f,"%m-%d_%H-%M-%S"))
        print("Analyzing folder {}".format(foldername))

    #create analysis object with foldername
    abca = ABCAnalysis(foldername,sv=15,state='wi')
    print(abca.number_successful_trials(strict=False))

    #make pairplot
    abca.plot_results(save=True,strict=False)
    #abca.plot_data_and_error_bar()
    abca.pairplot(save=True,strict=False)
    #abca.pairplot_R0_k()
    #abca.jointplot_R0_k()
    #abca.plot_results()