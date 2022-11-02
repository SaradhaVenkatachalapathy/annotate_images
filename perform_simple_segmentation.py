import argparse
from annotate.batch_processing import perfrom_simple_intensity_based_segmentation

# Parse the input arguments
options = argparse.ArgumentParser(description = "Correct annotations for a given set of images")

options.add_argument('--datadir', help = 'directory of raw images' , default = 'data/nuc_imgs/')
options.add_argument('--savedir', help = 'directory to output segmentations', default = 'data/nuc_labeled/')
options.add_argument('--sigma', type = int, help = 'sigma to use for the gaussian filter', default = 1)
options.add_argument('--threshold_method', type = str, help = 'threshold method', default = "Otsu")
options.add_argument('--smallest_obj_area', type = int, help = 'Area of the smallest object(in pixels)', default = 25)
options.add_argument('--anno_depth', type = str, help = 'Depth of the annotated image', default = "8bit")

arguments = options.parse_args()

# normalize the images in the folder
perfrom_simple_intensity_based_segmentation(path_to_input_dir = arguments.datadir, 
                                            path_to_output_dir = arguments.savedir,
                                            fil_sigma = arguments.sigma,
                                            threshold_method = arguments.threshold_method,
                                            smallest_object_area = arguments.smallest_obj_area,
                                            label_img_depth = arguments.anno_depth)
