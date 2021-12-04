from datetime import datetime
import os
import json
import sys
import pandas as pd
import argparse
import subprocess
from tqdm import tqdm
import logging
from datetime import datetime

from priors import normal_priors
from discretebranchingprocess import simulate_branching_process, save_data

class WriteFiles:
    """Class to write the files for the trials and parameters.
    """

    def __init__(
            self,
            state='vt',
            foldername=None,
            error=1, 
            num_trials=100):

        self.error = error
        self.state = state
        self.foldername = foldername

        #get output directory
        if not foldername:
            dirname = datetime.now().strftime("%m-%d_%H-%M-%S") # if (foldername is None or len(foldername)==0) else foldername
        else:
            dirname = foldername
        self.dirpath = os.path.join('simulations', dirname)
        os.mkdir(self.dirpath)

        # save run params to a json file
        hyperparams = dict(state=state,error=error,num_trials=num_trials)
        json_fpath = os.path.join(self.dirpath, 'hyperparams.json')
        with open(json_fpath, 'w') as f:
            json.dump(hyperparams, f)

        logging.info('started making priors')

        #pull R0 and k for files
        r0List = []
        kList = []
        rList = []
        for i in range(num_trials):
            R0, k, r = normal_priors()
            r0List.append(R0)
            kList.append(k)
            rList.append(r)
        
        logging.info('finished making priors')

        #save csv
        paramDF = pd.DataFrame(list(zip(r0List, kList, rList)), columns = ['R0', 'k', 'recovery'])
        trials_fpath = os.path.join(self.dirpath,'trials.csv')
        paramDF.to_csv(trials_fpath)
        self.paramDF = paramDF
    
        logging.info("finished initialization of WriteFiles object.")


    def submit_all_jobs(self):
        
        print("in job submitter")
        for index, vals in enumerate(self.paramDF.to_numpy()):
            
            if index%10==0:
                logging.info(f"starting trial {index} at {datetime.now()}")
            try:
                r0,k,r = vals
                output = simulate_branching_process(r0,k,r,self.state,threshold = self.error)

                trial_fpath = os.path.join(self.dirpath, f'trial_{index}.csv')
                save_data(output,trial_fpath)
            except:
                logging.info(f"trial {index} failed")

        logging.info("finished all jobs")
        sys.exit()
        

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',default='vt')
    parser.add_argument('--error',default=0.5,type=float, help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default='',help='custom foldername')

    args = parser.parse_args()
    
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
    logging.info("starting trials")

    wf = WriteFiles(num_trials = args.num_trials,error=args.error,state=args.state,foldername = args.foldername)
    wf.submit_all_jobs()
    
        




