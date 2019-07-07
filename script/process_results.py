"""
This file parses the output from running results.py into a nice table.

Run from the top level like:
python3 script/process_results.py data/dog_project_tau.csv > data/dog_project_tau_aggregates.txt
"""
import csv
import sys
from collections import defaultdict

import numpy as np


def parse_results(results):
    vote_induction_method_to_taus = defaultdict(lambda: [])

    for row in results:
        tau = row[0]
        # But it's formatted as `tau=<actual tau value>`
        tau = float(tau.replace("tau=", ""))

        induction_method = tuple(row[1:])
        vote_induction_method_to_taus[induction_method] += [tau]

    for (int, inc), taus in vote_induction_method_to_taus.items():
        print(f"{int}\t{inc}\t{np.mean(taus)}\t{np.std(taus)}")


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as fd:
        parse_results(list(csv.reader(fd)))
