import argparse
import subprocess
import os

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def submit(num_trials,state,error,foldername,subdir=''):

    script = f'/usr/bin/sbatch'
    script += f' --export=ALL,NUM_TRIALS={num_trials},STATE={state},ERROR={error},FOLDERNAME={foldername},SUBDIR={subdir}'
    script += ' subscript.sbatch'
    subprocess.call([script],shell=True)

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',type = str, default='vt')
    parser.add_argument('--error',default=0.5,type=float,help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default=None,type = str, help='custom foldername')

    args = parser.parse_args()
    
    if args.state == 'all':
        for state in STATES:
            os.mkdir(os.path.join('simulations',args.foldername))
            submit(args.num_trials,state.lower(),args.error,f"{args.foldername}_{state}",subdir=args.foldername)
    else:
        submit(args.num_trials,args.state,args.error,args.foldername)