import socket
import threading
import re
import codecs
import timeit
import sympy
import numpy as np
from numpy import *
from sympy import symbols, Eq, solve
import timeit


XA = 0.0
YA = 0.0
ZA = 2.0

XB = 5.0
YB = 0.0
ZB = 2.0

XC = 0.0
YC = 5.0
ZC = 2.0

XD = 5.0
YD = 5.0
ZD = 3.0



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
            print(triposition(XA,YA,inStr[0],XB,YB,inStr[1],XC,YC,inStr[2])) #tag 和 base 的距离
        else:
            print("Error!")
        print("/n")

# t = threading.Thread(target=main)
# t.start()


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
            if (i == 12 or i == 14 or i == 16 or i == 18 or i == 20 or i == 22 or i == 24 or i == 26): #高八位
                inStr = string[i:i+2]
                inInt = int(inStr, 16) #转成十进制
                out = inInt/100
                if (i == 14 or i == 18 or i == 22 or i == 26): #低八位
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


def quartPosition(xa,ya,za,da,xb,yb,zb,db,xc,yc,zc,dc,xd,yd,zd,dd): #四组base   
    x = symbols('x')
    y = symbols('y')
    z = symbols('z')
    
    a1 = 2*xa-2*xb
    a2 = 2*ya-2*yb
    a3 = 2*za-2*zb
    
    a4 = 2*xa-2*xc
    a5 = 2*ya-2*yc
    a6 = 2*za-2*zc

    a7 = 2*xa-2*xd
    a8 = 2*ya-2*yd
    a9 = 2*za-2*zd
    
    b1 = xa*xa-xb*xb+ya*ya-yb*yb+za*za-zb*zb-da*da+db*db
    b2 = xa*xa-xc*xc+ya*ya-yc*yc+za*za-zc*zc-da*da+dc*dc
    b3 = xa*xa-xd*xd+ya*ya-yd*yd+za*za-zd*zd-da*da+dd*dd

    #解方程
    f1 = x*a1+y*a2+z*a3-b1
    f2 = x*a4+y*a5+z*a6-b2
    f3 = x*a7+y*a8+z*a9-b3
    out, = sympy.linsolve([f1,f2,f3],[x,y,z]) #tuple
    return list(out)

def test():
    DA = 5.83
    DB = 5.39
    DC = 4.36
    DD = 3.0

    triposition(XA,YA,DA,XB,YB,DB,XC,YC,DC)

    quartPosition(XA,YA,ZA,DA,XB,YB,ZB,DB,XC,YC,ZC,DC,XD,YD,ZD,DD)

# main()
# test()

print(timeit.timeit("test()", setup="from __main__ import test",number=100))
