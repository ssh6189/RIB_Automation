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
0. 작성자 : 함종수

1. input 
 (1-1) source_img : raw_drawing(np)
 (1-2) yolo_img : image_for_yolo(np)
 (1-3) gujo_ocr_result_path : path of Gujo OCR result txt(str)
 (1-4) appended_vl, appended_hl : vertical lines and horizontal lines from line detection algorithm (list)

2. output 
 (2-1) scaling_result : result of calculation from scaling method (list) [symbol, length]

3. algorithm : matching texts to lines and predicting the length
'''
def scaling(source_img, yolo_img, yolo_result_path, gujo_ocr_result_path, appended_vl, appended_hl):
    
    roi_x = 4300 # 유저 입력으로 교체 필요.

    start = time.time() #코드 실행시간 측정을 위한 시작 시간 메모리

    path = 'C:/Users/CAI-Ham/Documents/T_in/ganseok/'

    result_dir = './scaling_results/'

    os.makedirs(result_dir, exist_ok=True) #결과 저장 디렉토리 생성

    bp_name = "blueprint"

    dst = source_img.copy()

    src = source_img.copy()



    ########## 검출 선 정제 ##########


    new_lines = [] # [[종류, 길이, 교점 간 중점]]


    cleared_appended_hl = []

    for lines in appended_hl:
        if lines not in cleared_appended_hl:
            cleared_appended_hl.append(lines)

    appended_hl = []
    appended_hl = cleared_appended_hl



    cleared_appended_vl = []

    for lines in appended_vl:
        if lines not in cleared_appended_vl:
            cleared_appended_vl.append(lines)

    appended_vl = []
    appended_vl = cleared_appended_vl



    lines = appended_hl + appended_vl

    for hl in appended_hl:
        new_lines.append(['p', abs(hl[0]-hl[2]), [int((hl[0]+hl[2])/2), int((hl[1]+hl[3])/2)]])
    for vl in appended_vl:
        new_lines.append(['v', abs(vl[1]-vl[3]), [int((vl[0]+vl[2])/2), int((vl[1]+vl[3])/2)]])




    ########### cross points & new lines ###########

    ###### 현재 가로선, 세로선으로 검출되는 것을 전제로 작성되어 있으므로 이후 개선 필요.

    cross_points = []

    # new_lines = [] # [[종류, 길이, 교점 간 중점]]
    cp_temp = []
    # new_lines => [p or v, length, [cx, cy], 텍스트 번호]


    cross_area = []
    cp_test = source_img.copy() ###

    for lh in appended_hl:  

        for lv in appended_vl:
            csx = max(lh[0], lv[0])
            csy = max(lh[1], lv[1])
            cex = min(lh[2], lv[2])
            cey = min(lh[3], lv[3])

            width = (cex - csx)
            height = (cey - csy)

            if (width>=0) and (height >=0):

                if width == lv[2] and height != lh[2]:
                    height = lh[2]        
                    csy = lh[1]
                    cey = lh[3]

                elif width != lv[2] and height == lh[2]:

                    width = lv[2]                
                    csx = lv[0]
                    cex = lv[2]


                cross_area.append([1, (csx+width/2)/dst.shape[1], (csy+height/2)/dst.shape[0], width/dst.shape[1], height/dst.shape[0]])
                
                cross_points.append([int(csx+width/2), int(csy+height/2)])
                cv2.line(dst, (int(csx+width/2), int(csy+height/2)), (int(csx+width/2), int(csy+height/2)), (0, 0, 255), 5) #debug
                
                cp_temp.append([int(csx+width/2), int(csy+height/2)])


        for cp_index, coord in enumerate(cp_temp):
            for cp_index_02 in range(cp_index + 1, len(cp_temp)):

                if abs(coord[0] - cp_temp[cp_index_02][0]) >= abs(coord[1] - cp_temp[cp_index_02][1]):
                    new_lines.append(['p', abs(coord[0] - cp_temp[cp_index_02][0]), [round((coord[0] + cp_temp[cp_index_02][0])/2), round((coord[1] + cp_temp[cp_index_02][1])/2)]])
                else:
                    new_lines.append(['v', abs(coord[1] - cp_temp[cp_index_02][1]), [round((coord[0] + cp_temp[cp_index_02][0])/2), round((coord[1] + cp_temp[cp_index_02][1])/2)]])

        cp_temp = []
        
    for lv in appended_vl:  

        for lh in appended_hl:
            csx = max(lh[0], lv[0])
            csy = max(lh[1], lv[1])
            cex = min(lh[2], lv[2])
            cey = min(lh[3], lv[3])

            width = (cex - csx)
            height = (cey - csy)

            if (width>=0) and (height >=0):

                if width == lv[2] and height != lh[2]:
                    height = lh[2]        
                    csy = lh[1]
                    cey = lh[3]

                elif width != lv[2] and height == lh[2]:

                    width = lv[2]                
                    csx = lv[0]
                    cex = lv[2]


                cross_area.append([1, (csx+width/2)/dst.shape[1], (csy+height/2)/dst.shape[0], width/dst.shape[1], height/dst.shape[0]])
                
                cross_points.append([int(csx+width/2), int(csy+height/2)])
                cv2.line(dst, (int(csx+width/2), int(csy+height/2)), (int(csx+width/2), int(csy+height/2)), (0, 0, 255), 5) #debug
                
                
                cp_temp.append([int(csx+width/2), int(csy+height/2)])


        for cp_index, coord in enumerate(cp_temp):
            for cp_index_02 in range(cp_index + 1, len(cp_temp)):

                if abs(coord[0] - cp_temp[cp_index_02][0]) >= abs(coord[1] - cp_temp[cp_index_02][1]):
                    new_lines.append(['p', abs(coord[0] - cp_temp[cp_index_02][0]), [round((coord[0] + cp_temp[cp_index_02][0])/2), round((coord[1] + cp_temp[cp_index_02][1])/2)]])
                else:
                    new_lines.append(['v', abs(coord[1] - cp_temp[cp_index_02][1]), [round((coord[0] + cp_temp[cp_index_02][0])/2), round((coord[1] + cp_temp[cp_index_02][1])/2)]])

        cp_temp = []



    cv2.imwrite(result_dir + bp_name + 'HoughP_cross.jpg', dst) #debug



    print("cp = ", len(cross_points))

    cleared_cp = []

    for cp in cross_points:
        if cp not in cleared_cp:
            cleared_cp.append(cp)

    print("cleared_cp =",len(cleared_cp))

    cross_points = []
    cross_points = cleared_cp





    test_dst = source_img.copy() #debug

    channel = [0, 0, 255] #debug

    os.makedirs(result_dir + bp_name + '_lines/' , exist_ok=True) #debug

    for nli, nl in enumerate(new_lines): #debug
           
        if nl[0] == 'p':
            cv2.line(test_dst, (nl[2][0]-int(nl[1]/2), nl[2][1]), (nl[2][0]+int(nl[1]/2), nl[2][1]), channel, 2)
          
        else:
            cv2.line(test_dst, (nl[2][0], nl[2][1]-int(nl[1]/2)), (nl[2][0], nl[2][1]+int(nl[1]/2)), channel, 2) 
            
            
    cv2.imwrite(result_dir + bp_name + '_lines/' + bp_name + '_lines_' + str(nli) + '.jpg', test_dst) #debug



    ########## numb & symb load from yolo result ##########

    text_loc = []  #[[수직or수평, 주길이, 중점좌표, 보조길이, 타입:numb or symb, 라벨]]
    classes_name = []
    labels = []


    full_filename = os.path.join(gujo_ocr_result_path) # dirname + "label/" : 라벨 디렉토리

    f = open(full_filename, 'r')
    labels = f.readlines()
    f.close()

    for data in labels:
        data = data.split()

        ht = source_img.shape[0]
        wt = source_img.shape[1]
        xc = float(data[1])
        yc = float(data[2])
        w = float(data[3])
        h = float(data[4])
        
        label_value = data[5]

        x1 = int(wt * xc - wt * w / 2)
        x2 = x1 + int(wt * w)
        y1 = int(ht * yc - ht * h / 2)
        y2 = y1 + int(ht * h)


        try:

            if (wt * w) >= (ht * h):
                text_loc.append(['p', int(wt*w), [int(wt*xc), int(ht*yc)], int(ht*h), 'numb', int(label_value)])
                                # [수직or수평, 주길이, 중점좌표, 보조길이, 숫자or부호, 라벨]
            else:
                text_loc.append(['v', int(ht*h), [int(wt*xc), int(ht*yc)], int(wt*w), 'numb', int(label_value)])

        except:

            if (wt * w) >= (ht * h):
                text_loc.append(['p', int(wt*w), [int(wt*xc), int(ht*yc)], int(ht*h), 'symb', label_value])
            else:
                text_loc.append(['v', int(ht*h), [int(wt*xc), int(ht*yc)], int(wt*w), 'symb', label_value])

                
        if "층" in label_value:
            floor = data[5][:-1]


    ########## text-line matching ##########


    text_match = []  # [[text_loc index, new_lines index]]
    text_temp = [len(src) + len(src[0]), -1]

    scale_list = []

    for tli in range(len(text_loc)):

        for nli in range(len(new_lines)):
            
            if new_lines[nli][0] == text_loc[tli][0]:
                if text_temp[0] != min(text_temp[0], math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))):
                    text_temp[0] = math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))
                    text_temp[1] = nli

                elif (text_temp[0] == math.sqrt(math.pow((text_loc[tli][2][0] - new_lines[nli][2][0]), 2) + math.pow((text_loc[tli][2][1] - new_lines[nli][2][1]), 2))) and (new_lines[nli][1] < new_lines[text_temp[1]][1]):
                    text_temp[1] = nli


        new_lines[text_temp[1]].append(tli)      # new_lines => [p or v, length, [cx, cy], 텍스트 번호]
        text_match.append([tli, text_temp[1]])     # [텍스트 번호, new_lines 번호]

        
        if text_loc[tli][4] == "numb":
            scale_list.append([text_loc[tli][5], new_lines[text_temp[1]][1]])

            
        text_temp = [len(src) + len(src[0]), -1]


    #         print("text matching... ", int(tli / len(text_loc) * 100), "% done   ")
        
    print(len(text_match))



    #[[수직or수평, 주길이, 중점좌표, 보조길이, 타입:numb or symb, 라벨]]

    test_dst = source_img.copy() #debug

    channel = [0, 0, 255] #debug

    os.makedirs(result_dir + bp_name , exist_ok=True) #debug

    for tmi, tm in enumerate(text_match): #debug
           
        if new_lines[tm[1]][0] == 'p':
            cv2.line(test_dst, (new_lines[tm[1]][2][0]-int(new_lines[tm[1]][1]/2), new_lines[tm[1]][2][1]), (new_lines[tm[1]][2][0]+int(new_lines[tm[1]][1]/2), new_lines[tm[1]][2][1]), channel, 2)
            if len(new_lines[tm[1]]) > 3:
                if text_loc[tm[0]][0] == 'p':
                    cv2.rectangle(test_dst, (int(text_loc[tm[0]][2][0]-text_loc[tm[0]][1]/2), int(text_loc[tm[0]][2][1]-text_loc[tm[0]][3]/2)), (int(text_loc[tm[0]][2][0]+text_loc[tm[0]][1]/2), int(text_loc[tm[0]][2][1]+text_loc[tm[0]][3]/2)), channel, 2)
                    cv2.putText(test_dst, text = str(text_loc[tm[0]][5]), org = (100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)
    #                 cv2.putText(image, text=text, org=(x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

                else :    
                    cv2.rectangle(test_dst, (int(text_loc[tm[0]][2][0]-text_loc[tm[0]][3]/2), int(text_loc[tm[0]][2][1]-text_loc[tm[0]][1]/2)), (int(text_loc[tm[0]][2][0]+text_loc[tm[0]][3]/2), int(text_loc[tm[0]][2][1]+text_loc[tm[0]][1]/2)), channel, 2)
                    cv2.putText(test_dst, text = str(text_loc[tm[0]][5]), org = (100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)

        else:
            cv2.line(test_dst, (new_lines[tm[1]][2][0], new_lines[tm[1]][2][1]-int(new_lines[tm[1]][1]/2)), (new_lines[tm[1]][2][0], new_lines[tm[1]][2][1]+int(new_lines[tm[1]][1]/2)), channel, 2)
            if len(new_lines[tm[1]]) > 3:
                if text_loc[tm[0]][0] == 'p':
                    cv2.rectangle(test_dst, (int(text_loc[tm[0]][2][0]-text_loc[tm[0]][1]/2), int(text_loc[tm[0]][2][1]-text_loc[tm[0]][3]/2)), (int(text_loc[tm[0]][2][0]+text_loc[tm[0]][1]/2), int(text_loc[tm[0]][2][1]+text_loc[tm[0]][3]/2)), channel, 2)
                    cv2.putText(test_dst, text = str(text_loc[tm[0]][5]), org = (100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)
                else :    
                    cv2.rectangle(test_dst, (int(text_loc[tm[0]][2][0]-text_loc[tm[0]][3]/2), int(text_loc[tm[0]][2][1]-text_loc[tm[0]][1]/2)), (int(text_loc[tm[0]][2][0]+text_loc[tm[0]][3]/2), int(text_loc[tm[0]][2][1]+text_loc[tm[0]][1]/2)), channel, 2)
                    cv2.putText(test_dst, text = str(text_loc[tm[0]][5]), org = (100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)

        cv2.imwrite(result_dir + bp_name + '/' + bp_name + '_textmatch_' + str(tmi) + '.jpg', test_dst)

                    
        test_dst = source_img.copy()

                    
            
    ########## scaling ##########

    real_length = np.array(scale_list)[:,0]
    drawing_length = np.array(scale_list)[:,1]
    scale_value = real_length / drawing_length

    h_list = []
    v_list = []

    for i in range(scale_value.shape[0]):
        # print(drawing_length[i], "\t", real_length[i], "\t", scale_value[i])
        
        if scale_value[i] > 8: ###### 유저 입력으로 바꿔야할 부분.
            h_list.append(scale_value[i])
        else:
            v_list.append(scale_value[i])


    scaling_result = []

    for tmi, tmv in enumerate(text_match):
        if text_loc[tmv[0]][4] == 'symb':
            if new_lines[tmv[1]][0] == 'p':
                scaling_result.append([text_loc[tmv[0]][5], new_lines[tmv[1]][1] * sum(h_list)/len(h_list)])
            if new_lines[tmv[1]][0] == 'v':
                scaling_result.append([text_loc[tmv[0]][5], new_lines[tmv[1]][1] * sum(h_list)/len(h_list)])
            

    # print(scaling_result)


    for sr in scaling_result:
        
        sr[0] = floor + sr[0]


    ########## 결과 pickle 저장 ##########


    # result_list = []

    # for sni, snv in enumerate(sn_match):

    #     result_list.append([text_loc[new_lines[snv[0]][3]][5][:-1], text_loc[new_lines[snv[1]][3]][5]])


    # with open(path + 'hough/' + bp_name + '/' + bp_name + 'result_.p', 'wb') as file_result:    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
    #     pickle.dump(result_list, file_result)

    # print(result_list)

    print("running time :", time.time() - start)  #실행시간 출력
    print('done')

    return scaling_result