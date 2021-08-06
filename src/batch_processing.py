# -*- coding: utf-8 -*-
from pathlib import Path
import os
from glob import glob
from tifffile import imread, imsave

from src.basic_image_processing_tasks import simple_intensity_based_segmentation
from src.interactive_segmentation import correcting_annotation_large_image,correcting_annotation,generate_labels_large_image,generate_labels

def generate_annotation_labels_batch(path_to_input_dir,
                                    path_to_output_dir,
                                    large_image = False, anno_img_depth = "8bit",
                                    scale_factor = 10):
    
    """Generate annotation of all images in folder
    
    Args:
        path_to_raw_images              : path to raw images to use as guide
        path_to_output_dir              : path to the output directory 
        large_image                     : is the image large? (true- performs resizing)
        anno_img_depth                  : depth of the output image 
        scale_factor                    : resizing factor
    """
    
    # Make sure that the output directory exists-if not create it. 
    Path(path_to_output_dir).mkdir(parents=True, exist_ok=True)

    # Extract the paths to images (assumed here to be TIF)
    path_to_raw_images = sorted(glob(path_to_input_dir + "*.tif"))
    
    for i in range(len(path_to_raw_images)):
        #Extract the file name
        img_name = os.path.splitext(os.path.basename(path_to_raw_images[i]))[0]
        
        #correct annotation
        if(large_image):
            corrected_labels =  generate_labels_large_image(path_to_raw_images[i],
                                              label_img_depth = anno_img_depth,
                                              resize_factor = scale_factor)
        else:
            corrected_labels =  generate_labels(path_to_raw_images[i],
                                              label_img_depth = anno_img_depth)
                                              
        #Write the image to the user defined output directory
        imsave(path_to_output_dir+"/"+img_name+".tif", corrected_labels) 
        


def correct_annotation_labels_batch(path_to_input_dir,path_to_uncorrected_annotations,
                                    path_to_output_dir,
                                    large_image = False, anno_img_depth = "8bit",
                                    scale_factor = 10):
    
    """Correct annotation of all images in folder
    
    Args:
        path_to_raw_images              : path to raw images to use as guide
        path_to_uncorrected_annotations : path to uncorrected annotated images
        path_to_output_dir              : path to the output directory 
        large_image                     : is the image large? (true- performs resizing)
        anno_img_depth                  : depth of the output image 
        scale_factor                    : resizing factor
    """
    
    # Make sure that the output directory exists-if not create it. 
    Path(path_to_output_dir).mkdir(parents=True, exist_ok=True)

    # Extract the paths to images (assumed here to be TIF)
    path_to_raw_images = sorted(glob(path_to_input_dir + "*.tif"))
    
    for i in range(len(path_to_raw_images)):
        #Extract the file name
        img_name = os.path.splitext(os.path.basename(path_to_raw_images[i]))[0]
        
        #correct annotation
        if(large_image):
            corrected_labels =  correcting_annotation_large_image(path_to_raw_images[i],
                                              path_to_uncorrected_annotations+"/"+ img_name +".tif",
                                              label_img_depth = anno_img_depth,
                                              resize_factor = scale_factor)
        else:
            corrected_labels =  correcting_annotation(path_to_raw_images[i],
                                              path_to_uncorrected_annotations+"/"+ img_name +".tif",
                                              label_img_depth = anno_img_depth)
                                              
        #Write the image to the user defined output directory
        imsave(path_to_output_dir+"/"+img_name+".tif", corrected_labels)                                      



def perfrom_simple_intensity_based_segmentation(path_to_input_dir,path_to_output_dir,
                                                fil_sigma=1,
                                                threshold_method="Otsu",
                                                smallest_object_area = 5,
                                                label_img_depth = "8bit"):
    """ Segment objects in a given image for all images in a folder
     
    Args:
        path_to_input_dir  : path to a input directory
        path_to_output_dir : path to the output directory 
        fil_sigma          : sigma to use for the gaussian filter
        threshold_method   : threshold method
        smallest_object_area : smallest area of objects in pixels
        label_img_depth         : label depth
     
    """

    # Make sure that the output directory exists-if not create it. 
    Path(path_to_output_dir).mkdir(parents=True, exist_ok=True)

    # Extract the paths to images (assumed here to be TIF)
    path_to_raw_images = sorted(glob(path_to_input_dir + "*.tif"))
    
    for i in range(len(path_to_raw_images)):
        #Read in the image
        raw_img = imread(path_to_raw_images[i])

        #Extract the file name
        img_name = os.path.splitext(os.path.basename(path_to_raw_images[i]))[0]
        
        #segment_image
        labelled_image = simple_intensity_based_segmentation(raw_img, 
                                                     gaussian_sigma=fil_sigma,
                                                     thresh_method=threshold_method,
                                                     smallest_area_of_object=smallest_object_area)

        #Write the image to the user defined output directory
        imsave(path_to_output_dir+"/"+img_name+".tif", labelled_image)