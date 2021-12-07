from datetime import datetime
import os
import json
import sys
import pandas as pd
import argparse
from tqdm import tqdm
import logging
from datetime import datetime

from priors import non_parametric_priors, normal_priors
from discretebranchingprocess import simulate_branching_process

class SimulationRunner:
    """Class to write the files for the trials and parameters."""

    def __init__(
            self,
            state='vt',
            foldername=None,
            subdir = None,
            error=0.5,
            non_parametric=False,
            num_trials=100):

        self.error = error
        self.state = state
        self.foldername = foldername
        self.non_parametric = non_parametric

        #get output directory
        dirname = foldername if foldername else datetime.now().strftime("%m-%d_%H-%M-%S")
        if subdir:
            self.dirpath = os.path.join('simulations', subdir, dirname)
        else:
            self.dirpath = os.path.join('simulations',dirname)
        os.mkdir(self.dirpath)

        # save run params to a json file
        hyperparams = dict(state=state,error=error,num_trials=num_trials)
        json_fpath = os.path.join(self.dirpath, 'hyperparams.json')
        with open(json_fpath, 'w') as f:
            json.dump(hyperparams, f)

        #pull R0 and k for files
        if non_parametric:
            ps_list = [non_parametric_priors() for _ in range(num_trials)]
            paramDF = pd.DataFrame(ps_list,columns=[f'p_{i}' for i in range(len(ps_list[0]))])
            paramDF.to_csv(os.path.join(self.dirpath,'trials.csv'))
            self.paramDF = paramDF
        
        else:
            r0List = []
            kList = []
            rList = []
            for i in range(num_trials):
                R0, k, r = normal_priors()
                r0List.append(R0)
                kList.append(k)
                rList.append(r)

            #save csv
            paramDF = pd.DataFrame(list(zip(r0List, kList, rList)), columns = ['R0', 'k', 'recovery'])
            paramDF.to_csv(os.path.join(self.dirpath,'trials.csv'))
            self.paramDF = paramDF
        
        logging.info("finished initialization of WriteFiles object.")


    def run_all_simulations(self):

        trial_successes = []
        self.successful_trials_data = []

        for index, vals in enumerate(self.paramDF.to_numpy()):
            
            if index%100==0:
                logging.info(f"starting trial {index} at {datetime.now()}")

            if self.non_parametric:
                output = simulate_branching_process(ps=vals,state = self.state,threshold=self.error)
            else:
                r0,k,r = vals
                output = simulate_branching_process(r0=r0,k=k,r=r,state = self.state,threshold = self.error)

            if isinstance(output,str) and output.startswith('Failure'):
                trial_successes.append(0)
            else:
                trial_successes.append(1)
                if self.non_parametric:
                    results_dict = {f'p_{i}':vals[i] for i in range(10)}
                    results_dict.update({'trialID':index, 'cumulative_cases_simulated':output})       
                    self.successful_trials_data.append(results_dict) 
                else:
                    results_dict = {'trialID':index, 'cumulative_cases_simulated':output,'r0':r0,'k':k,'r':r}
                    self.successful_trials_data.append(results_dict)

        # add trial success to data
        self.paramDF['trial_success'] = trial_successes
        self.paramDF.to_csv(os.path.join(self.dirpath,'trials.csv'))

        # save successful trials to df
        df = pd.DataFrame(self.successful_trials_data)
        df.to_csv(os.path.join(self.dirpath,'successful_trials.csv'))

        logging.info("finished all jobs")
        sys.exit()
        
    def __exit__(self):

         # save successful trials to df
        df = pd.DataFrame(self.successful_trials_data)
        df.to_csv(os.path.join(self.dirpath,'successful_trials.csv'))



if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',default='vt')
    parser.add_argument('--error',default=0.5,type=float, help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default='',help='custom foldername')
    parser.add_argument('--subdir',default='',help='subdir to hold related trials')
    parser.add_argument('--non_parametric',default=False,type=bool,help='non parametric version')

    args = parser.parse_args()
    
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
    logging.info("starting trials")

    wf = SimulationRunner(
        num_trials = args.num_trials,
        error=args.error,
        state=args.state,
        foldername = args.foldername,
        subdir=args.subdir,
        non_parametric = args.non_parametric
    )
    wf.run_all_simulations()
    
        




