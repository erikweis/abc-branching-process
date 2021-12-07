import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from analyze import ABCAnalysis
from scipy.stats import gaussian_kde
from tqdm import tqdm
import pandas as pd
import plotly.figure_factory as ff


from meta_submitter_all_python import STATES

class MetaABCAnalysis:

    def __init__(self,subdir):

        folders = [f for f in os.listdir(os.path.join('simulations',subdir))]
        states = [f.split('_')[-1] for f in folders]

        self.abcas = []
        for f,s in tqdm(zip(folders,states)):
            try:
                self.abcas.append(ABCAnalysis(os.path.join(subdir,f),state=s))
            except Exception as e:
                print(e)
        
        self.states = [abca.state for abca in self.abcas]
        #self.abcas = [ABCAnalysis(f,state=s) for f,s in zip(folders,states)]

    
    def plot_posteriors(self):

        dfs = [abca.successful_trials_df for abca in self.abcas]
        
        fig, axes = plt.subplots(1,2,figsize=(10,4))
        
        for df,state in tqdm(zip(dfs,self.states)):

            r0_x = np.linspace(0,6.5,200)
            k_x = np.linspace(0,1.1,200)
            r_x = np.linspace(0,1,200)

            r0_y = gaussian_kde(df['r0']).pdf(r0_x)
            k_y = gaussian_kde(df['k']).pdf(k_x)
            #r_y = gaussian_kde(df['r']).pdf(r_x)

            color = 'red' if state.lower()=='vt' else 'steelblue'
            alpha = 1 if state.lower() =='vt' else 0.3

            axes[0].plot(r0_x,r0_y,color=color,alpha=alpha)
            axes[1].plot(k_x,k_y,color=color,alpha=alpha)
            #axes[2].plot(r_x,r_y,color=color,alpha=alpha)
        
        axes[0].set_title('r0')
        axes[1].set_title('k')
        #axes[2].set_title('recovery')

        fig.tight_layout()

        # for nshape,seg in enumerate(m.states):
        #     # skip DC and Puerto Rico.
        #     if statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
        #     # Offset Alaska and Hawaii to the lower-left corner. 
        #         if statenames[nshape] == 'Alaska':
        #         # Alaska is too big. Scale it down to 35% first, then transate it. 
        #             seg = list(map(lambda (x,y): (0.35*x + 1100000, 0.35*y-1300000), seg))
        #         if statenames[nshape] == 'Hawaii':
        #             seg = list(map(lambda (x,y): (x + 5100000, y-900000), seg))

        #         color = rgb2hex(colors[statenames[nshape]]) 
        #         poly = Polygon(seg,facecolor=color,edgecolor=color)
        #         ax.add_patch(poly)

        plt.show()

    def visualize_sample_counts(self):

        num_successful_trials = [abca.number_successful_trials() for abca in self.abcas]
        max_cumulative_cases = [max(abca.cumulative_cases_data) for abca in self.abcas]

        plt.scatter(max_cumulative_cases,num_successful_trials)

        for i, txt in enumerate(self.states):
            plt.annotate(txt, ( max_cumulative_cases[i],num_successful_trials[i]))

        #plt.xscale('log')
        plt.xlabel('Max Cumulative Cases')
        #plt.yscale('log')
        plt.ylabel('Number of Accepted Samples')
        plt.show()

        # for abca, state in zip(self.abcas, self.states):
        #     print(state,abca.number_successful_trials())


    def plot_map_of_MAPS(self,param):

        self.MAPS = [abca.get_MAP(param) for abca in self.abcas]
        print(self.MAPS)



if __name__ == "__main__":

    mabca = MetaABCAnalysis('state_sweep_3')
    mabca.plot_map_of_MAPS('r0')
    mabca.visualize_sample_counts()
    mabca.plot_posteriors()


        