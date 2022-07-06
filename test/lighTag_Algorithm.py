import socket
import codecs
import timeit
import sympy
import numpy as np
from numpy import *
from sympy import symbols, Eq, solve
import timeit


# Four Base Station Coordinates
XA = 0.0
YA = 0.0
ZA = 2.0

XB = 0.0
YB = 8.6
ZB = 2.0

XC = 5.6
YC = 8.6
ZC = 2.0

XD = 5.6
YD = 0.0
ZD = 1.5
"""
Note that if all four z-coordinates are the same, 
then the x, y and z of the fourth point can be directly implied, 
so the fourth z should be different in order to form a 3D-perceived environment
"""


def main():
    """main function
    Steps:
    1. Receive data from WIFI by TCP/IP
    2. Call getDis() function to convert received data to distance data
    3. Call triPosition()/quartPosition() function to calculate the 2D/3D location of the tag
    """
    
    # ######## For WIFI ########
    print("Starts to connect socket.")

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.bind(
        ("192.168.0.119", 8234)
    )
    c.listen(10)
    client, address = c.accept()

    print("Socket connected.")
    # ######## For WIFI ########

    # ######## For serial port ########
    # ser = serial.Serial("/dev/cu.usbserial-110", 115200)
    # if ser.isOpen():                        
    #     print("Serial port connected.")
    #     print(ser.name)
    # else:
    #     print("Serial port failed to connect.")

    # ser = serial.Serial(port="/dev/cu.usbserial-110",
    #                     baudrate=115200,
    #                     bytesize=serial.EIGHTBITS,
    #                     parity=serial.PARITY_NONE,
    #                     stopbits=serial.STOPBITS_ONE,
    #                     timeout=0.5) 
    # ######## For serial port ########
    
    while True:
        # Receive bytes from serial port
        # bytes = ser.read(16) 
        
        # Receive bytes from WIFI
        bytes = client.recv(1024) 
         
        print(bytes.hex())
        inDisArr = getDis(
            bytes.hex()
        )  # Convert bytes to hex string and get the distance data
        if inDisArr != -1:
            print(inDisArr)
            print(
                triPosition(
                    XA, YA, inDisArr[0], XB, YB, inDisArr[1], XC, YC, inDisArr[2]
                )
            )  # Calculate the 2D location of the tag
            print(
                quartPosition(
                    XA,
                    YA,
                    ZA,
                    inDisArr[0],
                    XB,
                    YB,
                    ZB,
                    inDisArr[1],
                    XC,
                    YC,
                    ZC,
                    inDisArr[2],
                    XD,
                    YD,
                    ZD,
                    inDisArr[3],
                )
            )  # Calculate the 3D location of the tag
        else:
            print("Error!")
        print("/n")


def getDis(inStr):
    """Convert hex string to distance data

    Args:
        inStr (String): received hex string from WIFI
        32 Bytes data from WIFI

    Returns:
        arr (float[]): An array of length 4 containing distance data: [TA, TB, TC, TD]
        or -1 if error: wrong format or received 0000
    """
    # Check if the string is valid, start with "6d72" and end with "0a0d"
    if ((inStr[0:2] == "6d") and (inStr[2:4] == "72")) and (
        (inStr[28:30] == "0a") and (inStr[30:32] == "0d")
    ):
        arr = []
        flag = 0
        for i in range(0, len(inStr), 2):
            str_1 = inStr[i : i + 2]

            # # m r
            # if i == 0 or i == 2:
            #     binary_str = codecs.decode(str_1, "hex")  # hex to ASCII code
            #     arr.append(str(binary_str, "utf-8"))

            # # S/N, TAG ID, Frame
            # if i == 4 or i == 6 or i == 8 or i == 10:
            #     arr.append(inStr[i : i + 2])

            # dis 1.hex -> dec 2. dec/100
            if (
                i == 12
                or i == 14
                or i == 16
                or i == 18
                or i == 20
                or i == 22
                or i == 24
                or i == 26
            ):  # High 8 bits (2 bytes)
                s = inStr[i : i + 2]  # Get the 2 bytes
                inInt = int(s, 16)  # hex to dec
                out = inInt / 100  # Get real distance

                if i == 14 or i == 18 or i == 22 or i == 26:  # Low 8 bits (2 bytes)
                    val = inInt << 8  # Shift 8 bits to left
                    val = val / 100  # Get real distance
                    out = (
                        val + arr[int(i / 2 - 1)]
                    )  # Add the high 8 bits distance to the low 8 bits distance to get the real distance
                    if out == 0:
                        return -1
                arr.append(out)
        return arr[
            7::2
        ]  # Return the real distance data (high 8 bits distance + low 8 bits distance)
    else:
        return -1


def triPosition(xa, ya, da, xb, yb, db, xc, yc, dc):
    """Calculate the coordinates of the tag using the three base stations coordinates and the distance data

    Args:
        xP (float): x coordinate of the base station P
        yP (float): y coordinate of the base station P
        dP (float): distance between the tag and the base station P
        ...

    Returns:
        arr (float[]): An array of length 2 containing the coordinates of the tag: [x, y]
    """
    x, y = sympy.symbols("x y")

    # List of equations
    f1 = (
        2 * x * (xa - xc)
        + np.square(xc)
        - np.square(xa)
        + 2 * y * (ya - yc)
        + np.square(yc)
        - np.square(ya)
        - (np.square(dc) - np.square(da))
    )
    f2 = (
        2 * x * (xb - xc)
        + np.square(xc)
        - np.square(xb)
        + 2 * y * (yb - yc)
        + np.square(yc)
        - np.square(yb)
        - (np.square(dc) - np.square(db))
    )

    # Solve the equations
    result = sympy.solve([f1, f2], [x, y])
    locx, locy = result[x], result[y]
    return [locx, locy]


def quartPosition(xa, ya, za, da, xb, yb, zb, db, xc, yc, zc, dc, xd, yd, zd, dd):
    """Calculate the coordinates of the tag using the four base stations coordinates and the distance data

    Args:
        xP (float): x coordinate of the base station P
        yP (float): y coordinate of the base station P
        zP (float): z coordinate of the base station P
        dP (float): distance between the tag and the base station P
        ...

    Returns:
        arr (float[]): An array of length 3 containing the coordinates of the tag: [x, y, z]
    """
    x, y, z = sympy.symbols("x y z")

    # List of equations
    f1 = (
        x * (2 * xa - 2 * xb)
        + y * (2 * ya - 2 * yb)
        + z * (2 * za - 2 * zb)
        - (
            np.square(xa)
            - np.square(xb)
            + np.square(ya)
            - np.square(yb)
            + np.square(za)
            - np.square(zb)
            - da * da
            + db * db
        )
    )
    f2 = (
        x * (2 * xa - 2 * xc)
        + y * (2 * ya - 2 * yc)
        + z * (2 * za - 2 * zc)
        - (
            np.square(xa)
            - np.square(xc)
            + np.square(ya)
            - np.square(yc)
            + np.square(za)
            - np.square(zc)
            - da * da
            + dc * dc
        )
    )
    f3 = (
        x * (2 * xa - 2 * xd)
        + y * (2 * ya - 2 * yd)
        + z * (2 * za - 2 * zd)
        - (
            np.square(xa)
            - np.square(xd)
            + np.square(ya)
            - np.square(yd)
            + np.square(za)
            - np.square(zd)
            - da * da
            + dd * dd
        )
    )

    # Solve the equations
    (out,) = sympy.linsolve([f1, f2, f3], [x, y, z])  # tuple
    rst = list(out,)
    rst[2] = rst[2] - 4.15
    return rst


def test():
    DA = 5.87
    DB = 6.01
    DC = 4.54
    DD = 4.72

    print(triPosition(XA, YA, DA, XB, YB, DB, XC, YC, DC))
    print(quartPosition(XA, YA, ZA, DA, XB, YB, ZB, DB, XC, YC, ZC, DC, XD, YD, ZD, DD))


#main()
test()

# print(timeit.timeit("test()", setup="from __main__ import test", number=100))
