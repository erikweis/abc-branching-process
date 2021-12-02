#!/bin/sh

#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --mem=2gb
#SBATCH --time=0:20:00
#SBATCH --job-name=1997

echo $NUM_TRIALS
python submitter_all_python.py --num_trials $NUM_TRIALS --state $STATE --error $ERROR --foldername $FOLDERNAME
