import pickle
import os
import serial
import re
import time
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

def rw(a,n,v,pt):
    if a=='R':
        data='0,0,R,S,S,0,1,0,6,%,D,W,0,0,0'.split(',')
    if a=='W':
        data='0,0,W,S,S,0,1,0,6,%,D,W,0,0,0,0,0,0,0'.split(',')
        data[18]=str(format(v%16,'x'))
        data[17]=str(format(v%256//16,'x'))
        data[16]=str(format(v%4096//256,'x'))
        data[15]=str(format(v//4096,'x'))
    data[14]=str(n%10)
    data[13]=str(n%100//10)
    data[12]=str(n//100)
    x=[]
    x.append(5)
    for i in range(len(data)):
        x.append(ord(data[i]))
    x.append(4)
    ser=serial.Serial()
    ser.baudrate = 115200
    ser.port = pt
    ser.open()
    ser.write(bytearray(x))
    if(a=='R'):
        rx_data=ser.read(15)
    if(a=='W'):
        rx_data=ser.read(ser.inWaiting())
    rx_data=rx_data.decode()
    ser.close()
    if a=='R':
        return int(rx_data[10],16)*4096+int(rx_data[11],16)*256+int(rx_data[12],16)*16+int(rx_data[13],16)

def trasport(send, PN):
    portnumber = "COM" + "{0}".format(str(PN))
   # print(portnumber)
   #ser = serial.Serial(portnumber, 115200, timeout = 1)

    i = 0

    count = 0
    
    PLC_State = 0

    while(i <= len(send)):
        if((PLC_State == 2) and (i >= 1) and (rw('R',614,0, portnumber) == 0)):
            print("가공완료")
            PLC_State = 0
        
        if((rw('R',614,0, portnumber) == 0) and (PLC_State == 0)):
            time.sleep(1)
            if (count == 0):
                data = send[i]
                data = str(data)
                data = int(data)
                print(data)
                rw('W', 100, data, portnumber)
                i = i + 1
                count = count + 1
        
            elif (count == 1):
                data = send[i]
                data = str(data)
                data = int(data)
                print(data)
                rw('W', 101, data, portnumber)
                count = count + 1
         
            elif (count == 2):
                data = send[i]
                data = str(data)
                data = int(data)
                print(data)
                rw('W', 103, data, portnumber)
                i = i + 1
                count = count + 1
            
            else:
                data = send[i]
                data = str(data)
                data = int(data)
                print(data)
                rw('W', 102, data, portnumber)
                i = i + 1
                count = 0
                PLC_State = 1
        else:
            if(PLC_State==1):
                print("작업중")
                PLC_State = 2