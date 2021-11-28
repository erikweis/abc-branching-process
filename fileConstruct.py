from datetime import datetime
import os
import json
import sys
import pandas as pd
import argparse
import subprocess

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
            B_R0=10,
            A_k=.1,
            B_k=1,
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
            
        #save csv
        paramDF = pd.DataFrame(list(zip(r0List, kList, rList)), columns = ['R0', 'k', 'recovery'])
        trials_fpath = os.path.join(self.dirpath,'trials.csv')
        paramDF.to_csv(trials_fpath)
        self.paramDF = paramDF
    

    def get_bash_script(self,fpath,r0,k,r):

        return f"""#!/bin/bash
            #SBATCH --partition=short
            #SBATCH --nodes=1
            #SBATCH --mem=1gb
            #SBATCH --time=00:09:59
            #SBATCH --job-name=1997
            python discretebranchingprocess.py -f {fpath} -r0 {r0} -k {k} -r {r}"""

        
    def submit_all_jobs(self):
        
        for index, vals in enumerate(self.paramDF.to_numpy()):

            r0,k,r = vals
            trial_fpath = os.path.join(self.dirpath, f'trial_{index}.csv')

            script = self.get_bash_script(trial_fpath,r0,k,r)
            subprocess.call([script],shell=True)
        

if __name__=='__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , help = 'number of simulation runs')
    

    args = parser.parse_args()
    
    num_trials = args.num_trials
    wf = WriteFiles(num_trials = num_trials)
    wf.submit_all_jobs()
    
        




