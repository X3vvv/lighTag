import socket
import codecs
import sympy
import numpy as np
from numpy import *

import serial
import serial.tools.list_ports

class lighTagAlgo:
    """
    Default Four Base Station Coordinates
    
    Note that if all four z-coordinates are the same, 
    then the x, y and z of the fourth point can be directly implied, 
    so the fourth z should be different in order to form a 3D-perceived environment
    """
    # (x,y,z) for base A
    XA, YA, ZA = 0.0, 0.0, 2.0

    # (x,y,z) for base B
    XB, YB, ZB = 0.0, 8.6, 2.0

    # (x,y,z) for base C
    XC, YC, ZC = 5.6, 8.6, 2.0

    # (x,y,z) for base D
    XD, YD, ZD = 5.6, 0.0, 2.37
    
    # (TA, TB, TC, TD) for four distances
    disArr = [0.0, 0.0, 0.0, 0.0]
    
    # (x,y,z) for the target
    coorArr = [0.0, 0.0, 0.0, 0.0]
    
    # For WIFI
    c = None
    client = None
    address = None
    
    # For serial port
    ser = None
    
    def __init__(self):
        pass
    
    def wifiConnect(self):
        """
        For WIFI connection
        """
        print("Starts to connect socket.")
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.bind(("192.168.0.119", 8234))
        self.c.listen(10)
        self.client, self.address = self.c.accept()
        
        print("Socket connected.")
        return True
        
    def serialConnect(self):
        """
        For serial port connection
        """
        self.ser = serial.Serial("/dev/cu.usbserial-110", 115200)
        if self.ser.isOpen():                        
            print("Serial port connected.")
            print(self.ser.name)
        else:
            print("Serial port failed to connect.")
            
        self.ser = serial.Serial(port="/dev/cu.usbserial-110",
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=0.5) 
        return True
        
    def wifiDisconnect(self):
        """
        For WIFI disconnection
        """
        self.client.close()
        self.c.close()
        return True
        
    def serialDisconnect(self):
        """
        For serial port disconnection
        """
        self.ser.close()
        return True
    
    def getWifiData(self):
        """
        For WIFI data
        """
        bytes = self.client.recv(1024)
        return bytes.hex()
    
    def getSerialData(self):
        """
        For serial port data
        """
        bytes = self.ser.read(16)
        return bytes.hex()
    
    def convertDistance(self, inStr):
        """Convert hex string to distance data, assign the converted result to self.disArr

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
            for i in range(0, len(inStr), 2):
                str_1 = inStr[i : i + 2]
                # m r
                if i == 0 or i == 2:
                    binary_str = codecs.decode(str_1, "hex")  # hex to ASCII code
                    arr.append(str(binary_str, "utf-8"))
                # S/N, TAG ID, Frame
                if i == 4 or i == 6 or i == 8 or i == 10:
                    arr.append(inStr[i : i + 2])

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
                    
            self.disArr = arr
            return arr[7::2]  # Return the real distance data (high 8 bits distance + low 8 bits distance)
        else:
            return -1
        
    def setDistance(self,inArr):
        """set the distance data list for debug

        Args:
            inArr (float): a list of 4 distances

        Returns:
            Boolean: True for success
        """
        self.disArr = inArr
        return True
        
    def getDistance(self):
        """return the distance data list

        Returns:
            list: [TA,TB,TC,TD]
        """
        return self.disArr
    
    def calculateTriPosition(self):
        """Calculate the coordinates of the tag using the three base stations coordinates and the distance data, assign the result to self.coorArr

        Args:
            xP (float): x coordinate of the base station P
            yP (float): y coordinate of the base station P
            dP (float): distance between the tag and the base station P
            ...

        Returns:
            arr (float[]): An array of length 2 containing the coordinates of the tag: [x, y]
        """
        xa, ya, da, xb, yb, db, xc, yc, dc = (self.XA, self.YA, self.disArr[0], 
                                            self.XB, self.YB, self.disArr[1], 
                                            self.XC, self.YC, self.disArr[2])
        
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
        self.coorArr = [locx, locy]
        return [locx, locy]
    
    def calculateQuartPosition(self):
        """Calculate the coordinates of the tag using the four base stations coordinates and the distance data, assign the result to self.coorArr

        Args:
            xP (float): x coordinate of the base station P
            yP (float): y coordinate of the base station P
            zP (float): z coordinate of the base station P
            dP (float): distance between the tag and the base station P
            ...

        Returns:
            arr (float[]): An array of length 3 containing the coordinates of the tag: [x, y, z]
        """
        
        xa, ya, za, da, xb, yb, zb, db, xc, yc, zc, dc, xd, yd, zd, dd = (self.XA, self.YA, self.ZA, self.disArr[0],
                                                                          self.XB, self.YB, self.ZB, self.disArr[1],
                                                                          self.XC, self.YC, self.ZC, self.disArr[2],
                                                                          self.XD, self.YD, self.ZD, self.disArr[3])
        
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
        self.disArr = list(out)
        return list(out)
    
    
    def getCoor(self):
        """return the coordinates of the tag

        Returns:
            list: [x, y]
        """
        return self.coorArr
    
    def setBaseACoor(self,x,y,z):
        """set the coordinates of the base station A

        Args:
            x (float): x coordinate of the base station A
            y (float): y coordinate of the base station A
            z (float): z coordinate of the base station A

        Returns:
            Boolean: True for success
        """
        self.XA = x
        self.YA = y
        self.ZA = z
        return True
    
    def setBaseBCoor(self,x,y,z):
        """set the coordinates of the base station B

        Args:
            x (float): x coordinate of the base station B
            y (float): y coordinate of the base station B
            z (float): z coordinate of the base station B

        Returns:
            Boolean: True for success
        """
        self.XB = x
        self.YB = y
        self.ZB = z
        return True
    
    def setBaseCCoor(self,x,y,z):
        """set the coordinates of the base station C

        Args:
            x (float): x coordinate of the base station C
            y (float): y coordinate of the base station C
            z (float): z coordinate of the base station C

        Returns:
            Boolean: True for success
        """
        self.XC = x
        self.YC = y
        self.ZC = z
        return True
    
    def setBaseDCoor(self,x,y,z):
        """set the coordinates of the base station D

        Args:
            x (float): x coordinate of the base station D
            y (float): y coordinate of the base station D
            z (float): z coordinate of the base station D

        Returns:
            Boolean: True for success
        """
        self.XD = x
        self.YD = y
        self.ZD = z
        return True
    
    def getFourBaseCoor(self):
        """return the coordinates of the four base stations

        Returns:
            list: [xa, ya, za, xb, yb, zb, xc, yc, zc, xd, yd, zd]
        """
        return [self.XA, self.YA, self.ZA, self.XB, self.YB, self.ZB, self.XC, self.YC, self.ZC, self.XD, self.YD, self.ZD]
    
    
def test():
    lt = lighTagAlgo()
    
    lt.setBaseACoor(0,0,2.0)
    lt.setBaseBCoor(0,8.6,2.0)
    lt.setBaseCCoor(5.6,8.6,2.0)
    lt.setBaseDCoor(5.6,0.0,2.37)
    
    disArr = [5.83,5.39,4.36,3.0]
    lt.setDistance(disArr)
    
    lt.calculateTriPosition()
    lt.calculateQuartPosition()
    
    print(lt.getCoor())
    
test()
