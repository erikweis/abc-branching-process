import argparse
import subprocess

def submit(args):

    

    script = f'/usr/bin/sbatch'
    script += f'--export=ALL,NUM_TRIALS={args.num_trials},STATE={args.state},ERROR={args.error},FOLDERNAME={args.foldername}'
    script += 'subscript.sbatch'
    subprocess.call([script],shell=True)


if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_trials', type = int , default = 100, help = 'number of simulation runs')
    parser.add_argument('--state',default='vt')
    parser.add_argument('--error',default=0.5,type=float,help='the maximum error for simulation when checking against real data')
    parser.add_argument('--foldername',default=None,help='custom foldername')

    args = parser.parse_args()
    submit(args)