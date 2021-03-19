# Interpreting drawings with CAI-LAB & t-in Robotics
# CODE : gujo Analysis -> bujae Analysis -> Calculate Number of ribs

# import gujo Analysis code
from gujo_YOLO import detect_gujo, rotate_img
from gujo_OCR import demo_gujo
from gujo_line_detection import line_detection
from gujo_Scaling import scaling
from gujo_Grouping import grouping, txt_combine
from gujo_resize_img import resize_img

# import bujae Analysis code
from bujae_cell_cluster import img_preprocess, clustering
from bujae_YOLO import detect
from bujae_OCR import demo
from bujae_function import crop, remove_tmp_txt
from bujae_combine import info_combination
from sklearn.cluster import KMeans

# import caluculate code
from stirrub_calculator import stirrub_calculator

import math
import random
import os
import numpy as np
import cv2
import time
import copy
import matplotlib.pyplot as plt

import string
import argparse
import pickle

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F


def main_analisys(bujae, gujo):
    print(bujae)
    print(gujo)
    ##### 0-1. Input Parameter (GUJO) #######################################
    ### YOLO 
    # yolo weight 파일 경로
    weights_gujo = "YOLO_saved_models/twin_gujo_0217/weights/best.pt"

    # 도면 이미지 폴더 경로 
    source_gujo = "data_gujo/test/"
    source_origin_gujo = gujo + "/"

    # 결과 저장 폴더 경로 (이미지 & 텍스트 파일)
    out_gujo = "result_yolo_gujo/test/"
    txt_out_gujo = "result_gujo/txt_gujo/"

    ### OCR 
    # ocr weight 파일 경로
    weights_gujo_ocr = "OCR_saved_models/0304/best_accuracy.pth"

    Trans = "None"
    Feat = "ResNet"
    Seq = "None"
    Predict = "Attn"

    ### Combine 
    outfile_name_g = "gujo_results.txt"
    line_txt_name_g = 'yolo_result_pixel.txt'
    final_pickle_dir_g = 'result_gujo/ham_gujo_result.p'

    ### 0-2. input parameter (BUJAE) ########################################
    ### Cluster 
    input_path = bujae + "/"# bujae_list's img
    path_cluster = "result_bujae/result_bujae_cluster/" # cluster save dir

    ### YOLOv5 (Text Detection) 
    weights = "YOLO_saved_models/twin_bujae_v5m_20210201/weights/best.pt" # YOLO weight's dir 
    img_out = "result_bujae/result_bujae_yolo/img/" # YOLO's result (img)
    txt_out = "result_bujae/result_bujae_yolo/txt/" # YOLO's result (txt : class, cf_score, x_min, y_min, x_max, y_max (pixel value))

    ### YOLO's img crop
    yolo_result_txt = "result_bujae/result_bujae_yolo/txt/yolo_result.txt" # YOLO's txt result dir
    SAVE_PATH = "result_bujae/result_bujae_yolo/img_crop/" # crop img's save dir (by YOLOv5)

    ### OCR (Text Recogntion, NAVER)
    save_image_folder_path = "result_bujae/result_bujae_ocr/img_ocr/" # ocr result img's save dir

    ### Final Combine 
    final_pickle_dir = 'result_bujae/ham_bujae_result.p'
    
    #### 1. GUJO Flan Analyisy ##############################################
    print("GUJO Analysis Start")
    # Temp Txt File Remove
    remove_tmp_txt(txt_out_gujo) 

    resize_img(source_origin_gujo, source_gujo, 1280)

    # load gujo img (by openCV)
    origin_img = []
    img_list_sh = os.listdir(source_origin_gujo)

    for i, name in enumerate(img_list_sh):
        tmp_img = cv2.imread(source_origin_gujo + name)
        origin_img.append(tmp_img)

    # detect text for gujo (YOLO) 
    with torch.no_grad():
        img_origin_yolo = detect_gujo(weights_gujo, source_gujo, out_gujo, txt_out_gujo)

    # Rotate Vertical Image
    rotate_img(out_gujo)

    # recogntion text for gujo (OCR)
    tmp_image_folder_path = out_gujo
    image_folder_path = tmp_image_folder_path
    txt_gujo_path = txt_out_gujo

    cudnn.benchmark = True
    cudnn.deterministic = True
    num_gpu = torch.cuda.device_count()

    demo_gujo(weights_gujo_ocr, txt_gujo_path, tmp_image_folder_path, image_folder_path)

    # combine yolo & ocr txt
    directory = txt_out_gujo
    txt_combine(directory, outfile_name_g)

    # load origin gujo img
    origin_img = np.array(origin_img)
    img_origin_yolo = np.array(img_origin_yolo)

    img_origin_yolo = img_origin_yolo[0]
    origin_img  = origin_img[0]

    yolo_result_path = txt_out_gujo
    txt_name = line_txt_name_g

    # line detect
    appended_vl, appended_hl = line_detection(yolo_result_path, txt_name, origin_img, img_origin_yolo)

    # scaling by ham    
    scaling_result_g = scaling(origin_img, img_origin_yolo, yolo_result_path , directory+outfile_name_g, appended_vl, appended_hl)

    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
    with open(final_pickle_dir_g, 'wb') as file_result_g:
        pickle.dump(scaling_result_g, file_result_g)

    print("GUJO Analysis Finish")

    #### 2. Bujae LIST Analyisy ##############################################
    print("BUJAE Analysis Start")

    # Temp Txt File Remove
    remove_tmp_txt(txt_out)

    # load bujae img (by openCV)
    input_list = os.listdir(input_path)

    for img in input_list:
        tmp_img_name = img[:-4]
        tmp_img = input_path + img
        input = cv2.imread(tmp_img)

        # Image Pre-Processiing 
        blur_img = img_preprocess(input)
        
        # k-means clustering
        clustering(prerocess_img = blur_img, 
            origin_img = input, 
            img_name = tmp_img_name,
            save_path = path_cluster,
            show_graph = False)

    source_yolo = path_cluster
    with torch.no_grad():
        # 글자 검출 (YOLO)
        detect(weights, source_yolo, img_out, txt_out)

    # 글자 영역 crop
    source = path_cluster
    crop(yolo_result_txt, source, SAVE_PATH)

    cudnn.benchmark = True
    cudnn.deterministic = True
    num_gpu = torch.cuda.device_count()

    saved_model_path = weights_gujo_ocr
    image_folder_path = SAVE_PATH
    tmp_image_folder_path = SAVE_PATH

    # 글자 인식 (OCR)
    demo(saved_model_path, save_image_folder_path, image_folder_path, tmp_image_folder_path)  

    # 정보 통합
    info_combination(save_image_folder_path,final_pickle_dir)

    print("BUJAE Analysis Finish")

    #### 3. Final Caluclate #################################################
    print("Final Caluclate Start")

    final_result = stirrub_calculator()
    #stirrub_calculator()

    print("Final Caluclate Finish")

    return final_result
