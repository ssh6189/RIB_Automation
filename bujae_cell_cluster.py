# CODE : Extract floor plan's Cells by opencv-preprocess & K-Means(Clustering)
# DATE : 2020-12-01 (by Ham, HJ, SH)
# INPUT : floor plan (bujae-list) (JPG)
# OUTPUT : floor plan's Cells (JPG)

from sklearn.cluster import KMeans

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import os
import cv2
import copy


'''
0. 작성자 : 함종수

1. input 
 (1-1) input_img : bujae list's img

2. output 
 (2-1) blur : preporcess's img

3. algorithm : preprocess the image and clear the interior of cells
'''
def img_preprocess(input_img):
    ### 도면 내 내용물 제거 ########################
    print("START img_preprocess")
    ### 메모리 초기화 
    img = []            # 도면 원본
    copied_img = []     # 도면 사본 메모리
    blur = []           # 작업 메모리
    a = []              # contour 면적 리스트 메모리

    img = input_img.copy()
    img_path = "/"
    copied_img = img.copy()

    ### 전처리_1 : 흑백 변환
    blur = cv2.cvtColor(copied_img, cv2.COLOR_BGR2GRAY) 

    ### 전처리_2 : 이진화
    input = blur

    maxval = 255
    thresh = maxval / 2
    _, thresh2 = cv2.threshold(input, 0, 255, cv2.THRESH_OTSU)

    blur = thresh2
    # cv2.imwrite('result_cluster/test' + img_path[:-4]+ '_ip_01_01_binary.jpg', blur)

    ### 전처리_3 : 침식
    input = blur

    ksize = (5, 5)
    kernel = {}
    kernel[0] = cv2.getStructuringElement(cv2.MORPH_RECT, ksize)
    erosion = cv2.erode(input, kernel[0])

    blur = erosion.copy()
    # cv2.imwrite('result_cluster/test' + img_path[:-4]+ '_ip_01_02_erode.jpg', blur)

    ### 내용물 제거 : 최대 area, width, height 기준 제거 
    input = blur

    canny = cv2.Canny(input, 100, 200, L2gradient=True)
    # cv2.imwrite('result_cluster/test' + img_path[:-4]+ '_ip_01_02_canny.jpg', canny)

    ### contour 추출
    canny_contours, canny_hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ### 메모리 초기화
    mw = 0  # 내용물 최대 width
    mh = 0  # 내용물 최대 height
    ma = 0  # 내용물 최대 area
    margin = 0

    ### 각 contour마다 반복 : 내용물의 최대 width, height, area 정보 추출./cvresult/imageprocessing+rect_0628/
    for i, ch in enumerate(canny_hierarchy[0]):
        ### contour 면적 리스트 작성 ##a 초기화시 메모리 공간 설정 작업 추가 필요
        a.append(cv2.contourArea(canny_contours[i]))  

        ### child 없는 contour 선별
        if ch[2] == -1:
            x, y, w, h = cv2.boundingRect(canny_contours[i])
            mw = max(mw, w)
            mh = max(mh, h)
            ma = max(ma, a[i])

    ### 각 contour마다 반복 : . contour 근사화 사각형으로 제거
    for i, ch in enumerate(canny_hierarchy[0]):
        x, y, w, h = cv2.boundingRect(canny_contours[i])

        ### 사각형이 아닌 contour 제거
        if a[i] < ma and (w < mw or h < mh):
            blur[y + margin:y + h - margin, x + margin:x + w - margin] = 255


        elif a[i] > ma and (w < mw or h < mh):
            blur[y + margin:y + h - margin, x + margin:x + w - margin] = 255

            ###### debug #####           
            # debug_img = input_img.copy()
            # cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0,0,255), 1)
            # cv2.putText(debug_img, text=str(a[i])+","+str(ma), org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0,0,255), thickness=2)
            # cv2.putText(debug_img, text=str(w)+","+str(mw), org=(x, y+5), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0,0,255), thickness=2)
            # cv2.putText(debug_img, text=str(h)+","+str(mh), org=(x, y+10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0,0,255), thickness=2)
            # cv2.imwrite('C:/Users/cai-kvm-8/t-in/result_bujae/test/09_ham_new_img_proprecess_result'+str(i)+'.jpg', blur)        

    input = blur

    canny = cv2.Canny(input, 100, 200, L2gradient=True)
    canny_contours, canny_hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contour 추출

    for i, ch in enumerate(canny_hierarchy[0]):
        epsilon = 0.01 * cv2.arcLength(canny_contours[i], True)
        approx = cv2.approxPolyDP(canny_contours[i], epsilon, True)

        if len(approx) != 4:
            cv2.drawContours(blur, canny_contours, i, [255, 255, 255])

    ##### Result #####
    ### 실행 완료 출력
    cv2.imwrite('C:/Users/cai-kvm-8/t-in/result_bujae/result_bujae_preprocess/proprecess_result.jpg', blur)

    print("END img_preprocess")

    return blur


'''
0. 작성자 : 이호준

1. input 
 (1-1) prerocess_img : 
 (1-2) origin_img : 
 (1-3) img_name : 
 (1-4) save_path : 
 (1-5) show_graph : show graph clustering table?

2. output 
 (2-1) canny_bounding_result2 : clustering imgs

3. algorithm : 
'''
def clustering(prerocess_img, origin_img, img_name, save_path, show_graph):
    ### 도면 내 셀 추출 ########################
    print("START Clustering")
    cnt = 0

    input_1 = cv2.cvtColor(prerocess_img, cv2.COLOR_GRAY2BGR)
    gray_input = prerocess_img
    canny = cv2.Canny(gray_input, 100, 255, apertureSize=5)
    kernel = np.ones((3, 3), np.uint8)

    canny_contours, canny_hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    canny_contour_result = input_1.copy()
    canny_bounding_result = input_1.copy()
    canny_bounding_result2 = input_1.copy()

    data = []
    for contour in canny_contours:
        x, y, w, h = cv2.boundingRect(contour)
        data.append([w, h])

    # K-Means Clustering
    model = KMeans(n_clusters=2, algorithm='auto', max_iter=10000)

    K_point = model.fit_predict(data)
    print("K_point")
    print(K_point)
    kluster_point = K_point.tolist()
    cluster1 = kluster_point.count(0)
    cluster2 = kluster_point.count(1)
    cell = 0
    not_cell = 0
    if cluster1 > cluster2:
        cell=0
        not_cell = 1
    else :
        cell = 1
        not_cell = 0
    c0, c1 = model.cluster_centers_
    print("cluster_centers")
    print(c0, c1)

    for i in range(len(data)):
        if K_point[i] == cell:
            plt.scatter(data[i][0], data[i][1], marker='v', facecolor='r', edgecolors='k')

        elif K_point[i] == not_cell:
            plt.scatter(data[i][0], data[i][1], marker='o', facecolor='b', edgecolors='k')

    if show_graph == True :
        ### Graph for K-Means Result
        plt.scatter(c0[0], c0[1], marker='v', c="r", s=200)
        plt.scatter(c1[0], c1[1], marker='^', c="b", s=200)
        plt.grid(False)
        plt.title("K-Means")
        plt.show()

    for contour in canny_contours:
        ### 복사한 이미지에 칸투어를 그림
        cv2.drawContours(canny_contour_result, [contour], 0, (255, 0, 0), 1)

    for i in range(len(canny_contours)):
        x, y, w, h = cv2.boundingRect(canny_contours[i])

        if x<4400 and K_point[i] == cell:
            cv2.rectangle(canny_bounding_result, (x, y), (x+w, y+h), (0, 0 ,255), 1)

        elif x<4400 and K_point[i] == not_cell:
            cv2.rectangle(canny_bounding_result, (x, y), (x+w, y+h), (255,0, 0), 1)

    for i in range(len(canny_contours)):
        tmp = input_1.copy()
        x, y, w, h = cv2.boundingRect(canny_contours[i])

        if x<4400 and K_point[i] == not_cell:
            t_in = 10
            # print("loading...")
            
        elif x<4400 and K_point[i] == cell and w>100 and h>50:
            # print("loading...")
            cv2.rectangle(canny_bounding_result2, (x, y), (x+w, y+h), (0, 0, 255), 3)

            ### 경계사각형 영역을 tmp 이미지에 저장
            tmp = origin_img[y:y+h, x:x+w]
            ### tmp 이미지에 저장된 이미지를 사진으로 저장
            cv2.imwrite(save_path + img_name + '_' + str(x) + '_' + str(y) + '_' + str(w) + '_' + str(h) + '.jpg', tmp)

            cnt+=1
    cv2.imwrite('C:/Users/cai-kvm-8/t-in/result_bujae/result_bujae_preprocess/clustering_result.jpg', canny_bounding_result2)
    print("END Clustering")
