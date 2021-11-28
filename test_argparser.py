import argparse

def get_bash_script(fpath,r0,k,r):

    return f"""#!/bin/bash
        #SBATCH --partition=short
        #SBATCH --nodes=1
        #SBATCH --mem=1gb
        #SBATCH --time=02:59:59
        #SBATCH --job-name=1997

        python discretebranchingprocess.py -f {fpath} -r0 {r0} -k {k} -r {r}"""

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f',type=str,help='filename to save the output')
    parser.add_argument('-r0',type=float,help='expected secondary infections parameter for negative binomial distribution')
    parser.add_argument('-k',type= float,help='dispersion parameter for negative binomial')
    parser.add_argument('-r',type=float,help='carry-over infections proportion at each time step')
    parser.add_argument('--cutoff',default = -1, type=float,help='stop simualtion after N steps')
    parser.add_argument('--state',default='hi')


    args = parser.parse_args()
    print(dir(args))
    print(args.f)
    print(args.r0)
    print(args.k)
    print(args.r)
    print(args.cutoff)
    print(type(args))