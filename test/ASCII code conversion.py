''''
ASCII可显示字符
http://ascii.911cha.com

chr():直接用转换函数 文字
使用ord()函数 数字
ASCII=input("ascii values:")
print(ASCII,"",ord(ASCII))

'''
'''
import binascii
ASCII = input("ascii values:")
ascii_values = []
for character in ASCII:
    ascii_values.append(ord(character))
print(ascii_values)
'''
'''
string = "6D72020F 24011500 00000000 15000A0D 6D72020F 27011700 00000000 17"
byte_array = bytearray.fromhex(string)
byte_array.decode()
'''
'''
import codecs
string = "6D72020F" "24011500" "00000000" "15000A0D" "6D72020F" "27011700" "00000000" "17"
binary_str = codecs.decode(string, "hex")
print(str(binary_str,'utf-8'))

<< mr$ mr'
'''
'''
import codecs
string = "6D72020F240115000000000015000A0D6D72020F270117000000000017"
print(string[0:7])

binary_str = codecs.decode(string, "hex")
print(str(binary_str,'utf-8'))
'''

import codecs
# string = "6D72020F" 
string = "6D72020F240102010000000015000A0D"
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
    #arr.append(string[i:i+2])
    #print(string[i:i+2])

#print(arr[7::2])
# binary_str = codecs.decode(string, "hex")
# print(str(binary_str,'utf-8'))


#6D72020F240102010000000015000A0D

def decode(string):
    string = input("")
    if ((string[0:2] == "6D") and (string[2:4] == "72")) and ((string[28:30] == "0A") and (string[30:32] == "0D")):
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

print(input(decode("")))

