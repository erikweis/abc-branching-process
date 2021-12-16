import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from analyze import ABCAnalysis

def get_df():

    vt_ = ABCAnalysis('custom_vt',state='vt')
    vt = vt_.successful_trials_df
    vt = vt[vt['strict']==True]
    vt = vt[['r0','k','r','res']]
    #vt.assign(state = ['Vermont' for _ in range(len(vt))])
    vt['state'] = ['Vermont' for _ in range(len(vt))]
    # vt = vt[['trialID', 'cumulative_cases_simulated', 'r0', 'k', 'r',
    #    'res', 'strict', 'state']]

    wi = pd.read_csv('simulations/custom_wi3/successful_trials.csv',index_col=0)
    wi = wi[['r0','k','r','res']]
    wi['state'] = np.array(['Wisconsin' for _ in range(len(wi))])


    df = pd.concat([vt,wi])

    return df

def pairplot(df,save=False):

    df = df.reset_index()

    g = sns.pairplot(
        df,
        vars=['r0','k','r','res'],
        plot_kws={'alpha': 0.25},
        hue='state'
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
        plt.savefig(f'figures/joint_pairplot.png')
    plt.show()
    
if __name__=="__main__":

    df = get_df()
    pairplot(df,save=True)