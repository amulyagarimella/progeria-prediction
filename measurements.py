import subprocess
import sys
import pandas as pd
from pathlib import Path

"""
    purpose:
        converts .ims to .tif
        see: https://github.com/alexcwsmith/imarisConverter
    input: 
        ims_path = path to directory with .ims images
    output:
        none
"""
def convert(ims_path):
    ims_to_tif_script_path = "C:\Users\amulya\Documents\imarisConverter\ACWS_convertImaris.py"
    subprocess.Popen(["python3", ims_to_tif_script_path, "--channel", 0, "--directory", ims_path])

"""
    purpose:
        run CellProfiler analysis pipeline - get size and shape info on each cell. these will be our input features.
    input:
        tif_path = path to directory with .tif images
    output: 
        DataFrame with information on nuclei/object size/shape measurements
"""
def get_size_shape_features(tif_path, output_name):
    pipeline_path = "single_cell_pipeline_progeria.cppipe"
    output_path = Path().absolute() + "\\" + output_name
    Path(output_path).mkdir(parents=True, exist_ok=True)
    subprocess.Popen(["cellprofiler", "-c", "-r", "-p", pipeline_path, "-o", output_path, "-i", tif_path])
    return pd.read_csv(f"{output_path}/Nuclei.csv")

def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    convert(input_dir)
    print(get_size_shape_features(input_dir, output_dir))

if __name__ == "__main__":
    main()