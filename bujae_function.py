import cv2
import os
import copy

'''
0. 작성자 : 유승환

1. input 
 (1-1) txt_out : tmp txt dir

2. output 
 (2-1) remove tmp txt file (= algorithm)

'''
def remove_tmp_txt(txt_out):
    tmp_result_list = os.listdir(txt_out)

    for i in range(len(tmp_result_list)):
        os.remove(txt_out + tmp_result_list[i]) 


'''
0. 작성자 : 이호준

1. input
 (1-1) yolo_result_txt : 부재 리스트에서 클러스터링 된 셀의 이미지에 대한 yolo text 검출 결과 txt 파일 경로 
 (1-2) source : 클러스터링 된 셀 이미지 경로
 (1-3) SAVE_PATH : 크롭된 결과 이미지가 저장될 경로

2. output
 (2-1) tmp : 클러스터링 된 셀안의 글자 영역을 crop 한 이미지들

3. algorithm
 (3-1) 클러스터링 된 셀 이미지와 yolo로 검출한 텍스트 영역을 입력으로 받아 해당 텍스트 영역만을 추출
 (3-2) 추출한 영역을 이미지로 저장
'''
def crop(yolo_result_txt, source, SAVE_PATH):
    print("Start Crop Text (40%)")

    ### Load Box info
    # res = [class, 0.5, x_center, y_center, width, height]
    res = []

    ### Read yolo result
    f = open(yolo_result_txt, 'r')
    data = f.read()

    ### 이미지 단위로 분할
    img_split = data.split('###')
    # print(img_split)

    for img_output in img_split:
        tmp = []
        if '\n' in img_output:
            img_output_split = img_output.split('\n')

            for line in img_output_split:
                line_split = line.split()
                # print(line_split)

                if line_split:
                    construct_split = [int(line_split[0]), float(line_split[1]),
                                       [int(round(float(line_split[2]))), int(round(float(line_split[3]))),
                                        int(round(float(line_split[4]))), int(round(float(line_split[5])))]]
                    tmp.append(construct_split)

        else:
            img_output_split = img_output.replace('\n', '')
            line_split = img_output_split.split()
            construct_split = [int(line_split[0]), float(line_split[1]),
                               [int(round(float(line_split[2]))), int(round(float(line_split[3]))),
                                int(round(float(line_split[4]))), int(round(float(line_split[5])))]]
            tmp.append(construct_split)

        res.append(tmp)
    f.close()

    ### Load Cluster Img
    img_list = os.listdir(source)
    img_list.sort()
    print(len(img_list))
    print("###")
    for i in range(len(img_list)):
        print(img_list[i])

    ### crop the text from clutser img
    for idx, img in enumerate(img_list):
        image = cv2.imread(source + img, cv2.IMREAD_COLOR)
        height, width, channel = image.shape
        # print(height)
        # print("###")

        trans_res = []
        y_order = []
        y_ordered_trans_res = []
        floored_trans_res = []

        # 튜블 형식의 res를 수정가능하게 list로 변환
        for k in range(len(res[idx])):
            tmp_res = []
            tmp_res.append(res[idx][k][0])
            tmp_res.append(res[idx][k][1])
            box_info = list((res[idx][k][2]))
            tmp_res.append(box_info)
            trans_res.append(tmp_res)

        for w in range(len(trans_res)):
            y_order.append(float(trans_res[w][2][1]))

        y_order.sort()
        thresh = y_order[0]
        thresh_list = []
        thresh_list.append(thresh)

        for t in range(len(y_order)):
            if y_order[t] > thresh + 10 or y_order[t] < thresh - 10:
                thresh = y_order[t]
                thresh_list.append(thresh)

        for h in range(len(thresh_list)):
            x_order = []
            x_ordered_trans_res = []

            for p in range(len(trans_res)):
                for u in range(len(trans_res)):
                    if float(trans_res[u][2][1]) == y_order[p] and (
                            float(trans_res[u][2][1]) < thresh_list[h] + 10 and float(trans_res[u][2][1]) > thresh_list[
                        h] - 10):
                        y_ordered_trans_res.append(trans_res[u])

            for g in range(len(y_ordered_trans_res)):
                if float(y_ordered_trans_res[g][2][1]) < thresh_list[h] + 10 and float(y_ordered_trans_res[g][2][1]) > \
                        thresh_list[h] - 10:
                    x_order.append(float(y_ordered_trans_res[g][2][0]))

            x_order.sort()

            for n in range(len(x_order)):
                for m in range(len(y_ordered_trans_res)):
                    if float(y_ordered_trans_res[m][2][0]) == x_order[n]:
                        x_ordered_trans_res.append(y_ordered_trans_res[m])

            floored_trans_res.append(x_ordered_trans_res)

        for j in range(len(trans_res)):
            tmp = image.copy()
            # print(tmp.shape)
            # print(trans_res[j])
            # print(int(trans_res[j][2][1])-int(trans_res[j][2][3]/2),int(trans_res[j][2][1])+int(trans_res[j][2][3]/2),int(trans_res[j][2][0])-int(trans_res[j][2][2]/2),int(trans_res[j][2][0])+int(trans_res[j][2][2]/2))

            tmp = image[int(trans_res[j][2][1]) - int(trans_res[j][2][3] / 2):int(trans_res[j][2][1]) + int(
                trans_res[j][2][3] / 2),
                  int(trans_res[j][2][0]) - int(trans_res[j][2][2] / 2):int(trans_res[j][2][0]) + int(
                      trans_res[j][2][2] / 2)]
            # print("tmp_shape")
            # print(tmp.shape)
            name = copy.deepcopy(img)
            # print(img)
            name = name.replace('.jpg', '_' + str(j) + '.jpg')
            print(SAVE_PATH)
            cv2.imwrite(SAVE_PATH + name, tmp)
    print("Finish Crop Text")