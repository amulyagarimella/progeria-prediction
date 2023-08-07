import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import sys
import skimage
from imaris_ims_file_reader.ims import ims
import tables
import glob

sys.path.insert(1, 'aics-shparam')
from aicsshparam import shtools, shparam

sys.path.insert(1, 'aics-segmentation')
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_3d

np.random.seed(42) # for reproducibility

def preprocess_image (channel):
    intensity_scaling_param = [4000]
    struct_img = intensity_normalization(channel, scaling_param=intensity_scaling_param)
    gaussian_smoothing_sigma = 8
    structure_img_smooth = image_smoothing_gaussian_3d(struct_img, sigma=gaussian_smoothing_sigma)
    return structure_img_smooth

def binary_mask (channel, show=False):
    binary_mask = np.zeros(np.shape(channel))
    for i in range(np.shape(channel)[0]):
        # Otsu filter
        thresh = skimage.filters.threshold_otsu(channel[i])
        binary = channel[i] > thresh
        # Closing
        bw = skimage.morphology.closing(binary, skimage.morphology.square(5))
        # Get objects, take largest object
        labeled,_ = scipy.ndimage.label(bw)
        region_table = pd.DataFrame.from_dict(skimage.measure.regionprops_table(labeled,properties=['label','area']))
        largest = region_table.loc[np.argmax(region_table['area']),'label']
        # Add largest object to binary mask
        binary_mask[i][np.where(labeled==largest)] = 1
        image_label_overlay = skimage.color.label2rgb(binary_mask[i], image=channel[i], bg_label=0)
        if show:
            plt.imshow(image_label_overlay)
            plt.show()
    return binary_mask

def parameterize (binary_mask, lmax=16, ):
    (coeffs, _), _ = shparam.get_shcoeffs(image=binary_mask, lmax=lmax)
    coeffs = pd.DataFrame.from_dict({k : [v] for k, v in coeffs.items()})
    return coeffs

def get_all_coeffs_ims (dir):
    coeffs_all = pd.DataFrame()
    for fn in glob.glob(f"{dir}/*ims"):
        print(fn)
        tables.file._open_files.close_all()
        try:
            f = ims(fn,write=True)
        except Exception as e:
            print("file opening unsuccessful")
            print(e)
            continue
        print("file opening successful")
        c2 = f[0][1]
        bm = binary_mask(preprocess_image(c2))
        coeffs = parameterize(bm)
        coeffs = coeffs.assign(orig = fn)
        coeffs_all = pd.concat([coeffs_all, coeffs])
    coeffs_all.to_csv(f"{dir}/aics_coeffs_ims.csv")
    return coeffs_all

def main():
    get_all_coeffs_ims(sys.argv[1])

if __name__ == '__main__':
    progeria_dirs = ["Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Passage 22 Progeria/PostEX_P22progeria_IF_DAPI_LMNA_Nup_LMNB1_0.2/", "Y:/users/Ajay/New progeria lines IF/Progerin_LMNA_K9ME2_K9ME4/2023-01-19/", "Y:/users/Ajay/IF_Progeria1972/Late_passage/2023-02-07/"]
    normal_dirs = ["Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Normal Progeria/PostEX_NP_IF_Progerin_LMNA_Nup_LMNB1/", "Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Normal Progeria/PostEX_NP_IF_LMNA_K9me2_K9me3/", "Y:/users/Ajay/IF_Progeria1972/Normal fibroblast/2023-02-10/"]
    dirs = progeria_dirs + normal_dirs
    done_already = ["Y:/users/Ajay/IF_Progeria1972/Normal fibroblast/2023-02-10/", "Y:/users/Ajay/IF_Progeria1972/Late_passage/2023-02-07/"]
    for d in dirs:
        if d not in done_already:
            get_all_coeffs_ims(d)