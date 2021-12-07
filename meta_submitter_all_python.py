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

    script = f'/usr/bin/sbatch'
    script += f' --export=ALL,NUM_TRIALS={num_trials},STATE={state},ERROR={error},FOLDERNAME={foldername},SUBDIR={subdir},NONPARAMETRIC={non_parametric}'
    script += ' subscript.sbatch'
    subprocess.call([script],shell=True)

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',type = str, default='vt')
    parser.add_argument('--error',default=0.5,type=float,help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default=None,type = str, help='custom foldername')
    parser.add_argument('--non_parametric',default=False,type=bool,help='non parametric verison')


    args = parser.parse_args()
    
    if args.state == 'all':
        os.mkdir(os.path.join('simulations',args.foldername))
        for state in STATES:
            submit(args.num_trials,state.lower(),args.error,f"{args.foldername}_{state}",subdir=args.foldername,non_parametric=args.non_parametric)
    else:
        submit(args.num_trials,args.state,args.error,args.foldername,non_parametric=args.non_parametric)