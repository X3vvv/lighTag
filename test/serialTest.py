import serial
import serial.tools.list_ports

 
def getSerial():

    # ports_list = list(serial.tools.list_ports.comports())
    # if len(ports_list) <= 0:
    #     print("无串口设备。")
    # else:
    #     print("可用的串口设备如下：")
    #     for comport in ports_list:
    #         print(list(comport)[0], list(comport)[1])

    ser = serial.Serial("/dev/cu.usbserial-1430", 115200)  # 打开COM17，将波特率配置为115200，其余参数使用默认值
    if ser.isOpen():  # 判断串口是否成功打开
        print("打开串口成功。")
        print(ser.name)  # 输出串口号
    else:
        ser.open()
        print("打开串口失败。")

    ser = serial.Serial(port="/dev/cu.usbserial-1430",
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5) 

    while True:
        com_input = ser.read(32)
        if com_input:
            print(com_input.hex())
            
    
    ser.close()


getSerial()
