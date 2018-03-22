import diaoyong
import cv2
from multiprocessing import  Process
from object_detection.utils import visualization_utils as vis_util
import  numpy as np
import  tensorflow as tf



def div(imge):
    dec = diaoyong.TOD()
    dec.detect(imge)



if __name__ == '__main__':

    imgg = cv2.imread('/home/yurunyang/Pictures/pic2.jpeg')
    div(imgg)
    while (1):
        pro = Process(target=(div), args=(imgg))
        pro.start()

