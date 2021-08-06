import argparse
from src.batch_processing import generate_annotation_labels_batch

# Parse the input arguments
options = argparse.ArgumentParser(description = "Interactively annotate all images in a given directory")

options.add_argument('--datadir', help = 'directory of raw images' , default = 'data/nuc_imgs/')
options.add_argument('--savedir', help = 'directory to store normalized images', default = 'data/nuc_user_annotated/')
options.add_argument('--large_image', type = bool, help = 'Is this a large image?(will be downsampled)', default = False)
options.add_argument('--anno_depth', type = str, help = 'Depth of the annotated image', default = "8bit")
options.add_argument('--downsize_factor', type = int, help = 'Resizing factor for large iamge', default = 10)

arguments = options.parse_args()

# normalize the images in the folder
generate_annotation_labels_batch(path_to_input_dir = arguments.datadir, 
                                 path_to_output_dir= arguments.savedir,
                                 large_image = arguments.large_image,
                                 anno_img_depth = arguments.anno_depth,
                                 scale_factor = arguments.downsize_factor)
