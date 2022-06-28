import socket
import threading
import re


def main():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #c.connect(('192.168.0.113', 8234))
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
        print("/n")

# t = threading.Thread(target=main)
# t.start()

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


main()