#! /usr/bin/env python

from __future__ import print_function

import os
import subprocess

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz


df = pd.read_csv("/data/digital-analytics/i637308/data/input.csv")
print("* df.head()", df.head(), sep="\n", end="\n\n")
print("* df.tail()", df.tail(), sep="\n", end="\n\n")
    
ages_dict = {"1": 1, "6": 2, "7": 3, "8": 4, "9": 5, "A": 6, "?": 0, np.nan: 0}
segments_dict = {"C01": 1, "C02": 2, "C03": 3, "CP4": 4, "C00": 5, np.nan: 0}
inmkt_dict = {"IN": 1, "OUT": 0, np.nan: 0}
yn_dict = {"Y": 1, "N": 0, np.nan: 0}
	
df["age"] = df["AGE_RNG"].map(ages_dict)
df["segment"] = df["segment_cd"].map(segments_dict)
df["inmkt"] = df["in_market"].map(inmkt_dict)
df["has_ext"] = df["has_ext_acct"].map(yn_dict)

# df.astype(str).groupby(["AGE_RNG", "age"]).size()
# pd.crosstab(df.AGE_RNG, df.age)
# df.groupby(["segment_cd", "segment"]).size()
# df.groupby(["in_market", "inmkt"]).size()

#df.dtypes
#df.has_ext_acct.unique()
#	array(['N', 'Y'], dtype=object)

def encode_target(df, target_column):
	"""Add column to df with integers for the target.

	Args
	----
	df -- pandas DataFrame.
	target_column -- column to map to int, producing
	                 new Target column.

	Returns
	-------
	df_mod -- modified DataFrame.
	targets -- list of target names.
	"""
	df_mod = df.copy()
	targets = df_mod[target_column].unique()
	map_to_int = {name: n for n, name in enumerate(targets)}
	df_mod["Target"] = df_mod[target_column].replace(map_to_int)

	return (df_mod, targets)


df2, targets = encode_target(df, "grp")
print("* df2.head()", df2[["Target", "grp"]].head(), sep="\n", end="\n\n")
print("* df2.tail()", df2[["Target", "grp"]].tail(), sep="\n", end="\n\n")
print("* targets", targets, sep="\n", end="\n\n")




flist=[
'age', 
'segment', 
'inmkt', 
'has_ext',
'cnt_crd_any', 
'cnt_dep_any', 
'cnt_crd_per', 
'cnt_crd_bus', 
'cnt_crd_per_brd', 
'cnt_crd_bus_brd', 
'cnt_dda', 
#'cnt_dep_oth', 
#'cnt_heloc', 
'ever_dig_active', 
'ever_epay', 
#'ever_auto', 
#'cnt_acct', 
#'acct_has_bal', 
#'acct_has_bal_w_due', 
#'acct_has_bal_wo_due', 
'cnt_crd_per_pnr', 
'cnt_crd_bus_pnr'
]

df3=df2[flist]
features = list(df3.columns)
print("* features:", features, sep="\n")



y = df2["Target"]
X = df2[features]
dt = DecisionTreeClassifier(min_samples_split=5000000, random_state=99)
dt.fit(X, y)


with open("dt.dot", 'w') as f:
	f = export_graphviz(dt, out_file = f, feature_names = features)



#def visualize_tree(tree, feature_names):
#	"""Create tree png using graphviz.
#	
#	Args
#	----
#	tree -- scikit-learn DecsisionTree.
#	feature_names -- list of feature names.
#	"""
#	with open("dt.dot", 'w') as f:
#		export_graphviz(tree, out_file=f, feature_names=feature_names)
#	command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
#	try:
#		subprocess.check_call(command)
#	except:
#		exit(	"Could not run dot, ie graphviz, to " 
#					"produce visualization")
#
#
#visualize_tree(dt, features)


