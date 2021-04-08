import serial

def rw(a,n,v,pt):
    
    portnumber = "COM" + "{0}".format(str(pt))
    
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
    ser.port = portnumber
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