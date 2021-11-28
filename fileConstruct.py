from datetime import datetime
import os
import json
import sys
import pandas as pd
import argparse 

from priors import priors

class WriteFiles:
    """Class to write the files for the trials and parameters.
    """

    def __init__(
            self,
            state='vt',
            foldername=None,
            cutoff_time=90,
            A_R0=1,
            B_R0=4,
            A_k=.1,
            B_k=.5,
            error=1, 
            num_trials=100):
        self.A_R0 = A_R0
        self.B_R0 = B_R0
        self.A_k = A_k
        self.B_k = B_k
        self.error = error
        self.cutoff_time = cutoff_time
        #self.cumulative_cases_data = pd.read_csv(f'data/{state}_first_peak.csv').values



        dirname = datetime.now().strftime("%m-%d_%H-%M-%S") if foldername is None else foldername
        self.dirpath = os.path.join('simulations', dirname)
        os.mkdir(self.dirpath)

        # save hyperparams to a json file
        hyperparams = {'A_R0': A_R0, 'B_R0': B_R0, 'A_k': A_k, 'B_k': B_k}
        json_fpath = os.path.join(self.dirpath, 'hyperparams.json')
        with open(json_fpath, 'w') as f:
            json.dump(hyperparams, f)

        #pull R0 and k for files

        
        r0List = []
        kList = []
        rList = []
        for i in range(num_trials):
            R0, k, r = priors(A_R0, B_R0, A_k, B_k)
            r0List.append(R0)
            kList.append(k)
            rList.append(r)
            
            
        paramDF = pd.DataFrame(list(zip(r0List, kList, rList)), columns = ['R0', 'k', 'recovery'])
        
        
        paramDF.to_csv('trials.csv')
        trial_fpath = os.path.join(self.dirpath, 'trial.csv')
        
        
        
if __name__=='__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , help = 'number of simulation runs')
    

    args = parser.parse_args()
    
    num_trials = args.num_trials
    WriteFiles(num_trials = num_trials)
    
        




