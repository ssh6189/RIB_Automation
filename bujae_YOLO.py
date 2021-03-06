# CODE : Detect bujae list text by YOLOv5m (version 5-medium)
# DATE : 2021-03-09 (by SH)
# INPUT : bujae list's cluster img (JPG)
# OUTPUT : Text Area's txt file (class(0), cf_score, x_center(pixel value), y_center, width, height)

import argparse
import time
from pathlib import Path

import platform
import shutil

import os
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
 (1-1) weights : YOLOv5's weight file dir
 (1-2) source_yolo : clustering imgs dir
 (1-3) img_out : save img's dir
 (1-4) txt_out : save txt result's dir

2. output 
 (2-1) yolo_result.txt : text detect results (class, cf_score, bbox_x_center, y_center, width, height(pixel value))

3. algorithm : detect txt by YOLOv5
'''
def detect(weights, source_yolo, img_out, txt_out):
    ### input parameter for yolo ##############################################
    img_size = 640  # input img size
    conf_thres = 0.6 # class_threshold
    iou_thres = 0.5 # iou_threshold
    save_txt = True # save yolo result txt file
    ###########################################################################

    # Directories
    save_dir = img_out  # increment run

    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(img_size, s=stride)  # check img_size

    if half:
        model.half()  # to FP16
    
    # Set Dataloader
    vid_path, vid_writer = None, None
    dataset = LoadImages(source_yolo, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)
        t2 = time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(Path(img_out) / Path(p).name)
            txt_path = txt_out

            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()  # not normalized xywh
                        line = (cls, conf, *xywh)

                        # bbox (pixel)
                        with open(txt_path + 'yolo_result.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                # 이미지 구분하기
                with open(txt_path + 'yolo_result.txt', 'a') as f:
                    f.write('###\n')

            print("\n")