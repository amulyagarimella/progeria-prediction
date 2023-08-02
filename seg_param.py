import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sys
import pickle
import skimage
from imaris_ims_file_reader.ims import ims
import h5py
import tables
np.random.seed(42) # for reproducibility

sys.path.insert(1, 'aics-shparam')
from aicsshparam import shtools, shparam

sys.path.insert(1, 'aics-segmentation')
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_3d


tables.file._open_files.close_all()
fn = TODO IMS
f = ims(fn,write=True)
c1 = f[0][0]
c2 = f[0][1]

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
    skimage.io.imsave("TODO Late_progeria_IF_Test_1_c2_binarymask_v2.tif", binary_mask)
    return binary_mask

def (binary_mask, lmax=16):
    (coeffs, _), (image_, mesh, grid_down, transform) = shparam.get_shcoeffs(image=binary_mask, lmax=lmax)
    coeffs = pd.DataFrame.from_dict({k : [v] for k, v in coeffs.items()})
    with open("TODO progeria_test_binary_v2_coefs_l16.pkl", "wb") as f:
        pickle.dump(coeffs, f)
    mesh_orig, img_output, centroid = shtools.get_mesh_from_image(image=binary_mask)
    shtools.save_polydata(mesh, 'mesh_calc_binary_l16_v2.vtk')
    shtools.save_polydata(mesh_orig, 'mesh_orig_binary_v2.vtk')




