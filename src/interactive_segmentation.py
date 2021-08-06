# -*- coding: utf-8 -*-
import napari
from skimage import data
import skimage.filters as skfil
from skimage.measure import label
from tifffile import imread, imsave
from skimage.transform import resize
import numpy as np
from skimage.morphology import remove_small_objects
from skimage.util import img_as_ubyte
import cv2

from napari.utils.settings import SETTINGS
SETTINGS.application.ipy_interactive = False

def napari_interactive_annotation(base_image, label_image):
    """Perform interactive annotation of an image
    
    Args:
        base_image    : fluroscent image to use as a guide
        segmentation layer : label image

    """
    
    # create the viewer and add image
    viewer = napari.Viewer()
    image_layer = viewer.add_image(base_image, name='base_image', multiscale=False)
    labels_layer = viewer.add_labels(label_image)
    napari.run() 
    
    #napari automatically updates the label image, but I am being unnecessarily careful here :/
    updated_labels = labels_layer.data

    return updated_labels

def generate_object_labels(raw_image, label_img_depth = "8bit"):
    """Perform interactive annotation of an image
    
    Args:
        raw_image_path    : path to a raw image
        output_image_path : path to output directory
        label_img_depth   : depth of the output (labelled) image 
        resize_factor : resizing factor

    """
    #Read image

    # add an empty image to the image 
    if (label_img_depth == "8bit"):
        label_image = np.zeros((raw_image.shape[0],raw_image.shape[1]), dtype=np.uint8)
    elif (label_img_depth == "16bit"):
        label_image = np.zeros((raw_image.shape[0],raw_image.shape[1]), dtype=np.uint16)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
    
    labelled_image = napari_interactive_annotation(raw_image,label_image)
             
    return labelled_image

def generate_labels_large_image(raw_image_path,label_img_depth = "8bit",resize_factor=10):
    """Perform interactive annotation of a large image
    
    Args:
        raw_image_path    : path to a raw image
        label_img_depth   : depth of the output (labelled) image 
        resize_factor : resizing factor

    """
    #Read image
    raw_img = imread(raw_image_path)

    #Downsize image to make the annotation easier (napari does not handle large images gracefully!)
    image_resized = cv2.resize(raw_img, dsize=((raw_img.shape[0] // resize_factor),(raw_img.shape[1] // resize_factor)))
    image_resized = cv2.normalize(image_resized, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    #generate the labels
    updated_labels = generate_object_labels(image_resized)

    #upsize image
    labelled_image_upsized = cv2.resize(updated_labels, dsize=((updated_labels.shape[0] * 10),(updated_labels.shape[1] * 10)))    
    # correct image depth
    if (label_img_depth == "8bit"):
        labelled_image_upsized = cv2.normalize(labelled_image_upsized, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_8U)
    elif (label_img_depth == "16bit"):
        labelled_image_upsized = cv2.normalize(labelled_image_upsized, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_16U)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
    
    return labelled_image_upsized           

def generate_labels(raw_image_path,label_img_depth = "8bit"):
    """Perform interactive annotation of an image
    
    Args:
        raw_image_path    : path to a raw image
        label_img_depth   : depth of the output (labelled) image 
    
    Return:
        Segmented image
    """
    #Read image
    raw_img = imread(raw_image_path)
    raw_img = cv2.normalize(raw_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    #generate the labels
    updated_labels = generate_object_labels(raw_img)

    # correct image depth
    if (label_img_depth == "8bit"):
        updated_labels = cv2.normalize(updated_labels, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_8U)
    elif (label_img_depth == "16bit"):
        updated_labels = cv2.normalize(updated_labels, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_16U)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
   
    return updated_labels

def correcting_annotation_large_image(raw_image_path, annotated_image_path,
                                      label_img_depth = "8bit",resize_factor = 10):
    """Correct annotation of an image
    
    Args:
        raw_image_path    : path to a raw image
        anno_image_path   : path to uncorrected annotations
        label_img_depth   : depth of the output image 
        resize_factor     : resizing factor
        
    Return:
        Corrected image
    """
    
    #Read images
    raw_img = imread(raw_image_path)
    lab_img = imread(annotated_image_path)
    
    if (raw_img.shape[0]!=lab_img.shape[0] or raw_img.shape[1]!=lab_img.shape[1]):
        raise Exception('The raw and annotated images have different sizes')
    
    #Downsize image to make the annotation easier (napari does not handle large images gracefully!)
    image_resized = cv2.resize(raw_img, dsize=((raw_img.shape[0] // resize_factor),(raw_img.shape[1] // resize_factor)))
    image_resized = cv2.normalize(image_resized, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    label_resized = cv2.resize(lab_img, dsize=((lab_img.shape[0] // resize_factor),(lab_img.shape[1] // resize_factor)))

    updated_labels = napari_interactive_annotation(image_resized,label_resized)
    
    #upsize image
    labelled_image_upsized = cv2.resize(updated_labels, dsize=((updated_labels.shape[0] * 10),(updated_labels.shape[1] * 10)))
    
     # correct image depth
    if (label_img_depth == "8bit"):
        labelled_image_upsized = cv2.normalize(labelled_image_upsized, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_8U)
    elif (label_img_depth == "16bit"):
        labelled_image_upsized = cv2.normalize(labelled_image_upsized, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_16U)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
    

    return labelled_image_upsized

def correcting_annotation(raw_image_path, annotated_image_path,label_img_depth = "8bit"):
    """Correct annotation of an image
    
    Args:
        raw_image_path    : path to a raw image
        anno_image_path   : path to uncorrected annotations
        label_img_depth   : depth of the output image 
        
    Return:
        Corrected image
    """
    
    #Read images
    raw_img = imread(raw_image_path)
    lab_img = imread(annotated_image_path)
    
    if (raw_img.shape[0]!=lab_img.shape[0] or raw_img.shape[1]!=lab_img.shape[1]):
        raise Exception('The raw and annotated images have different sizes')
    
    raw_img = cv2.normalize(raw_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    #coorect annoations
    updated_labels = napari_interactive_annotation(raw_img,lab_img)
    
    
     # correct image depth
    if (label_img_depth == "8bit"):
        updated_labels = cv2.normalize(updated_labels, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_8U)
    elif (label_img_depth == "16bit"):
        updated_labels = cv2.normalize(updated_labels, None, 0, np.max(updated_labels), cv2.NORM_MINMAX, cv2.CV_16U)
    else:
        raise Exception('Invalid input: should be among {8bit, 16bit}')
    

    return updated_labels
    
    