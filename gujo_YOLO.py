# CODE : Detect Gujo Plan's text by YOLOv5m (version 5-medium)
# DATE : 2021-03-09 (by SH)
# INPUT : Gujo Plan (JPG, resize 1280 pixel)
# OUTPUT : Text Area's txt file (class(0), cf_score, x_center(pixel value & normalize 0~1), y_center, width, height)

import argparse
import time
import os
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from YOLO_utils.datasets import LoadStreams, LoadImages
from YOLO_utils.general import check_img_size, check_requirements, non_max_suppression, apply_classifier, scale_coords, \
    xyxy2xywh, strip_optimizer, set_logging, increment_path
from YOLO_utils.plots import plot_one_box
from YOLO_utils.torch_utils import select_device, load_classifier, time_synchronized


'''
0. 작성자 : 유승환

1. input 
 (1-1) out_gujo : YOLO crop img's dir

2. output 
 (2-1) dst_1 : Vertical img

3. algorithm : rotate Horizontal(가로) img -> Vertical(세로) img
'''
def rotate_img(out_gujo):
    yolo_img_list = os.listdir(out_gujo)
    # print(yolo_img_list)

    # Load Img
    for i in range(len(yolo_img_list)):
        img_name = yolo_img_list[i]
        src_1 = cv2.imread(out_gujo+img_name, cv2.IMREAD_COLOR)
        height, width, channel = src_1.shape

        # If Vertical Image -> Rotate
        if height > width:
            dst_1 = cv2.rotate(src_1, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(out_gujo + img_name, dst_1)

'''
0. 작성자 : 유승환

1. input 
 (1-1) weights_gujo : YOLOv5's weight file dir
 (1-2) source_gujo : Gujo Plan's img (resize 1280)
 (1-3) out_gujo : crop txt img's dir
 (1-4) txt_out_gujo : save txt result's dir

2. output 
 (2-1) yolo_result.txt : text detect results with normalize 0~1 (class, cf_score, bbox_x_center, y_center, width, height)
 (2-2) yolo_result_pixel.txt : text detect results with pixel value (class, x_min, y_min, x_max, y_max)

3. algorithm : detect txt by YOLOv5
'''
def detect_gujo(weights_gujo, source_gujo, out_gujo, txt_out_gujo):
    ### input parameter for yolo ##############################################
    img_size = 1280  # input img size
    conf_thres = 0.5 # class_threshold
    iou_thres = 0.5 # iou_threshold
    save_img = True
    save_txt = True # save yolo result txt file
    ###########################################################################

    # Directories
    save_dir = out_gujo  # increment run
    
    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights_gujo, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(img_size, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    vid_path, vid_writer = None, None
    dataset = LoadImages(source_gujo, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    img_origin_yolo = []
    for path, img, im0s, vid_cap in dataset:
        img_origin_yolo.append(im0s)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=None)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=None)
        t2 = time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(Path(out_gujo) / Path(p).name)
            txt_path = txt_out_gujo

            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                k = 0 # world_num

                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        # line = (cls, *xywh, conf) # label format
                        line = (cls, *xywh) # label format

                        dst = im0.copy()
                        dst = im0[int(xyxy[1]):int(xyxy[3]), int(xyxy[0]):int(xyxy[2])] # y_min, y_max, x_min, x_max
                        cv2.imwrite(save_path[:-4] + "_" + str(k) + save_path[-4:], dst) 

                        # yolo result (text area (normalize 0~1))
                        with open(txt_path + 'yolo_result.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        # yolo result (text area (pixel value) & don't write cf_score )
                        with open(txt_path + 'yolo_result_pixel.txt', 'a') as f:
                            f.write(('%g %s %s %s %s' + '\n') % (cls, int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])))  # label format
                            
                    k = k + 1

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        
            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')

    print(f'Done. ({time.time() - t0:.3f}s)')

    return img_origin_yolo