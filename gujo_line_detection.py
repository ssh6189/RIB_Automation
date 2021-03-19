import numpy as np
import cv2
import math

from gujo_line_algorithm import gradient_calc, line_sum, yolo_text_box_to_list, draw_line, draw_box
from operator import itemgetter

import os
import time


'''
0. 작성자 : 이호준

1. input 
 (1-1) input_line : 허프변환을 통해 검출된 선 집합 리스트
 (1-2) redundancy : 선의 양 끝점을 기준으로 해당 값의 픽셀 이내에 다른 선이 있으면 연결 (정수)

2. output 
 (2-1) appended_vl : 조각난 선들을 연결한 선분의 집합

3. algorithm
 (3-1) 입력으로 받은 선을 순환하며 해당 선으로부터 redundancy 만큼의 범위 내에 포함되는 선들을 모두 추출 후 그 집합 안의 선중 최소 x,y값과 최대 x,y 값을 선정하여 하나의 선으로 반환
 (3-2) 입력받은 선과 결과로 나온 선의 집합이 일치할때까지 재귀함수 호출
'''

### 세로 가로 선 별로 돌면서 각 선의 x 좌표 +-2픽셀 y 좌표 +-2픽셀안에 겹치는 구간이 있는 선을 하나로 합치기
appended_vl = []

def connect_vl(input_line, redundancy):
    append_line = []
    for i in range(len(input_line)):
        base_box_min_x = int(input_line[i][0]) - redundancy
        base_box_min_y = int(input_line[i][1]) - redundancy
        base_box_max_x = int(input_line[i][2]) + redundancy
        base_box_max_y = int(input_line[i][3]) + redundancy
        iou_detected = [input_line[i]]
        for j in range(len(input_line)):
            if j == i:
                continue
            compare_box_min_x = int(input_line[j][0]) - redundancy
            compare_box_min_y = int(input_line[j][1]) - redundancy
            compare_box_max_x = int(input_line[j][2]) + redundancy
            compare_box_max_y = int(input_line[j][3]) + redundancy

            x1 = max(base_box_min_x, compare_box_min_x)
            y1 = max(base_box_min_y, compare_box_min_y)
            x2 = min(base_box_max_x, compare_box_max_x)
            y2 = min(base_box_max_y, compare_box_max_y)
            if x2 - x1 > 0 and y2 - y1 > 0:
                iou_detected.append(input_line[j])
        if len(iou_detected) > 1:
            iou_detected = sorted(iou_detected, key=itemgetter(0))
            new_x1 = iou_detected[0][0]
            iou_detected = sorted(iou_detected, key=itemgetter(1))
            new_y1 = iou_detected[0][1]
            iou_detected = sorted(iou_detected, key=itemgetter(2), reverse=True)
            new_x2 = iou_detected[0][2]
            iou_detected = sorted(iou_detected, key=itemgetter(3), reverse=True)
            new_y2 = iou_detected[0][3]
            if not new_x2 - new_x1 == 0:
                if (float(abs(new_y2 - new_y1)) / float(abs(new_x2 - new_x1))) > 0.5:
                    append_line.append([new_x1, new_y1, new_x1, new_y2])
                else:
                    append_line.append([new_x1, new_y1, new_x2, new_y1])
            else:
                append_line.append([new_x1, new_y1, new_x1, new_y2])
        else:
            append_line.append(input_line[i])
    if append_line != input_line:
        connect_vl(append_line, redundancy)
    else:
        global appended_vl
        appended_vl = append_line.copy()


'''
0. 작성자 : 이호준

1. input 
 (1-1) input_line : 허프변환을 통해 검출된 선 집합 리스트
 (1-2) redundancy : 선의 양 끝점을 기준으로 해당 값의 픽셀 이내에 다른 선이 있으면 연결 (정수)

2. output 
 (2-1) appended_hl : 조각난 선들을 연결한 선분의 집합

3. algorithm : 
'''
appended_hl = []
def connect_hl(input_line, redundancy):
    append_line = []
    for i in range(len(input_line)):
        base_box_min_x = int(input_line[i][0]) - redundancy
        base_box_min_y = int(input_line[i][1]) - redundancy
        base_box_max_x = int(input_line[i][2]) + redundancy
        base_box_max_y = int(input_line[i][3]) + redundancy
        iou_detected = [input_line[i]]
        for j in range(len(input_line)):
            if j == i:
                continue
            compare_box_min_x = int(input_line[j][0]) - redundancy
            compare_box_min_y = int(input_line[j][1]) - redundancy
            compare_box_max_x = int(input_line[j][2]) + redundancy
            compare_box_max_y = int(input_line[j][3]) + redundancy

            x1 = max(base_box_min_x, compare_box_min_x)
            y1 = max(base_box_min_y, compare_box_min_y)
            x2 = min(base_box_max_x, compare_box_max_x)
            y2 = min(base_box_max_y, compare_box_max_y)
            if x2 - x1 > 0 and y2 - y1 > 0:
                iou_detected.append(input_line[j])
        if len(iou_detected) > 1:
            iou_detected = sorted(iou_detected, key=itemgetter(0))
            new_x1 = iou_detected[0][0]
            iou_detected = sorted(iou_detected, key=itemgetter(1))
            new_y1 = iou_detected[0][1]
            iou_detected = sorted(iou_detected, key=itemgetter(2), reverse=True)
            new_x2 = iou_detected[0][2]
            iou_detected = sorted(iou_detected, key=itemgetter(3), reverse=True)
            new_y2 = iou_detected[0][3]
            if not new_x2 - new_x1 == 0:
                if (float(abs(new_y2 - new_y1)) / float(abs(new_x2 - new_x1))) > 0.5:
                    append_line.append([new_x1, new_y1, new_x1, new_y2])
                else:
                    append_line.append([new_x1, new_y1, new_x2, new_y1])
            else:
                append_line.append([new_x1, new_y1, new_x1, new_y2])
        else:
            append_line.append(input_line[i])
    if append_line != input_line:
        connect_hl(append_line, redundancy)
    else:
        global appended_hl
        appended_hl = append_line.copy()

'''
0. 작성자 : 이호준

1. input 
 (1-1) yolo_result_path : 구조평면도에서 텍스트를 찾은 욜로 결과 경로 (이미지,텍스트파일)
 (1-2) txt_name : 욜로결과를 픽셀좌표로 변환한 txt 파일 이름
 (1-3) source_img : 구조평면도 원본이미지
 (1-4) yolo_img : 구조평면도 욜로 검출 결과 텐서

2. output 
 (2-1) appended_vl, appended_hl : 허프변환 및 전처리를 거쳐 변환된 최종 가로 , 세로 선 집합

3. algorithm : 
'''
def line_detection(yolo_result_path, txt_name, source_img, yolo_img):


    start = time.time() #코드 실행시간 측정을 위한 시작 시간 메모리

    print("Start line detecing")

    result_dir = "./scaling_result/"

    os.makedirs(result_dir , exist_ok=True) #결과 저장 디렉토리 생성


    # img = cv2.imread(boe_name)
    img = source_img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_gray_bin = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
    gray = img_gray_bin
    gray = cv2.bitwise_not(gray)
    #########################################
    min_line_length = 40
    max_line_gap = 15
    ########## parameters ##########
    threshold = 100  ## to find nonzero point
    angle_step = 90  ## pi / angle step
    ################################
    src = img.copy()
    src2 = img.copy()
    ##############
    ##degree 2 radian##
    thetas = np.deg2rad(np.arange(-90.1, 90, angle_step))
    print(thetas)
    ###################
    width, height = gray.shape
    diag_len = int(round(math.sqrt(width * width + height * height)))
    ############################################################################
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

    cos_t = np.cos(thetas)

    sin_t = np.sin(thetas)

    num_thetas = len(thetas)
    # print(num_thetas)
    ## accumulator is hough space ##
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    ################################

    non_zero = gray > threshold

    ## To optimize calculate find non zero point ##
    y_idxs, x_idxs = np.nonzero(non_zero)
    ###############################################

    ## nonzero point의 픽셀위치를 저장하기 위한 리스트 ##
    non_zero_point = []
    ## accumulator와 동일한 크기의 리스트를 생성 ##
    for j in range(len(rhos)):
        tmp_list = []
        for j in range(num_thetas):
            tmp_list.append([])
        non_zero_point.append(tmp_list)

    ##rho , theta에 투표될때 nonzero point의 좌표를 저장함 ##
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]
        tmp = [x, y]
        for t_idx in range(num_thetas):
            rho = diag_len + round(x * cos_t[t_idx] + y * sin_t[t_idx])
            accumulator[rho, t_idx] += 1
            non_zero_point[rho][t_idx].append(tmp)

    x, y = [], []
    vote_thresh = 5
    for j in range(2 * diag_len):
        for i in range(num_thetas):
            if accumulator[j, i] >= vote_thresh:
                x.append(i)
                y.append(j)


    ## rho,theta에 투표된 좌표의 값을 dot로 불러옴
    line = []
    for i in range(len(x)):
        dot = non_zero_point[y[i]][x[i]]
        tmp = []
        result = []
        ## 이미지의 원점(좌상단)으로부터 해당 점까지의 거리 순으로 순서대로 정렬
        for j in range(len(dot)):
            dis = math.sqrt((dot[j][0] * dot[j][0]) + (dot[j][1] * dot[j][1]))
            tmp.append([dot[j][0], dot[j][1], dis])

        tmp.sort(key=itemgetter(2))

        start_point = [tmp[0][0], tmp[0][1]]
        last_point = []
        for k in range(len(tmp)):
            # 마지막 점인 경우 가장 최근에 갱신된 선분의 시작점과 마지막점을 하나의 선으로 검출
            if (k == len(tmp) - 1):
                if (math.sqrt(((tmp[k][0] - start_point[0]) * (tmp[k][0] - start_point[0])) + (
                        (tmp[k][1] - start_point[1]) * (tmp[k][1] - start_point[1])))) > min_line_length:
                    cv2.line(src, (start_point[0], start_point[1]), (tmp[-1][0], tmp[-1][1]), (255, 255, 0), 2)
                    cv2.line(src, (start_point[0], start_point[1]), (start_point[0], start_point[1]), (255, 0, 0), 4)
                    cv2.line(src, (tmp[-1][0], tmp[-1][1]), (tmp[-1][0], tmp[-1][1]), (255, 0, 0), 4)
                    line.append([[start_point[0], start_point[1]], [tmp[-1][0], tmp[-1][1]]])
                continue
            gap = math.sqrt(math.pow(tmp[k + 1][0] - tmp[k][0], 2) + math.pow(tmp[k + 1][1] - tmp[k][1], 2))
            # 계산된 gap이 설정한 max_line_gap 보다 큰 경우 현재까지 누적된 좌표의 시작점과 끝점을 하나의 선으로 검출
            if gap > max_line_gap:
                last_point = [tmp[k][0], tmp[k][1]]
                if math.sqrt(math.pow(last_point[0] - start_point[0], 2) + math.pow(last_point[1] - start_point[1],
                                                                                    2)) > min_line_length:
                    cv2.line(src, (start_point[0], start_point[1]), (last_point[0], last_point[1]), (0, 0, 255), 2)
                    cv2.line(src, (start_point[0], start_point[1]), (start_point[0], start_point[1]), (255, 0, 0), 4)
                    cv2.line(src, (last_point[0], last_point[1]), (last_point[0], last_point[1]), (255, 0, 0), 4)
                    line.append([[start_point[0], start_point[1]], [last_point[0], last_point[1]]])
                start_point = [tmp[k + 1][0], tmp[k + 1][1]]

    virtical_line = []
    horizon_line = []
    ## 기울기를 계산한 후 y/x에 따라 세로선인지 가로선인지 구분 함
    for l in line:

        grad = gradient_calc(l[0], l[1])
        if grad <= 1:
            horizon_line.append(l)
        else:
            virtical_line.append(l)

    new_virtical_line = []
    new_horizon_line = []
    post_virtical_line = virtical_line.copy()
    post_horizon_line = horizon_line.copy()
    cnt = 0
    ## line_sum 함수를 통해 분할되어 검출된 가로, 세로선을 1차적으로 합치는 과정을 거침
    while ((new_horizon_line != post_horizon_line) or (new_virtical_line != post_virtical_line)):

        new_virtical_line, new_horizon_line = line_sum(post_virtical_line, post_horizon_line)
        if cnt != 0:
            post_virtical_line, post_horizon_line = new_virtical_line, new_horizon_line
        cnt += 1

    #### 2021.01.20 추가 욜로 박스 검출 결과를 리스트로 저장 ####


    box_info = yolo_text_box_to_list(yolo_result_path, txt_name, source_img, yolo_img)
    #######################################################

    delete_vl = []
    sorted_vl = []
    for vl in new_virtical_line:
        ##box info = x_min,y_min,x_max,y_max
        ## 가로선은 두 점중 하나가  x_min < 한 점 x 값 < x_max 이고 y_min< 한점 y 값 < y_max 이고
        ##                      x_min < 다른 한 점x 값 <x_max 이고 y_min < 다른 한 점 y값 < y max 이면
        ## 해당 선은 그리지 않는다
        x_start = 0
        x_end = 0
        y_start = 0
        y_end = 0
        if vl[0][1] < vl[1][1]:
            x_start = vl[0][0]
            x_end = vl[1][0]
            y_start = vl[0][1]
            y_end = vl[1][1]
        else:
            x_start = vl[1][0]
            x_end = vl[0][0]
            y_start = vl[1][1]
            y_end = vl[0][1]
        sorted_vl.append([x_start, y_start, x_end, y_end])
        for box in box_info:
            if box[0] - 25 < x_start and x_start < box[2] + 25:
                if box[1] - 25 < y_start and y_start < box[3] + 25:
                    if box[0] - 25 < x_end and x_end < box[2] + 25:
                        if box[1] - 25 < y_end and y_end < box[3] + 25:
                            delete_vl.append([x_start, y_start, x_end, y_end])

    delete_hl = []
    sorted_hl = []

    for hl in new_horizon_line:
        x_start = 0
        x_end = 0
        y_start = 0
        y_end = 0
        if hl[0][0] < hl[1][0]:
            x_start = hl[0][0]
            x_end = hl[1][0]
            y_start = hl[0][1]
            y_end = hl[1][1]
        else:
            x_start = hl[1][0]
            x_end = hl[0][0]
            y_start = hl[1][1]
            y_end = hl[0][1]
        sorted_hl.append([x_start, y_start, x_end, y_end])
        for box in box_info:
            if box[0] - 25 < x_start and x_start < box[2] + 25:
                if box[1] - 25 < y_start and y_start < box[3] + 25:
                    if box[0] - 25 < x_end and x_end < box[2] + 25:
                        if box[1] - 25 < y_end and y_end < box[3] + 25:
                            delete_hl.append([x_start, y_start, x_end, y_end])
    for dvl in delete_vl:
        iter=sorted_vl.count(dvl)
        for i in range(iter):
            sorted_vl.remove(dvl)
        """
        if dvl in sorted_vl:
            sorted_vl.remove(dvl)
        """
    for dhl in delete_hl:
        iter = sorted_hl.count(dhl)
        for i in range(iter):
            sorted_hl.remove(dhl)
        """
        if dhl in sorted_hl:
            sorted_hl.remove(dhl)
        """


    connect_vl(sorted_vl, 2)
    connect_hl(sorted_hl, 2)

    list(set(map(tuple, appended_vl)))  ## 가로선 집합
    list(set(map(tuple, appended_hl)))  ## 세로선 집합

    draw_line(appended_vl, src2)
    draw_line(appended_hl, src2)

    draw_img = src2.copy()
    draw_box(box_info, draw_img)

    cv2.imwrite(result_dir + 'result-before.jpg',src)
    cv2.imwrite(result_dir + 'result-after.jpg',src2)
    cv2.imwrite(result_dir + 'result-after-bb.jpg',draw_img)

    print("line detecting done")
    return appended_vl,appended_hl

# appended_vl,appended_hl = line_detection(yolo_result_path, boe_name, txt_name)
# print(len(appended_hl), len(appended_vl))