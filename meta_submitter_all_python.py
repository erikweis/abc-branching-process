import argparse
import subprocess

def submit(self,args):

    script = f"""#!/bin/bash
            #SBATCH --partition=short
            #SBATCH --nodes=1
            #SBATCH --mem=2gb
            #SBATCH --time=0:20:00
            #SBATCH --job-name=1997
            python submitter_all_python.py --num_trials {args.num_trials} --state {args.state} --error {args.error} --foldername {args.foldername}"""
    subprocess.call([script],shell=True)


if __name__=='__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',default='vt')
    parser.add_argument('--error',default=0.5,help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default=None,help='custom foldername')

    args = parser.parse_args()
    submit(args)

    