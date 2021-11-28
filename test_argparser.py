import argparse


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