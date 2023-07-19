import subprocess
import sys
import pandas as pd
from pathlib import Path
from glob import glob

"""
    purpose:
        run CellProfiler analysis pipeline - get size and shape info on each cell. these will be our input features.
    input:
        tif_path = path to directory with .tif images
    output: 
        DataFrame with information on nuclei/object size/shape measurements
"""
def get_size_shape_features(input_path, output_name, pipeline_path = Path("C:/Users/amulya/Documents/progeria-prediction/pipeline_measureobjs_v4.cppipe").resolve()):
    output_path = str(Path().absolute()) + "\\" + output_name
    Path(output_path).mkdir(parents=True, exist_ok=True)
    cppath = Path("C:/Program Files/CellProfiler/CellProfiler.exe").resolve()
    subprocess.Popen([cppath, "-c", "-r", "-p", pipeline_path, "-o", output_path.encode('unicode_escape'), "-i", input_path])

def main():
    input_dir = Path(sys.argv[1]).resolve()
    print(input_dir)
    output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        pipeline_path = Path(sys.argv[3]).resolve()
        get_size_shape_features(input_dir, output_dir, pipeline_path)
    get_size_shape_features(input_dir, output_dir)

if __name__ == "__main__":
    main()