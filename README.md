# Annotate_images
Interactively generate/edit segmentation labels using napari

For more details on how to generate and edit annotations please refer to: https://napari.org/tutorials/fundamentals/labels.html
## Installation 

The current implementation has been developed in Python 3.

In order to avoid any changes to the local packages, install in a virtual environment (optional).

```
   $ conda create --name annotate_napari python
   $ conda activate annotate_napari
```

To clone the repository run the following from the terminal.

```
   $ git clone https://github.com/SaradhaVenkatachalapathy/Annotate_images.git
```

Then install requirements and run the setup from the repository directory

```
   $ pip install -r requirements.txt
   $ python setup.py install
```
## Useage

To manually generate annotations, run the following. 
```
   $ python annotate_images.py --datadir <path/to/image/directory> --savedir <path/to/output/directory> --large_image <True/False> --anno_img_depth <depth_of_annotated_image --downsize_factor <scaling_factor_for_large_images>
```
To correct existing annotations, run the following. 
```
   $ python perform_simple_segmentation.py --datadir <path/to/image/directory> --annodir <path/to/annoated/images> --userannodir <path/to/output/directory> --large_image <True/False> --anno_img_depth <depth_of_annotated_image --downsize_factor <scaling_factor_for_large_images>
```

To correct segmented labels, use the following. 
```
   $ python correct_annotation.py --datadir <path/to/image/directory> --annodir <path/to/annotated/image/directory> --userannodir <path/to/output/directory> --large_image <True/False> --anno_img_depth <depth_of_annotated_image --downsize_factor <scaling_factor_for_large_images>
```

TO DO: add functions for model based instace segmentation
