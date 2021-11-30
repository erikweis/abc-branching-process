#!/bin/bash
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --mem=2gb
#SBATCH --time=0:20:00
#SBATCH --job-name=1997

sbatch python submitter_all_python.py --num_trials $NUMTRIALS --state $STATE --error $ERROR --foldername $FOLDERNAME