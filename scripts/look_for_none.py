#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import base64
import json
import os

file = sys.argv[1]
print(f'Searching {file}')
data = pd.read_csv(file, sep='\t')

print(f"Total columns: {len(data['node_synonyms'])}")
node_synonyms_not_None = data[data['node_synonyms'].str.contains('None')==False]
print(f"Columns where node_synonyms is not None: {len(node_synonyms_not_None)}")
node_dbxrefs_not_None = data[data['node_dbxrefs'].str.contains('None')==False]
print(f"Columns where node_dbxrefs is not None: {len(node_dbxrefs_not_None)}")
both_not_None = node_synonyms_not_None[node_synonyms_not_None['node_dbxrefs'].str.contains('None')==False]
print(f"Columns where node_synonyms && node_dbxrefs is not None: {len(both_not_None)}")
print('Done!')