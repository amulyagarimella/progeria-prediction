import pandas as pd
from glob import glob
import numpy as np
import shutil
import os

prog_dir = " Y:/users/Amulya/converted_v2/progeria"
dir_to_remove = ["Y:/users/Ajay/New progeria lines IF/Progerin_LMNA_K9ME2_K9ME4/2023-01-19/"]
mp = pd.read_csv("mapping.csv",index_col=None,header=None)
to_rem = [x.split("\\")[-1] for x in mp.loc[mp.iloc[:,1].isin(dir_to_remove)].iloc[:,0]]
to_rem = [y for x in to_rem for y in glob(f"{prog_dir}/*/{x}*")]
print(to_rem)

"""dest = f"{prog_dir}/unmagnified/"
os.makedirs(os.path.dirname(dest), exist_ok=True)
for f in to_rem:
    shutil.move(f, dest)"""