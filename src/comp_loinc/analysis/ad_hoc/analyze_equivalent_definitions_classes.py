"""Analyze the set of 'class_' parts used for equivalent class defs in the supplemental model"""
import os
from pathlib import Path

import pandas as pd
from pprint import pprint as pp

THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent.parent.parent.parent
INPATH = PROJ_DIR / 'equivalent_groups_defs.tsv'
INPATH_PRIMARY = PROJ_DIR / 'equivalent_groups_defs_primary.tsv'
INDIR = PROJ_DIR / 'output' / 'analysis' / 'equivalent_def_collisions'

# TODO: save to file
#  - single TSV, where each model x (include indirect?) shows up. 1 col for each of those dimensions
def run():
    """Run analysis"""
    for path in [INPATH, INPATH_PRIMARY]:
        print(os.path.basename(path))
        df = pd.read_csv(path, sep='\t')
        df = df[df['property'] == 'class_'].sort_values('value')
        counts = df['label'].value_counts().to_dict()
        pp(counts)


if __name__ == '__main__':
    run()
