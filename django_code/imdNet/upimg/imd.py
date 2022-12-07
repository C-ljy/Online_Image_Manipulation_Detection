from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.compat.v1 as tf
tf.logging.set_verbosity(tf.logging.ERROR)
from upimg._lib.config import config as cfg
from upimg._lib.utils.nms_wrapper import nms
from upimg._lib.utils.test import im_detect
from upimg._lib.nets.vgg16 import vgg16
from upimg._lib.utils.timer import Timer


# % matplotlib
# inline

CLASSES = ('__background__',
           'tampered')

# PLEASE specify weight files dir for vgg16
NETS = {'vgg16': ('vgg16_faster_rcnn_iter_40000.ckpt',)}

def fig2data(fig, form="RGBA"):
    """
    fig = plt.figure()
    image = fig2data(fig)
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    import PIL.Image as Image
    # draw the renderer
    fig.canvas.draw()
 
    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    image = Image.frombytes(form, (w, h), buf.tostring())
    # image = np.asarray(image)
    return image


def vis_detections(im, class_name, dets, image_name, save_path, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
        )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('Image: {} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name, thresh),
                 fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    
    plt.savefig(os.path.join(save_path, image_name), bbox_inches='tight')
    #plt.show()


def demo(sess, net, image_name, load_path, save_path, CONF_THRESH):
    """Detect object classes in an image using pre-computed object proposals."""
    # Load test image
    im = cv2.imread(os.path.join(load_path, image_name))

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    #print('Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]))

    # Visualize detections for each class
    NMS_THRESH = 0.2
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1  # because we skipped background
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, image_name, save_path, thresh=CONF_THRESH)


def imd(imgs, load_path, save_path, model_path,
        conf_thresh=0.2, useGpu=False, demonet='vgg16'):

    ## Just for test
    #print("\nimd test")
    #print(save_path)
    #print(load_path)
    #print(model_path)
    #print("\n")
    
    if conf_thresh < 1e-6 or conf_thresh > 1.0-1e-6:
        raise Exception("conf_thresh is illegal, please set (0.0, 1.0)")
        
    # model path
    tfmodel = os.path.join(model_path,  NETS[demonet][0])
    #print(tfmodel)
    if not os.path.isfile(tfmodel + '.meta'):
        print(tfmodel)
        raise IOError(('{:s} not found.\nDid you download the proper networks from '
                       'our server and place them properly?').format(tfmodel + '.meta'))

    tf.reset_default_graph()
    # set config
    if useGpu:
        tfconfig = tf.ConfigProto(allow_soft_placement=True)
        tfconfig.gpu_options.allow_growth = True
    else:
        tfconfig = tf.ConfigProto(device_count={"CPU":1})

    # init session
    with tf.Session(config=tfconfig) as sess:
        # load network
        if demonet == 'vgg16':
            net = vgg16(batch_size=1)
        else:
            raise NotImplementedError
        net.create_architecture(sess, "TEST", 2,
                                tag='default', anchor_scales=[8, 16, 32])
        saver = tf.train.Saver()
        saver.restore(sess, tfmodel)

        #print('Loaded network {:s}'.format(tfmodel))

        for img in imgs:
            demo(sess, net, img, load_path, save_path, conf_thresh)
           
#if __name__ == '__main__':
    #imd(["tampered1.jpg", "tampered2.jpg"], load_path="/mnt/hgfs/Learning-Rich-Features-for-Image-Manipulation-Detection/data/ImageForTest/", save_path="../media/download/", model_path=os.path.join('/mnt/hgfs/Learning-Rich-Features-for-Image-Manipulation-Detection/', 'default', 'gene_2007_trainval', 'default'))


