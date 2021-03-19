import os
import cv2


def resize_img(input_path, save_path, resize):

    # load img list
    img_list = os.listdir(input_path)

    # read & resize img
    for i in range(len(os.listdir(input_path))):
        img = cv2.imread(input_path + img_list[i], cv2.IMREAD_COLOR)
        print(img)
        height, width, channel = img.shape
        height_ratio = round(height/resize, 3)
        width_ratio = round(width/resize, 3)
        dst = cv2.resize(img, dsize=(resize, resize), interpolation=cv2.INTER_AREA)
        cv2.imwrite(save_path + str(height_ratio) + "_" + str(width_ratio) + "_" + img_list[i], dst)
