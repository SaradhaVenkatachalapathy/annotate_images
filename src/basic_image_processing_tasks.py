# -*- coding: utf-8 -*-
import napari
from skimage import data
import skimage.filters as skfil
from skimage.measure import label
from tifffile import imread, imsave
from skimage.transform import resize
import numpy as np
from skimage.morphology import remove_small_objects
import cv2


def gen_background_mask(image, threshold_method = "Otsu", user_thresh = None):
    """Performs intensity based thresholding to generate a background mask
    
    Args:
        image : image to be thresholded (this is expected to a gray scale image)
        thresolding method : method to use for identifying lower threshold (default is Otsu)
        lower_thresh : user-defined lower threshold
    Returns:
        A binary image where the background is set to 0
    """
    
    # extract threshold
    if (threshold_method == "Li"):
        thresh = skfil.threshold_li(image)
    elif (threshold_method == "Otsu"):
        thresh = skfil.threshold_otsu(image)
    elif (threshold_method == "Isodata"):
        thresh = skfil.threshold_isodata(image)
    elif (threshold_method == "Mean"):
        thresh = skfil.threshold_mean(image)
    elif (threshold_method == "Minimum"):
        thresh = skfil.threshold_minimum(image)
    elif (threshold_method == "Triangle"):
        thresh = skfil.threshold_triangle(image)
    elif (threshold_method == "Yen"):
        thresh = skfil.threshold_yen(image)
    elif (threshold_method == "Manual"):
        if user_thresh is None:
            raise Exception("Manual threshold requires a user-defined threshold value")
        else:
            thresh = user_thresh
    else:
        raise Exception('Invalid threshold_method: should be among {"Li","Otsu","Isodata","Mean","Minimum","Triangle","Yen", "Manual"}')
        
    # generate a background mask
    bw = (image > thresh)
    
    return bw

def simple_intensity_based_segmentation(image, gaussian_sigma=1, thresh_method="Otsu", smallest_area_of_object=5,label_img_depth = "8bit"):
    """Perform intensity based thresholding and detect objects
    
    Args:
        raw_image_path          : path to a raw image
        gaussian_sigma          : sigma to use for the gaussian filter
        thresh_method           : threshold method
        smallest_area_of_object : smallest area of objects in pixels
        label_img_depth         : label depth

    Returns:
        A labelled image
    """
    
    # apply a gaussian filter
    image_smooth = skfil.gaussian(image, sigma=gaussian_sigma, preserve_range = True)
    
    # apply threshold
    bw = gen_background_mask(image_smooth, threshold_method = thresh_method)
    
    #remove small objects
    bw_size_filtered = remove_small_objects(bw,smallest_area_of_object )
    
    #Label connected components
    label_image = label(bw_size_filtered)
    
    # add an empty image to the image 
    if (label_img_depth == "8bit"):
        label_image_cor = cv2.normalize(label_image, None, 0, np.max(label_image), cv2.NORM_MINMAX, cv2.CV_8U)
    elif (label_img_depth == "16bit"):
        label_image_cor = cv2.normalize(label_image, None, 0, np.max(label_image), cv2.NORM_MINMAX, cv2.CV_16U)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
    
    return label_image_cor
    