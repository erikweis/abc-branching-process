#!/bin/bash
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --mem=1gb
#SBATCH --time=02:59:59
#SBATCH --job-name=1997

python discretebranchingprocess.py -f test2.csv