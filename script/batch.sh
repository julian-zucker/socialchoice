#!/usr/bin/env bash
#SBATCH --job-name=VoteInduction
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=6Gb
#SBATCH --partition=general

module load python/3.7.0
srun run.sh
#python3 results.py dog_project_votes.csv
