import pickle
import os
import serial
import re
import serial
'''
root_path = './Predict_Save'

# \\는 /로 나타내야한다.
root_path = root_path.replace('\\', '/')
    
def make_abspath_list(root_path):
    cout = 0
    str_result = ""
    text_list = []
    
    ## TODO2: 입력받은 경로 내 모든 파일 중 이미지인 파일의 절대경로를 pick_list에 추가
    
    #텍스트파일 확장자 리스트 생성
    text_extension = ['.txt']
    
    #root path내부를 탐색해 파일을 탐색한 후, 해당 파일이 텍스트 파일이면, pick_list에 이미지 파일의 절대경로를 추가
    for text_file in os.walk(root_path):
        for text in text_file[2]:
            for i in text_extension:
                if i in text:
                    #print(text)
                    fr = open(root_path + "/" + text,"r")
                    text = fr.read()
                    fr.close()
                        
                    #print(text)
                    
                    str_text = str(text)
'''
def chuchul(str_txt):
    cout = 0
    str_result = ""
    text_list = []
    fr = open(str_txt, 'r')
    str_text = fr.read()
    fr.close()
    #결과값이 저장된 txt파일 내부에서, PLC 제어에 필요한 부분만 추출
    for i in str_text:
        if i == "\n":
            i = i.replace('\n', '')
            
        if cout < 4:
            if ((i == '[') or (i == ']')):
                cout = cout + 1
                
        else:
            str_result = str_result + i
        
    return str_result

#print(make_abspath_list(root_path))
#send = make_abspath_list(root_path)
#괄호 제거
'''
def erase_gwalho(s):
    final_s = ""
    for i in s:
        if (i == '['):
            i = i.replace('[', '')
        elif (i == ']'):
            i = i.replace(']', '')
            
        final_s = final_s + i
            
    return final_s
'''
def transpormation(stirrup):
    number = []
    
    for i in stirrup:
        i = int(i)
        number.append(i)
        
    return number
        

def pick_number(stirrup):
    number = re.findall('\d+', stirrup)
    return number

#send = pick_number(send)

#send = transpormation(send)

#print(send)

def trasport(send, PN):
    portnumber = "COM" + "{0}".format(str(PN))
   # print(portnumber)
    ser = serial.Serial(portnumber, 115200, timeout = 1)

    ok = "okay"

    i = 0

    count = 0

    seto = "set"

    while(i < len(send)):
        if (count == 0):
             if ("sig1" in str(ser.readline())):
                data = send[i]
                data = str(data)
                ser.write(data.encode('utf-8'))
                i = i + 1
                count = count + 1
        
        elif (count == 1):
            if ("sig2" in str(ser.readline())):
                data = send[i]
                data = str(data)
                ser.write(data.encode('utf-8'))
                i = i + 1
                count = count + 1
        
        else:
            if ("sig3" in str(ser.readline())):
                data = send[i]
                data = str(data)
                ser.write(data.encode('utf-8'))
                ser.write(data.encode('utf-8'))
                i = i + 1
                count = 0