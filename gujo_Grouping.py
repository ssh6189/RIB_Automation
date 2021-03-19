############ Grouping ############

import cv2
import numpy as np
import os
import math
import time
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random
import pickle


'''
1. input 
 (1-1) directory : yolo & ocr txt dir (for gujo)
 (1-2) outfile_name : combine txt name

2. output 
 (2-1) out_file : combine yolo & ocr txt (= algorithm)

'''
def txt_combine(directory, outfile_name):
    files = os.listdir(directory)
    text_list = []

    # Load YOLO & OCR Txt
    for filename in files:

        if ".txt" not in filename:
            continue

        file = open(directory + filename)
        temp_text_list = []

        for line in file:
            temp_text_list.append(line[:-2])

        text_list.append(temp_text_list)

    # Open Final Txt
    out_file = open(directory + outfile_name, 'w+t')

    # Make Final Txt
    for i in range(0, len(text_list[0])):
        data = text_list[1][i] + " " + text_list[0][i] + "\n"
        out_file.write(data)

    out_file.close()


'''
0. 작성자 : 함종수

1. input 
 (1-1) source_img : 
 (1-2) yolo_ocr_results : 

2. output 
 (2-1) grouping_result.p : 

3. algorithm : 
'''
def grouping(source_img, yolo_ocr_results):
    
    path = './'

    result_dir = 'mrg_grp/'
    
    
    os.makedirs(path + result_dir, exist_ok=True) #결과 저장 디렉토리 생성


    # src = cv2.imread(path + bp_name + '.jpg')
    src = cv2.imread(source_img)
    dst = src.copy()
    dst_line = dst.copy()
    dst_dash = dst.copy()

    cv2.imwrite(path + result_dir + '_original.jpg', src)

    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path + result_dir + '_gray.jpg', gray)

    #     kernel = cv2.getStructuringElement(cv2.MORPH_ERODE , (3, 3))
    #     gray = cv2.morphologyEx(gray, cv2.MORPH_HITMISS, kernel, iterations=3)
    #     cv2.imwrite(path + 'hough/' + bp_name + '_morph.jpg', gray)

    ret, gray_bin = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    gray = gray_bin
    cv2.imwrite(path + result_dir + '_bin.jpg', gray)


    ########## numb & symb load ##########

    text_loc = []  #[[수직or수평, 주길이, 중점좌표, 보조길이, 타입:numb or symb, 라벨]]
    classes_name = []
    labels = []

    full_filename = yolo_ocr_results # dirname + "label/" : 라벨 디렉토리

    f = open(full_filename, 'r')
    labels = f.readlines()
    f.close()

    for data in labels:
        data = data.split()

        ht = len(src)
        wt = len(src[0])
        xc = float(data[1])
        yc = float(data[2])
        w = float(data[3])
        h = float(data[4])
        classes_name.append(data[5])

        x1 = int(wt * xc - wt * w / 2)
        x2 = x1 + int(wt * w)
        y1 = int(ht * yc - ht * h / 2)
        y2 = y1 + int(ht * h)


        gray[y1:y2, x1:x2] = 255  


        try:

            if (wt * w) >= (ht * h):
                text_loc.append(['p', int(wt*w), [int(wt*xc), int(ht*yc)], int(ht*h), 'numb', int(data[5])])
                                # [수직or수평, 주길이, 중점좌표, 보조길이, 숫자or부호, 라벨]
            else:
                text_loc.append(['v', int(ht*h), [int(wt*xc), int(ht*yc)], int(wt*w), 'numb', int(data[5])])

        except:

            if (wt * w) >= (ht * h):
                text_loc.append(['p', int(wt*w), [int(wt*xc), int(ht*yc)], int(ht*h), 'symb', data[5]])
            else:
                text_loc.append(['v', int(ht*h), [int(wt*xc), int(ht*yc)], int(wt*w), 'symb', data[5]])




    ########### 교점 검출 ############


    cross_points = []

    mask = [[255, 255], [255, 255]]
    filter = [ [[0, 255],[255, 255]], [[255, 0],[255, 255]], [[255, 255],[0, 255]], [[255, 255],[255, 0]],
              [[0, 0],[0, 255]], [[0, 0],[255, 0]], [[0, 255],[0, 0]], [[255, 0],[0, 0]] ]

    for j, row in enumerate(gray):
        for i, channel in enumerate(row):

            try:
                mask[0][0] = gray[j, i]
                mask[0][1] = gray[j, i+1]
                mask[1][0] = gray[j+1, i]
                mask[1][1] = gray[j+1, i+1]

                if mask == [[0, 0], [0, 255]]:
                    cross_points.append([i, j])
                elif mask == [[0, 0], [255, 0]]:
                    cross_points.append([i+1, j])
                elif mask == [[0, 255], [0, 0]]:
                    cross_points.append([i, j+1])
                elif mask == [[255, 0], [0, 0]]:
                    cross_points.append([i+1, j+1])                

            except:
                pass


    for [x, y] in cross_points:
        cv2.line(dst, (x, y), (x, y), (0, 0, 255), 3)



    ########### new lines ###########


    new_lines = [] # [[종류, 길이, [cx, cy], text_loc index]]

    for cp_i, cp_v in enumerate(cross_points):
        for cp_i2, cp_v2 in enumerate(cross_points):

            if cp_v[1] == cp_v2[1]:
                new_lines.append(['p', abs(cp_v[0] - cp_v2[0]), [round((cp_v[0] + cp_v2[0])/2), round((cp_v[1] + cp_v2[1])/2)]])
            elif cp_v[0] == cp_v2[0]:
                new_lines.append(['v', abs(cp_v[1] - cp_v2[1]), [round((cp_v[0] + cp_v2[0])/2), round((cp_v[1] + cp_v2[1])/2)]])

        cp_temp = []


    ########## text-line matching ##########

    # print("!!!!!!!!!!!!!!!! debug !!!!!!!!!!!!!!")

    # print(src.shape, len(new_lines))

    text_match = []  # [[text_loc index, new_lines index]]
    text_temp = [len(src) + len(src[0]), -1]

    for tli in range(len(text_loc)):

        for nli in range(len(new_lines)):
            if text_temp[0] != min(text_temp[0], math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))):
                text_temp[0] = math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))
                text_temp[1] = nli

            elif (text_temp[0] == math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))) and (new_lines[nli][1] < new_lines[text_temp[1]][1]):
                text_temp[1] = nli

        # print(text_temp)

        new_lines[text_temp[1]].append(tli)      # new_lines => [p or v, length, [cx, cy], 텍스트 번호]
        text_match.append([tli, text_temp[1]])     # [텍스트 번호, new_lines 번호]

        text_temp = [len(src) + len(src[0]), -1]



    ########## new numbers ############

    new_numb_margin = 5  ## 유저 param

    numb_sum_temp = []
    new_numb_check = []
    new_numb_img = src.copy()

    for nli, nlv in enumerate(new_lines):
        if len(nlv) < 4:
            for nli2, nlv2 in enumerate(new_lines):
                if len(nlv2) > 3 and (text_loc[nlv2[3]][4] == 'numb') and (nli2 not in new_numb_check):
                    if (nlv2[0] == nlv[0]) and (nlv2[1] < nlv[1]):
                        if (nlv[0] == 'p') and (abs(nlv2[2][1]-nlv[2][1]) <= new_numb_margin) and ((nlv[2][0]-(nlv[1]/2)) < nlv2[2][0]) and (nlv2[2][0] < (nlv[2][0]+(nlv[1]/2))):
                            numb_sum_temp.append(text_loc[nlv2[3]][5])


                        elif (nlv[0] == 'v') and (abs(nlv2[2][0]-nlv[2][0]) <= new_numb_margin) and ((nlv[2][1]-(nlv[1]/2)) < nlv2[2][1]) and (nlv2[2][1] < (nlv[2][1]+(nlv[1]/2))):
                            numb_sum_temp.append(text_loc[nlv2[3]][5])



            # [수직or수평, 주길이, 중점좌표, 보조길이, 숫자or부호, 라벨]

            if len(numb_sum_temp) >= 2:
                text_loc.append([nlv[0], 70, [nlv[2][0],nlv[2][1]], 20, 'numb', sum(numb_sum_temp)])
                new_lines[nli].append(len(text_loc)-1)
                text_match.append([len(text_loc)-1, nli])

                new_numb_check.append(nli)

                cv2.putText(new_numb_img, str(sum(numb_sum_temp)), (nlv[2][0],nlv[2][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))



        numb_sum_temp = []



    ########### numb -symb matching ############

    sn_match = [] # [[new_lines index of 부호, new_lines index of 수치]]
    sn_temp = [len(src) + len(src[0]), -1, len(src) + len(src[0]), (len(src) + len(src[0]))*2] #[거리, 매칭 번호, 길이차, 거리 + 길이차]

    for tli, tlv in enumerate(text_loc):

        if tlv[4] == 'symb':

            nln_s = text_match[tli][1] # new_lines에서 현재 해당 부호선의 번호

            for tli2, tlv2 in enumerate(text_loc):

                nln_n = text_match[tli2][1] # new_lines에서 현재 해당 수치선의 번호

                if (tlv2[4] == 'numb') and (new_lines[nln_s][0] == new_lines[nln_n][0]):

                    if new_lines[nln_s][0] == 'p' and (sn_temp[3] != min(sn_temp[3],( math.sqrt(math.pow((new_lines[nln_s][2][0] - new_lines[nln_n][2][0]), 2)) + abs(new_lines[nln_s][1]- new_lines[nln_n][1]) ))):
                        sn_temp[0] = math.sqrt(math.pow((new_lines[nln_s][2][0] - new_lines[nln_n][2][0]), 2))
                        sn_temp[1] = nln_n
                        sn_temp[2] = abs(new_lines[nln_s][1]- new_lines[nln_n][1])
                        sn_temp[3] = sn_temp[0] + sn_temp[2]

                    elif new_lines[nln_s][0] == 'v' and (sn_temp[3] != min(sn_temp[3],( math.sqrt(math.pow((new_lines[nln_s][2][1] - new_lines[nln_n][2][1]), 2)) + abs(new_lines[nln_s][1]- new_lines[nln_n][1]) ))):
                        sn_temp[0] = math.sqrt(math.pow((new_lines[nln_s][2][1] - new_lines[nln_n][2][1]), 2))
                        sn_temp[1] = nln_n
                        sn_temp[2] = abs(new_lines[nln_s][1]- new_lines[nln_n][1])
                        sn_temp[3] = sn_temp[0] + sn_temp[2]

            sn_match.append([nln_s, sn_temp[1]])
            sn_temp = [len(src) + len(src[0]), -1, len(src) + len(src[0]), (len(src) + len(src[0]))*2] #[거리, 매칭 번호, 길이차, 거리 + 길이차]


    ########### grouping ############


        #### 자기 자신 포함 안 되는 버그 존재!!! => 현재 수정했으나 확인 필요.

    line_match = []
    group_temp = []
    group_check = []
    length_gap = 0
    cp_gap = 0

    for m_i in range(len(new_lines)):
        if m_i not in group_check:

            for m_i_next in range(m_i + 1, len(new_lines)):
                if (new_lines[m_i][0] == new_lines[m_i_next][0]):
                    if new_lines[m_i][0] == 'p' and abs(new_lines[m_i][1] - new_lines[m_i_next][1]) <= length_gap and abs(new_lines[m_i][2][0] - new_lines[m_i_next][2][0]) <= cp_gap:
                        group_temp.append(m_i_next)
                        group_check.append(m_i_next)
                    elif new_lines[m_i][0] == 'v' and abs(new_lines[m_i][1] - new_lines[m_i_next][1]) <= length_gap and abs(new_lines[m_i][2][1] - new_lines[m_i_next][2][1]) <= cp_gap:
                        group_temp.append(m_i_next)
                        group_check.append(m_i_next)

        if group_temp != []:
            group_temp.append(m_i)
            line_match.append(group_temp)
            group_temp = []    




    ########### 그룹 표시 _ 각 그룹별로 이미지 저장 _ symb-numb ############

    dst = src.copy()
    # dst = new_numb_img.copy()

    channel = [0, 0, 255]


    for sn_i, sn_v in enumerate(sn_match):
        if ('g' in text_loc[new_lines[sn_v[0]][3]][5]) or ('b' in text_loc[new_lines[sn_v[0]][3]][5]):

            for lm_v in line_match :
                if (sn_v[0] in lm_v) or (sn_v[1] in lm_v):
                    for nl_number in lm_v:
                        if new_lines[nl_number][0] == 'p':
                            cv2.line(dst, (new_lines[nl_number][2][0]-int(new_lines[nl_number][1]/2), new_lines[nl_number][2][1]), (new_lines[nl_number][2][0]+int(new_lines[nl_number][1]/2), new_lines[nl_number][2][1]), channel, 2)
                            if len(new_lines[nl_number]) > 3:
                                if text_loc[new_lines[nl_number][3]][0] == 'p':
                                    cv2.rectangle(dst, (int(text_loc[new_lines[nl_number][3]][2][0]-text_loc[new_lines[nl_number][3]][1]/2), int(text_loc[new_lines[nl_number][3]][2][1]-text_loc[new_lines[nl_number][3]][3]/2)), (int(text_loc[new_lines[nl_number][3]][2][0]+text_loc[new_lines[nl_number][3]][1]/2), int(text_loc[new_lines[nl_number][3]][2][1]+text_loc[new_lines[nl_number][3]][3]/2)), channel, 2)
                                else :    
                                    cv2.rectangle(dst, (int(text_loc[new_lines[nl_number][3]][2][0]-text_loc[new_lines[nl_number][3]][3]/2), int(text_loc[new_lines[nl_number][3]][2][1]-text_loc[new_lines[nl_number][3]][1]/2)), (int(text_loc[new_lines[nl_number][3]][2][0]+text_loc[new_lines[nl_number][3]][3]/2), int(text_loc[new_lines[nl_number][3]][2][1]+text_loc[new_lines[nl_number][3]][1]/2)), channel, 2)

                        else:
                            cv2.line(dst, (new_lines[nl_number][2][0], new_lines[nl_number][2][1]-int(new_lines[nl_number][1]/2)), (new_lines[nl_number][2][0], new_lines[nl_number][2][1]+int(new_lines[nl_number][1]/2)), channel, 2)
                            if len(new_lines[nl_number]) > 3:
                                if text_loc[new_lines[nl_number][3]][0] == 'p':
                                    cv2.rectangle(dst, (int(text_loc[new_lines[nl_number][3]][2][0]-text_loc[new_lines[nl_number][3]][1]/2), int(text_loc[new_lines[nl_number][3]][2][1]-text_loc[new_lines[nl_number][3]][3]/2)), (int(text_loc[new_lines[nl_number][3]][2][0]+text_loc[new_lines[nl_number][3]][1]/2), int(text_loc[new_lines[nl_number][3]][2][1]+text_loc[new_lines[nl_number][3]][3]/2)), channel, 2)
                                else :    
                                    cv2.rectangle(dst, (int(text_loc[new_lines[nl_number][3]][2][0]-text_loc[new_lines[nl_number][3]][3]/2), int(text_loc[new_lines[nl_number][3]][2][1]-text_loc[new_lines[nl_number][3]][1]/2)), (int(text_loc[new_lines[nl_number][3]][2][0]+text_loc[new_lines[nl_number][3]][3]/2), int(text_loc[new_lines[nl_number][3]][2][1]+text_loc[new_lines[nl_number][3]][1]/2)), channel, 2)


            cv2.imwrite(path + result_dir + '_textmatch_' + str(sn_i) + '.jpg', dst)

        dst = src.copy()


    ########## 결과 pickle 저장 ##########


    result_list = []

    for sni, snv in enumerate(sn_match):

        result_list.append([text_loc[new_lines[snv[0]][3]][5], text_loc[new_lines[snv[1]][3]][5]])


    with open(path + result_dir + '/' + 'grouping_result.p', 'wb') as file_result:    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
        pickle.dump(result_list, file_result)

    print(result_list)