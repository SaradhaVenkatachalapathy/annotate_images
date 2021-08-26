import argparse
from src.batch_processing import correct_annotation_labels_batch

# Parse the input arguments
options = argparse.ArgumentParser(description = "Correct annotations for a given set of images")

options.add_argument('--datadir', help = 'directory of raw images' , default = 'data/nuc_imgs/')
options.add_argument('--annodir', help = 'directory to uncorrected annotated images', default = 'data/nuc_labeled/')
options.add_argument('--userannodir', help = 'directory to output corrected annotations', default = 'data/nuc_user_corrected/')
options.add_argument('--large_image', type = str, help = 'Is this a large image?(will be downsampled)', default = 'no')
options.add_argument('--anno_depth', type = str, help = 'Depth of the annotated image', default = "8bit")
options.add_argument('--downsize_factor', type = str, help = 'Resizing factor for large iamge', default = 10)

arguments = options.parse_args()

# normalize the images in the folder
correct_annotation_labels_batch(path_to_input_dir = arguments.datadir, 
                                 path_to_uncorrected_annotations= arguments.annodir,
                                path_to_output_dir= arguments.userannodir,
                                 large_image = arguments.large_image,
                                 anno_img_depth = arguments.anno_depth,
                                 scale_factor = arguments.downsize_factor)

