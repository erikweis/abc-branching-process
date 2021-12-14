import argparse
import subprocess
import os

from priors import non_parametric_priors

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def submit(num_trials,state,error,foldername,subdir='',non_parametric=False):


    foldername_string = f"--foldername {foldername}" if foldername else ''
    subdir_string = f"--subdir {subdir}" if subdir else ''
    nonparametric_string = f"--non_parametric" if non_parametric else ''
    
    subscript = \
        f"""#!/bin/sh

        #SBATCH --nodes=1
        #SBATCH --mem=2gb
        #SBATCH --time=8:00:00
        #SBATCH --job-name=1997

        python run_simulations.py --num_trials $NUM_TRIALS --state $STATE --error $ERROR {foldername_string} {subdir_string} {nonparametric_string} """
    
    with open('subscript.sbatch','w') as f:
        f.write(subscript)

    script = f'/usr/bin/sbatch'
    script += f' --export=ALL,NUM_TRIALS={num_trials},STATE={state},ERROR={error},FOLDERNAME={foldername},SUBDIR={subdir},NONPARAMETRIC={non_parametric}'
    script += ' subscript.sbatch'
    subprocess.call([script],shell=True)

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',type = str, default='vt')
    parser.add_argument('--error',default=0.5,type=float,help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default='',type = str, help='custom foldername')
    parser.add_argument('--non_parametric',action='store_true',help='non parametric verison')

    args = parser.parse_args()
    
    if args.state == 'all':
        os.mkdir(os.path.join('simulations',args.foldername))
        for state in STATES:
            submit(args.num_trials,state.lower(),args.error,f"{args.foldername}_{state}",subdir=args.foldername,non_parametric=args.non_parametric)
    elif args.state == 'select':
        os.mkdir(os.path.join('simulations',args.foldername))
        for state in ['WI','OH','VT','NY','NC']:
            submit(args.num_trials,state.lower(),args.error,f"{args.foldername}_{state}",subdir=args.foldername,non_parametric=args.non_parametric)
    else:
        submit(args.num_trials,args.state,args.error,args.foldername,non_parametric=args.non_parametric)