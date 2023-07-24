import subprocess
import sys
import pandas as pd
from pathlib import Path
from glob import glob

def get_size_shape_features(input_path, output_name, pipeline_path = Path("C:/Users/amulya/Documents/progeria-prediction/pipeline_measureobjs_v7.cppipe").resolve()):
    """
    purpose:
        run CellProfiler analysis pipeline - get size and shape info on each cell. these will be our input features.
    input:
        tif_path = path to directory with .tif images
    output: 
        DataFrame with information on nuclei/object size/shape measurements
    """
    output_path = str(Path().absolute()) + "\\" + output_name
    Path(output_path).mkdir(parents=True, exist_ok=True)
    cppath = Path("C:/Program Files/CellProfiler/CellProfiler.exe").resolve()
    subprocess.Popen([cppath, "-c", "-r", "-p", pipeline_path, "-o", output_path.encode('unicode_escape'), "-i", input_path])

import tensorflow
from stardist.models import StarDist2D
from stardist.plot import render_label
import skimage
from csbdeep.utils import normalize
import matplotlib.pyplot as plt
def segment_measure_stardist(input_path, output_name):
    
    """purpose:
        use StarDist to segment + get size and shape info on each cell. these will be our input features.
    input:
        tif_path = path to directory with .tif images
    output: 
        DataFrame with information on nuclei/object size/shape measurements """
    
    # from cellprofiler source code
    desired_properties = [
        "label",
        "image",
        "area",
        "perimeter",
        "bbox",
        "bbox_area",
        "major_axis_length",
        "minor_axis_length",
        "orientation",
        "centroid",
        "equivalent_diameter",
        "extent",
        "eccentricity",
        "convex_area",
        "solidity",
        "euler_number",
        "inertia_tensor",
        "inertia_tensor_eigvals",
        "moments",
        "moments_central",
        "moments_hu",
        "moments_normalized",
    ]
    model = StarDist2D.from_pretrained('2D_versatile_fluo')
    for tif in glob(f'{input_path}/*.tif'):
        img = skimage.io.imread(tif)
        print(img.shape)
        rescaled = skimage.transform.resize(normalize(img),  (img.shape[0] // 8, img.shape[1] // 8), anti_aliasing=False)
        print(rescaled.shape)
        labels, _ = model.predict_instances(rescaled, prob_thresh=0.5, nms_thresh=0.01)
        plt.imshow(render_label(labels, img=rescaled))
        plt.axis("off")
        plt.title("prediction + input overlay")
        plt.show()
        props = skimage.measure.regionprops_table(labels, properties=desired_properties)
        # print(props)

def main():
    input_dir = Path(sys.argv[1]).resolve()
    print(input_dir)
    output_dir = sys.argv[2]
    # segment_measure_stardist(input_dir, output_dir)
    if len(sys.argv) > 3:
        pipeline_path = Path(sys.argv[3]).resolve()
        get_size_shape_features(input_dir, output_dir, pipeline_path)
    get_size_shape_features(input_dir, output_dir)

if __name__ == "__main__":
    main()