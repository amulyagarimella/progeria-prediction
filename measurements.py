import subprocess
import sys
import pandas as pd
from pathlib import Path
from glob import glob
import shutil

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
    ims_to_tif_script_path = Path("C:/Users/amulya/Documents/imarisConverter/ACWS_convertImaris.py")
    print(ims_to_tif_script_path)
    subprocess.Popen(["python3", str(ims_to_tif_script_path), "--channel", "0", "--directory", ims_path])
    tif_list = glob(str(ims_path) + "\\" + "*.tif")
    target = str(ims_path) + "\\" + "tifs"
    Path(target).mkdir(parents=True, exist_ok=True)
    for tif in tif_list:
        shutil.move(tif, target)
    return target

"""
    purpose:
        run CellProfiler analysis pipeline - get size and shape info on each cell. these will be our input features.
    input:
        tif_path = path to directory with .tif images
    output: 
        DataFrame with information on nuclei/object size/shape measurements
"""
def get_size_shape_features(tif_path, output_name):
    pipeline_path = Path("C:/Users/amulya/Documents/progeria-prediction/single_cell_pipeline_progeria.cppipe").resolve()
    print(pipeline_path)
    output_path = str(Path().absolute()) + "\\" + output_name
    Path(output_path).mkdir(parents=True, exist_ok=True)
    cppath = Path("C:/Program Files/CellProfiler/CellProfiler.exe").resolve()
    subprocess.Popen([cppath, "-c", "-r", "-p", pipeline_path, "-o", output_path.encode('unicode_escape'), "-i", tif_path])


def main():
    input_dir = Path(sys.argv[1]).resolve()
    print(input_dir)
    target = str(input_dir) + "\\" + "images"
    output_dir = sys.argv[2]
    # tifdir = convert(input_dir)
    get_size_shape_features(target, output_dir)

if __name__ == "__main__":
    main()