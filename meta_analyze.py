import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from analyze import ABCAnalysis
from scipy.stats import gaussian_kde
from tqdm import tqdm

from meta_submitter_all_python import STATES

class MetaABCAnalysis:

    def __init__(self,folder_tag):

        folders = [f for f in os.listdir('simulations/') if f.startswith(folder_tag)]
        states = [f.split('_')[-1] for f in folders]

        self.abcas = []
        for f,s in tqdm(zip(folders,states)):
            try:
                self.abcas.append(ABCAnalysis(f,state=s))
            except:
                continue
        # self.abcas = [ABCAnalysis(f,state=s) for f,s in zip(folders,states)]

    
    def plot_posteriors(self):

        dfs = [abca.successful_trials_df for abca in self.abcas]
        
        fig, axes = plt.subplots(2,2)
        
        for df in tqdm(dfs):

            r0_x = np.linspace(1,5,200)
            k_x = np.linspace(0,5,200)
            r_x = np.linspace(0,1,200)

            r0_y = gaussian_kde(df['R0']).pdf(r0_x)
            k_y = gaussian_kde(df['k']).pdf(k_x)
            r_y = gaussian_kde(df['recovery']).pdf(r_x)

            axes[0][0].plot(r0_x,r0_y,color='steelblue',alpha=0.3)
            axes[0][1].plot(k_x,k_y,color='steelblue',alpha=0.3)
            axes[1][0].plot(r_x,r_y,color='steelblue',alpha=0.3)
        
        axes[0][0].set_title('r0')
        axes[0][1].set_title('k')
        axes[1][0].set_title('recovery')

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


if __name__ == "__main__":

    mabca = MetaABCAnalysis('state_sweep')
    mabca.plot_posteriors()
        