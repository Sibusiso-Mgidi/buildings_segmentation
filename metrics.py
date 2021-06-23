import numpy as np
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf

SMOOTH = 1e-10


def get_iou(A, B):
    """
    This method defines the intersection over union metric using the Jaccard metrics. The Jaccards metrics is the
    evaluation metrics which coomputes the overlapping between the ground truth and prediction.
    :returns: iou
    """
    # borrowed from https://www.kaggle.com/aglotero/another-iou-metric

    # get the ground and prediction values
    t , p  = A > 0,  B > 0 

        
    # compute the truth value of t OR p element-wise.
    union = np.logical_or(t, p)

    # compute the truth value of A AND B element-wise.
    intersection = np.logical_and(A, B)
    
    # computes the intersection over union so that the probability sum up to 1.
    # to avoid invalid division (0/0), we smooth the intersection over union
    iou = (np.sum(intersection) + SMOOTH)/ (np.sum(union) + SMOOTH)

    return iou


def get_iou_score(mask, pred):
        """
        This method gets the intersection over union between the mask and prediction
        :params: the masks and predicted output
        :returns: iou_score
        """
        iou_score = round( get_iou(mask, pred),2 )
        return iou_score