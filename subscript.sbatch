#!/bin/sh

#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --mem=2gb
#SBATCH --time=3:00:00
#SBATCH --job-name=1997

echo $NUM_TRIALS
echo $SUBDIR
python run_simulations.py --num_trials $NUM_TRIALS --state $STATE --error $ERROR --foldername $FOLDERNAME --subdir $SUBDIR --non_parametric $NONPARAMETRIC
