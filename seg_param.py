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
        tables.file._open_files.close_all()
        f = ims(fn,write=True)
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
    main()