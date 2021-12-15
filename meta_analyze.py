import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from analyze import ABCAnalysis
from scipy.stats import gaussian_kde
from tqdm import tqdm
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px


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
        
        fig, axes = plt.subplots(2,2,figsize=(8,8))
        
        for df,state in tqdm(zip(dfs,self.states)):
            try:
                r0_x = np.linspace(0.8,6,200)
                k_x = np.linspace(0,0.25,200)
                r_x = np.linspace(0,1,200)
                res_x = np.linspace(0,40)

                r0_y = gaussian_kde(df['r0']).pdf(r0_x)
                k_y = gaussian_kde(df['k']).pdf(k_x)
                r_y = gaussian_kde(df['r']).pdf(r_x)
                res_y = gaussian_kde(df['res']).pdf(res_x)

                color = 'red' if state.lower()=='vt' else 'steelblue'
                alpha = 1 if state.lower() =='vt' else 0.3

                axes[0][0].plot(r0_x,r0_y,color=color,alpha=alpha)
                axes[0][1].plot(k_x,k_y,color=color,alpha=alpha)
                axes[1][0].plot(r_x,r_y,color=color,alpha=alpha)
                axes[1][1].plot(res_x,res_y,color=color,alpha=alpha)
            except:
                continue
        
        axes[0][0].set_title('r0')
        axes[0][1].set_title('k')
        axes[1][0].set_title('recovery')
        axes[1][1].set_title('reservoir')

        fig.tight_layout()

        plt.show()

    def visualize_sample_counts(self):

        num_successful_trials = [abca.number_successful_trials() for abca in self.abcas]
        max_cumulative_cases = [max(abca.cumulative_cases_data) for abca in self.abcas]

        plt.scatter(max_cumulative_cases,num_successful_trials)

        for i, txt in enumerate(self.states):
            plt.annotate(txt, ( max_cumulative_cases[i],num_successful_trials[i]))

        plt.xscale('log')
        plt.xlabel('Max Cumulative Cases')
        plt.yscale('log')
        plt.ylabel('Number of Accepted Samples')
        plt.show()

        # for abca, state in zip(self.abcas, self.states):
        #     print(state,abca.number_successful_trials())

    def visualize_sample_counts_vs_len_time_series(self):

        num_successful_trials = [abca.number_successful_trials() for abca in self.abcas]
        len_cumulative_cases = [len(abca.cumulative_cases_data) for abca in self.abcas]

        plt.scatter(len_cumulative_cases,num_successful_trials)

        for i, txt in enumerate(self.states):
            plt.annotate(txt, ( len_cumulative_cases[i],num_successful_trials[i]))

        plt.xscale('log')
        plt.xlabel('Number of Days in First Wave')
        plt.yscale('log')
        plt.ylabel('Number of Accepted Samples')
        plt.show()

    def len_time_vs_max_cum_cases(self):

        max_cumulative_cases = [max(abca.cumulative_cases_data) for abca in self.abcas]
        len_cumulative_cases = [len(abca.cumulative_cases_data) for abca in self.abcas]

        plt.scatter(max_cumulative_cases,len_cumulative_cases)

        for i, txt in enumerate(self.states):
            plt.annotate(txt, ( max_cumulative_cases[i],len_cumulative_cases[i]))

        plt.xlabel('Max Number of Cumulative Cases')
        plt.ylabel('Number of Days in Time Series')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()


    def plot_map_of_MAPS(self,param):

        MAPS = []
        states = []
        for abca in self.abcas:
            try:
                MAPS.append(abca.get_MAP(param))
                states.append(abca.state.upper())
            except:
                continue

        fig = px.choropleth(locations=states, locationmode="USA-states", color=MAPS, color_continuous_scale='Viridis', scope="usa")
        fig.show()
        



if __name__ == "__main__":

    mabca = MetaABCAnalysis('select_sweep')

    # for abca in mabca.abcas:
    #     if abca.state.upper() in ['WI','OH','VT','NY','NC']:
    #         abca.plot_results()

    for abca in mabca.abcas:
        print(abca.state,abca.number_successful_trials())
        if abca.number_successful_trials():
            abca.pairplot()
            abca.plot_results()

    #mabca.plot_map_of_MAPS('r0')
    #mabca.len_time_vs_max_cum_cases()
    # mabca.visualize_sample_counts()
    # mabca.visualize_sample_counts_vs_len_time_series()
    # mabca.plot_posteriors()


        