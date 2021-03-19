import cv2
import os
from operator import itemgetter
import pickle

'''
0. 작성자
 - 이호준 

1. input
 (1-1) save_image_folder_path : 텍스트 영역이 crop된 이미지 + 이름이 좌표영역 , 인식된 텍스트내용 .jpg로 구성된 OCR 아웃풋이 저장된 경로
 (1-2) final_pickle_dir : 통합된 정보를 저장할 pickle 파일 경로

2. output
 (2-1) bujae_obj : 딕셔너리 형태로 저장된 통합 정보 결과 list

3. 알고리즘
 (3-1) 모든 이미지를 조회하며 x 값이 비슷한 셀을 리스트로 묶어 저장한다.
 (3-2) 이중  x값이 가장 좌측인 첫 열 리스트를 선택한다.
 (3-3) 첫 열을 순환하며 y 값의 순서대로 데이터를 정렬한다.
 (3-4) 첫 열 리스트를 순환하며 중복을 허용하지 않고 텍스트 내용을 리스트에 저장한다. << 부재정보에 필요한 셀 갯수 추출
 (3-5) 첫 열 리스트를 순환하며 부재 정보에 필요한 셀 갯수만큼 나누어 리스트로 저장한다.
 (3-6) 부재 정보 셀 갯수만큼 나뉜 리스트의 첫 번째 셀(부호)을 기준으로 모든 이미지를 조회하며 동일한 y 값을 가지는 셀을 리스트에 저장한다. (이때 첫번째 셀(부호)을 제외함)
 (3-7) x 값의 순서대로 데이터를 정렬한다.
 (3-8) 부재 정보 셀 갯수만큼 나뉜 리스트의 두 번째 셀~ 마지막 셀을 기준으로 모든 이미지를 조회하며 동일한 y 값을 가지는 셀을 리스트에 저장한다.
 (3-9) x 값의 순서대로 데이터를 정렬한다.
 (3-10) 첫 번째 셀을 기준으로 동일한 y 값을 가지는 셀이 저장된 두번째 ~ 마지막 셀 리스트를 순차적으로 순환하며 첫 셀의 x 범위에 포함되는 하위 셀을 [첫번째 셀[j] , [ [두번째 셀[i],...마지막셀[i]] , [두번째 셀[i+1],...마지막셀[i+1]] ] ] 과 같이 저장한다.
 (3-11) 10 번에 저장된 리스트들을 순환하며 딕셔너리 형태로 데이터를 저장한다. << 데이터 저장시 10번 저장 리스트[1]의 개수만큼 반복하며 (첫번째 셀[j],두번째 셀[i],...마지막 셀[i]), (첫번째 셀[j],두번째 셀[i+1],...마지막셀[i+1])식으로 저장
'''

def info_combination(save_image_folder_path, final_pickle_dir):

    img_list = os.listdir(save_image_folder_path)
    img_list.sort()
    info = []

    ############ make information ('ganseok', 'boe', '02',x,y,w,h,cell_info,tex1,tex2,...)from img name
    ############ cell info : 0 = 해당 셀의 첫번째 데이터 1~ = 해당셀의 두번째, 세번째 , ... 데이터
    for i in range(len(img_list)):
        text = img_list[i]
        text = text.replace('.jpg', '')
        information = text.split('_')
        info.append(information)  ##### info = [ [ ['ganseok', 'boe', '02',x,y,w,h,cell_info,tex1] ] , .... ]

    columns=[]
    ## 셀 좌표의 x 값이 +-50픽셀 범위 이내인 셀끼리 분류하여 리스트에 저장
    for idx,cell in enumerate(info):
        if idx == 0:
            tmp = []
            tmp.append(cell)
            columns.append(tmp)

        else:

            insert_state = False
            for columns_idx,column in enumerate(columns):
                if insert_state == True:
                    continue
                else:
                    if abs(int(cell[3])-int(column[0][3]))<10:
                        if cell not in columns[columns_idx]:
                            columns[columns_idx].append(cell)
                            insert_state=True
                    else:
                        if columns_idx == len(columns)-1:
                            columns.append([cell])

    # 각 열의 첫번째 셀의 x 값을 추출 후 가장 좌측의 열 인덱스를 찾는다
    columns_x=[]
    for i in range(len(columns)):
        columns_x.append(int(columns[i][0][3]))

    # 가장 좌측열 추출
    left_column = columns[columns_x.index(min(columns_x))].copy()
    for i in range(len(left_column)):
        left_column[i][3]=int(left_column[i][3])
        left_column[i][4]=int(left_column[i][4])

    # 가장 좌측의 열을 순환하며 y 값의 순서대로 데이터를 정렬한다.

    left_column.sort(key=itemgetter(4))

    # 좌측열의 셀을 순환하며 부재 정보에 필요한 단위 정보 추출
    unit = []
    for cell in left_column:  ##find unit word from first row
        if not cell[8] in unit:  ## remove overlap word
            unit.append(cell[8])

    # 첫 열 리스트를 순환하며 부재정보에 필요한 셀 갯수 만큼 나누어 리스트로 저장
    divided_left_column = []
    div_num = int(len(left_column)/len(unit))
    for i in range(div_num):
        divided_left_column.append([])

    cell_cnt = 0
    object_cnt = 0

    for cell in left_column:
        divided_left_column[object_cnt].append(cell)
        cell_cnt+=1
        if cell_cnt % len(unit) == 0 and cell_cnt!=0:
            object_cnt+=1

    horizon_aline_list = []

    for i in range(len(divided_left_column)):
        tmp = []
        for j in range(len(divided_left_column[i])):
            tmp.append([])
        horizon_aline_list.append(tmp)

    for i in range(len(divided_left_column)):
        for j in range(len(divided_left_column[i])):
            cell_y_value = int(divided_left_column[i][j][4])
            for idx, cell in enumerate(info):
                if cell != divided_left_column[i][j] :
                    if abs(int(cell[4])-cell_y_value) <=10:
                        tmp_cell = cell.copy()
                        tmp_cell[3]=int(tmp_cell[3])
                        tmp_cell[4]=int(tmp_cell[4])
                        horizon_aline_list[i][j].append(tmp_cell)

    for i in range(len(horizon_aline_list)):
        for j in range(len(horizon_aline_list[i])):
            horizon_aline_list[i][j].sort(key=itemgetter(3))

    bujae = []
    for i in range(len(horizon_aline_list)): ## 행 개수

        tmp_column = []
        for j in range(len(horizon_aline_list[i][0])):
            tempo=[]
            tempo.append(horizon_aline_list[i][0][j])
            tempo.append([])
            tmp_column.append(tempo)
        bujae.append(tmp_column)
    ## bujae = (행 개수, 해당 행의 부재 개수 , [[부재 이름 및 위치 정보],[부재의 하위 정보 리스트]]])

    for i in range(len(horizon_aline_list)):
        for j in range(1,len(horizon_aline_list[i])):

            tmp = []
            for k in range(len(horizon_aline_list[i][j])):
                if horizon_aline_list[i][j][k][7] == '0':
                    tmp.append([horizon_aline_list[i][j][k]])
                else:
                    tmp[-1].append(horizon_aline_list[i][j][k])

            for l in range(len(bujae[i])):
                for u in range(len(tmp)):

                    if int((2*int(tmp[u][0][3])+int(tmp[u][0][5]))/2)>=int(bujae[i][l][0][3]) and int((2*int(tmp[u][0][3])+int(tmp[u][0][5]))/2)<=(int(bujae[i][l][0][3])+int(bujae[i][l][0][5])) :
                        bujae[i][l][1].append(tmp[u])

    for i in range(len(bujae)):
        for j in range(len(bujae[i])):
            lowest_y = bujae[i][j][1][0][0][4]
            cnt = 1
            for k in range(len(bujae[i][j][1])):
                if k == 0:
                    continue
                else:
                    if abs(bujae[i][j][1][k][0][4]-lowest_y)<5:
                        cnt+=1
            new_sub = bujae[i][j][1].copy()
            new_sub = new_sub[:cnt]

            for l in range(len(new_sub)):
                tmp = []
                for t in range(len(bujae[i][j][1])):
                    if bujae[i][j][1][t] != new_sub[l]:
                        if int((2*int(bujae[i][j][1][t][0][3])+int(bujae[i][j][1][t][0][5]))/2)>=int(new_sub[l][0][3]) and int((2*int(bujae[i][j][1][t][0][3])+int(bujae[i][j][1][t][0][5]))/2)<=int(new_sub[l][0][3])+int(new_sub[l][0][5]):
                            tmp.append(bujae[i][j][1][t])
                new_sub[l].append(tmp)

            bujae[i][j][1]=new_sub

    bujae_obj = []
    bujae_obj_list=[]

    for i in range(len(bujae)):
        for j in range(len(bujae[i])):
            for k in range(len(bujae[i][j][1])):
                dic = []
                dic.append([bujae[i][j][0][-1]])
                tmp = []
                for l in range(len(bujae[i][j][1][k][:-1])):
                    tmp.append(bujae[i][j][1][k][:-1][l][-1])
                dic.append([tmp])
                for t in range(len(bujae[i][j][1][k][-1])):
                    dic.append([bujae[i][j][1][k][-1][t][0][-1]])
                bujae_obj_list.append(dic)
                for r in range(len(dic)):
                    dic[r].insert(0,unit[r])

                #### 버그를 잡기위한 임시 코드 ####
                remove_list = []
                for idx, key in enumerate(dic[1][1]):
                    if isinstance(key,list):
                        remove_list.append(idx)
                target_list = []
                for target in remove_list:
                    target_list.append(dic[1][1][target])
                for target in target_list:
                    dic[1][1].remove(target)
                ###############################
                dic=dict(dic)
                bujae_obj.append(dic)

    for obj in bujae_obj:
        print(obj)

    #print(bujae_obj) << 튜플 형식으로 저장된 부재 정보
    #print(bujae_obj_list) << 리스트로 저장된 부재 정보

    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
    with open(final_pickle_dir, 'wb') as file_result:
        pickle.dump(bujae_obj, file_result)

    # print(result_list)
