from datetime import datetime
import os
import json
import sys
import pandas as pd

from discretebranchingprocess import simulate_branching_process

class Simulation:

    """Class to automatically run simulations.
    """

    def __init__(
        self,
        state='vt',
        foldername = None,
        cutoff_time = 90,
        A_R0 = 1,
        B_R0 = 4,
        A_k = .1,
        B_k = .5,
        error = 1):

        self.A_R0 = A_R0
        self.B_R0 = B_R0
        self.A_k = A_k
        self.B_k = B_k
        self.error = error
        self.cutoff_time = cutoff_time
        self.cumulative_cases_data = pd.read_csv(f'data/{state}_first_peak.csv').values

        dirname = datetime.now().strftime("%m-%d_%H-%M-%S") if foldername is None else foldername
        self.dirpath = os.path.join('simulations',dirname)
        os.mkdir(self.dirpath)
        
        #save hyperparams
        hyperparams = {'A_R0':A_R0,'B_R0':B_R0,'A_k':A_k,'B_k':B_k}
        json_fpath = os.path.join(self.dirpath,'hyperparams.json')
        with open(json_fpath,'w') as f:
            json.dump(hyperparams,f)
        
        #create data file
        self.csv_fpath = os.path.join(self.dirpath,'trials.csv')
        with open(self.csv_fpath,'w') as f:
            f.write('R0|k|cases\n')

    def run(self,iterations=1000):
        
        self.num_rejected_samples = 0

        for i in range(iterations):
            sampR0, sampK, simulated_cases  = simulate_branching_process(
                self.cumulative_cases_data,
                self.cutoff_time,
                self.A_R0,
                self.B_R0,
                self.A_k,
                self.B_k
            )

            with open(self.csv_fpath,'a') as f:
                f.write(f"{sampR0}|{sampK}|{simulated_cases}\n")
                if not simulated_cases:
                    self.num_rejected_samples += 1

        print("number of rejected samples",self.num_rejected_samples)


if __name__=="__main__":

    s = Simulation(cumulative_cases_data,cutoff_time=cutoff_time)
    s.run(iterations=100)

