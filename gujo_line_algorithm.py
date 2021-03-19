import math


def gradient_calc(dot1,dot2):
    x1 = float(dot1[0])
    y1 = float(dot1[1])
    x2 = float(dot2[0])
    y2 = float(dot2[1])
    if x2-x1 != 0:
        gradient = (y2-y1)/(x2-x1)
        magnitude_grad = abs(gradient)
    else:
        magnitude_grad = 1000
    return magnitude_grad


def line_sum(virtical_line,horizon_line):
    virtical_sum = []
    tmp_virtical = virtical_line.copy()
    for i in range(len(virtical_line)):
        for j in range(len(virtical_line)):
            if j <= i:
                continue
            else:
                meeting_point, side_point, case = line_summation(virtical_line[i], virtical_line[j], 2)
                if meeting_point:
                    #print('virtical_meeting_point')
                    #print(virtical_line[i],virtical_line[j])
                    if virtical_line[i] in tmp_virtical:
                        tmp_virtical.remove(virtical_line[i])
                    if virtical_line[j] in tmp_virtical:
                        tmp_virtical.remove(virtical_line[j])
                    if case == 1:
                        virtical_sum.append(side_point)
                    if case == 2:
                        if math.sqrt(math.pow(meeting_point[0] - side_point[0][0], 2) + math.pow(
                                meeting_point[1] - side_point[0][1], 2)) >= math.sqrt(
                                math.pow(meeting_point[0] - side_point[1][0], 2) + math.pow(
                                        meeting_point[1] - side_point[1][1], 2)):
                            virtical_sum.append([meeting_point, side_point[0]])
                        else:
                            virtical_sum.append([meeting_point, side_point[1]])
    new_virtical_line = virtical_sum + tmp_virtical

    horizon_sum = []
    tmp_horizon = horizon_line.copy()
    for i in range(len(horizon_line)):
        for j in range(len(horizon_line)):
            if j <= i:
                continue
            else:
                meeting_point, side_point, case = line_summation(horizon_line[i], horizon_line[j], 5)
                if meeting_point:
                    #print('horizon_meeting_point')
                    #print(horizon_line[i], horizon_line[j])
                    if horizon_line[i] in tmp_horizon:
                        tmp_horizon.remove(horizon_line[i])
                    if horizon_line[j] in tmp_horizon:
                        tmp_horizon.remove(horizon_line[j])
                    if case == 1:
                        horizon_sum.append(side_point)
                    if case == 2:
                        if math.sqrt(math.pow(meeting_point[0] - side_point[0][0], 2) + math.pow(
                                meeting_point[1] - side_point[0][1], 2)) >= math.sqrt(
                                math.pow(meeting_point[0] - side_point[1][0], 2) + math.pow(
                                        meeting_point[1] - side_point[1][1], 2)):
                            horizon_sum.append([meeting_point, side_point[0]])
                        else:
                            horizon_sum.append([meeting_point, side_point[1]])
    new_horizon_line = horizon_sum + tmp_horizon
    return new_virtical_line,new_horizon_line


def yolo_text_box_to_list(yolo_result_path,txt_name,source_img,yolo_img):
    height_ratio = source_img.shape[0] / yolo_img.shape[0]
    width_ratio = source_img.shape[1] / yolo_img.shape[1]
    # print(height_ratio, "\n", width_ratio)
#     height_ratio = 1
#     width_ratio = 1
    f = open(yolo_result_path + txt_name, 'r')
    data = f.readlines()
    box_info = []
    for line in data:
        box = line.split(' ')
        del box[0]
        box[0] = int(int(box[0]) * width_ratio)
        box[1] = int(int(box[1]) * height_ratio)
        box[2] = int(int(box[2]) * width_ratio)
        box[3] = box[3][0:-1]
        box[3] = int(int(box[3]) * height_ratio)
        box_info.append(box)
    f.close()
    return box_info

import cv2

def draw_line(line_list,img):
    if line_list:
        for line in line_list:
            x_start = line[0]
            y_start = line[1]
            x_end = line[2]
            y_end = line[3]
            cv2.line(img, (x_start,y_start),(x_end,y_end),(0,0,255),2)
            cv2.line(img, (x_start, y_start), (x_start, y_start), (255, 0, 0), 4)
            cv2.line(img, (x_end, y_end), (x_end, y_end), (255, 0, 0), 4)


def draw_box(box_list,img):
    for box in box_list :
        img = cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(255,0,0),2)


def line_summation(line1,line2,radius):
    meeting_point = []
    side_point = []
    case =0
    l1_start_point = line1[0]
    l1_end_point = line1[1]
    l2_start_point = line2[0]
    l2_end_point = line2[1]
    if math.sqrt(math.pow(l2_start_point[0]-l1_start_point[0],2)+math.pow(l2_start_point[1]-l1_start_point[1],2)) <= radius:
        meeting_point = l1_start_point
        side_point = [l1_end_point, l2_end_point]
    elif math.sqrt(math.pow(l2_end_point[0]-l1_start_point[0],2)+math.pow(l2_end_point[1]-l1_start_point[1],2)) <= radius:
        meeting_point = l1_start_point
        side_point = [l1_end_point, l2_start_point]
    elif math.sqrt(math.pow(l2_start_point[0]-l1_end_point[0],2)+math.pow(l2_start_point[1]-l1_end_point[1],2)) <= radius:
        meeting_point = l1_end_point
        side_point = [l1_start_point, l2_end_point]
    elif math.sqrt(math.pow(l2_start_point[0] - l1_end_point[0], 2) + math.pow(l2_start_point[1] - l1_end_point[1],2)) <= radius:
        meeting_point = l1_end_point
        side_point = [l1_start_point, l2_end_point]
    else :
        meeting_point = []
        side_point = []

    if meeting_point :
        direction_vector1 = [side_point[0][0]-meeting_point[0],side_point[0][1]-meeting_point[1]]
        direction_vector2 = [side_point[1][0]-meeting_point[0],side_point[1][1]-meeting_point[1]]
        direction1=0
        direction2=0
        if max(abs(direction_vector1[0]),abs(direction_vector1[1])) == abs(direction_vector1[0]):
            direction1 = direction_vector1[0]/abs(direction_vector1[0])
        else:
            direction1 = direction_vector1[1] / abs(direction_vector1[1])
        if max(abs(direction_vector2[0]),abs(direction_vector2[1])) == abs(direction_vector2[0]):
            direction2 = direction_vector2[0] / abs(direction_vector2[0])
        else:
            direction2 = direction_vector2[1] / abs(direction_vector2[1])
        if direction1 != direction2:
            case = 1
        if direction1 == direction2:
            case = 2
    return meeting_point,side_point,case