import socket
import threading
import re
import codecs
import sympy
import numpy as np

XA = 0.0
YA = 0.0

XB = 8.5
YB = 0.0

XC = 8.5
YC = 5.0



def main():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # c.connect(('192.168.0.113', 8234))
    # c.close()
    c.bind(('192.168.0.113', 8234))
    #c.sendall("connect server successfully!".encode(encoding='utf8'))
    c.listen(10)
    client, address = c.accept()
    while True:
        bytes = client.recv(1024)
        #msg = bytes.decode(encoding='utf8')
        #msg = bytes.decode('utf8')
        #print(bphero_dispose(msg)+"/n")
        print(bytes.hex())
        inStr = convert(bytes.hex())
        if (inStr != -1):
            print(inStr)
            print(triposition(XA,YA,inStr[0],XB,YB,inStr[1],XC,YC,inStr[2]))
        else:
            print("Error!")
        print("/n")

# t = threading.Thread(target=main)
# t.start()

'''
def bphero_dispose(string):
    result_dict = {'tag': 0x1005, 'seq': 7, 'time': 1234, 'anthor_count': 4,'anthor': []}

    # 数据包以&&& 开头
    res = re.findall(r'&&&', string)
    flag = 1
    if len(res) > 0:
        # step1 print message length,ex 76
        temp_string = string.split("$")[0]  # &&&:80$
        data_len = int(temp_string.split(":")[1], 16)

        # tag info
        temp_string = string.split("$")[1]  # 000A:20
        tag_id = int(temp_string.split(":")[0], 16)  # 000A
        tag_seq = int(temp_string.split(":")[1], 16)  # 20
        # print("标签ID: %02X  Seq: %X" % (tag_id, tag_seq))
        result_dict['tag'] = tag_id
        result_dict['seq'] = tag_seq

        # anthor info
        temp_string = string.split("$")[2]  # 0001:A1B1:11#0002:A2B2:22#0003:A3B3:33#0004:A4B4:44#0005:A5B5:55
        anthor_count = len(temp_string.split('#'))
        result_dict['anthor_count'] = anthor_count

        for index in range(anthor_count):
            anthor_info = temp_string.split('#')[index]  # 0001:A1B1:11
            anthor_id = int(anthor_info.split(":")[0], 16)
            anthor_dist = 0.01*int(anthor_info.split(":")[1], 16)   # convert to cm
            print("Anthor%d Distance = %0.2f m"% (index+1, anthor_dist))
            anthor_rssi = int(anthor_info.split(":")[2], 16)
            result_dict['anthor'].append([anthor_id, anthor_dist, anthor_rssi])
        flag = 0
    return result_dict
'''

def convert(string):
    # string = input("")
    if ((string[0:2] == "6d") and (string[2:4] == "72")) and ((string[28:30] == "0a") and (string[30:32] == "0d")):
        arr = []
        for i in range(0,len(string),2):
            inStr = string[i:i+2]
        # m r
            if (i == 0 or i == 2):
                binary_str = codecs.decode(inStr, "hex")
                arr.append(str(binary_str,'utf-8'))
        # S/N, TAG ID, Frame
            if (i == 4 or i == 6 or i == 8 or i == 10):
                arr.append(string[i:i+2])
        # dis 1.hex -> dec 2. dec/100
            if (i == 12 or i == 14 or i == 16 or i == 18 or i == 20 or i == 22 or i == 24 or i == 26):
                inStr = string[i:i+2]
                inInt = int(inStr, 16)
                out = inInt/100
                if (i == 14 or i == 18 or i == 22 or i == 26):
                    val = inInt << 8
                    val = val/100
                    out = val + arr[int(i/2-1)]
                arr.append(out)
        # \r \n
        #else:
            #arr.append(string[i:i+2])
        #print(string[i:i+2])
        return arr[7::2]
    else: 
        return -1


def triposition(xa,ya,da,xb,yb,db,xc,yc,dc): 
    x,y = sympy.symbols('x y')
    f1 = 2*x*(xa-xc)+np.square(xc)-np.square(xa)+2*y*(ya-yc)+np.square(yc)-np.square(ya)-(np.square(dc)-np.square(da))
    f2 = 2*x*(xb-xc)+np.square(xc)-np.square(xb)+2*y*(yb-yc)+np.square(yc)-np.square(yb)-(np.square(dc)-np.square(db))
    result = sympy.solve([f1,f2],[x,y])
    locx,locy = result[x],result[y]
    return [locx,locy]


main()

