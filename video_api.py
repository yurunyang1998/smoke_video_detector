import tensorflow as tf

import diaoyong
import cv2
from multiprocessing import  Process,Queue,Lock
from object_detection.utils import visualization_utils as vis_util
import  numpy as np



video_path = '/home/yurunyang/Downloads/CottonSmoke.avi'
path2 = '/home/yurunyang/Downloads/white smoke far.avi'

frame_array = []    #size =300

lock = Lock()
q = Queue(2)

dec_a = diaoyong.TOD()
global a
a=0

def single_dec(image):

    try:
        lock.acquire()
        #global a

        #print(q, 2)

        dec_b = diaoyong.TOD()

        [boxes, scores, classes] = dec_b.detect(image)
        print(np.squeeze(scores)[0])
        q.put([boxes, scores, classes])
        a = 0
        lock.release()
    except Exception as e:
        print(e)

# 很好，我不会！！
# 拜拜，我撤了。贼饿。。



if __name__ == '__main__':


    count =0

    cv2.namedWindow("capture",0)
    cv2.resizeWindow("capture",500,500)
    cap = cv2.VideoCapture(path2)
    fps = cv2.CAP_PROP_FPS



    #wait = int(1 / fps * 1000 / 1)
    while (1):
        # get a frame
        count = count +1
        for i in range(500):
            ret, frame = cap.read()
            frame_array.append(frame)
        frame_array.reverse()

        for i in range(len(frame_array)):

            if(len(frame_array)>0):

                if(i%5==0):

                        pro = Process(target=single_dec,args=[frame_array.pop()])
                        pro.start()
                        #pro.join()



                else:
                    #print("in main queue size is",q.qsize())
                    if(q.full()):
                        #print(q.get())
                        boxes, scores, classes =q.get()
                        #print(boxes,scores,classes)
                        now_img = frame_array.pop()
                        vis_util.visualize_boxes_and_labels_on_image_array(
                            now_img,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            dec_a.category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)

                        cv2.imshow("capture",now_img)
                        cv2.waitKey(55)

                        pro2 = Process(target=single_dec, args=[frame_array.pop()])
                        pro2.start()

                        for a in range(15):
                            if (len(frame_array)>0):
                                second_img = frame_array.pop()
                                vis_util.visualize_boxes_and_labels_on_image_array(
                                    second_img,
                                    np.squeeze(boxes),
                                    np.squeeze(classes).astype(np.int32),
                                    np.squeeze(scores),
                                    dec_a.category_index,
                                    use_normalized_coordinates=True,
                                    line_thickness=8)
                                # print(i)
                                cv2.imshow("capture", second_img)
                                cv2.waitKey(55)
                            else:
                                break


                    else:
                        cv2.imshow("capture",frame_array.pop())
                        cv2.waitKey(55)

            else:
                break




        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()