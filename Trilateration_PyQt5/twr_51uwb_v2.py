# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 22:08:43 2021

@author:  www.51uwb.cn
"""
import os
from qtpy import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
from PyQt5.Qt import *
from PyQt5 import *
from PyQt5.QtCore import *
import socket  # 导入 socket 模块
from threading import Thread
from threading import Timer
import datetime
from PyQt5.QtGui import QIcon, QPixmap

# 全局变量共享参考文档:http://www.videogametimes.com/article/343147.html
import globalvar

gAnthor_Node_Configure = globalvar.get_anthor()


# object has no attribute ‘setCentralWidget'
# https://www.cnblogs.com/LaoYuanStudyPython/p/12949580.html
class HuiTu(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        icon = QIcon()
        icon.addPixmap(QPixmap('Pngtree.png'))
        self.setWindowIcon(icon)

        self.graphicsView.setStyleSheet("padding: 0px; border: 0px;")  # 内边距和边界去除
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)  # 改变对齐方式
        self.graphicsView.setSceneRect(0, 0, self.graphicsView.viewport().width(),
                                       self.graphicsView.height())  # 设置图形场景大小和图形视图大小一致

        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        # 显示本机IP
        hostname = "192.168.0.113"
        # hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        self.label_ip.setText(ip)

        self.ratio = 100
        self.MAX_HISTORY = 5
        # gTag_Result =[{'short_address':0x0001,'result':[]}]
        self.gTag_Result = []
        self.gQtColor = [QtGui.QColor(QtCore.Qt.darkCyan),
                         QtGui.QColor(QtCore.Qt.black),
                         QtGui.QColor(QtCore.Qt.red),
                         QtGui.QColor(QtCore.Qt.darkGreen),
                         QtGui.QColor(QtCore.Qt.darkMagenta),
                         QtGui.QColor(QtCore.Qt.darkRed),
                         QtGui.QColor(QtCore.Qt.gray),
                         QtGui.QColor(QtCore.Qt.green),
                         QtGui.QColor(QtCore.Qt.blue),
                         QtGui.QColor(QtCore.Qt.cyan)]

        self.tcp_server = TCP_SERVER()
        self.tcp_server.data_result.connect(insert_result)
        self.tcp_server.data_draf.connect(self.do_insert_log)

        self.pushButton.clicked.connect(self.do_tcp_server_start)
        self.btn_clear.clicked.connect(self.do_btn_clear)
        self.btn_start.clicked.connect(self.do_btn_start_log)

        self.spinBox.valueChanged.connect(self.do_adjust_maxhistory)
        #        self.spinBox.setReadOnly(True)

        self.label_port_state.setStyleSheet('color: red')
        self.table_anthor.setAlternatingRowColors(True)

        self.table_tag.setAlternatingRowColors(True)
        self.edit_log.setMaximumBlockCount(1000)  # log box 函数限制
        self.enable_log = False

    def compute_ratio(self, width, heigh, Anthor_Node_Configure):
        max_data_x = 0
        max_data_y = 0
        for item in Anthor_Node_Configure:
            if item['enable'] == 1:
                if item['x'] > max_data_x:
                    max_data_x = item['x']
                if item['y'] > max_data_y:
                    max_data_y = item['y']
        print("MAX_X =%0.2f MAX_Y = %0.2f" % (max_data_x, max_data_y))
        ratio_x = int(width / (max_data_x + 1))
        ratio_y = int(heigh / (max_data_y + 1))

        if ratio_x > ratio_y:
            ratio = ratio_y
        else:
            ratio = ratio_x
        ratio = int(ratio * 0.9)

        print("width = %d heigh = %d" % (width, heigh))
        print("RATIO_X = %d RATIO_Y = %d RATIO = %d" % (ratio_x, ratio_y, ratio))
        return ratio

    def Display_Anthor(self, Anthor_Node_Configure):
        #        global ratio
        self.ratio = self.compute_ratio(self.graphicsView.viewport().width(), self.graphicsView.height(),
                                        Anthor_Node_Configure)
        heigh = self.graphicsView.height()
        width = self.graphicsView.viewport().width()
        for item in Anthor_Node_Configure:

            if item['enable'] == 0:  # 对于没有Enable的node
                continue

            x = item['x'] * self.ratio
            y = item['y'] * self.ratio
            #        print("x = %d,y = %d"%(x,y))
            Qitem = QGraphicsEllipseItem(-10, -10, 10, 10)
            if time.time() - item['time'] > 3:
                Qitem.setBrush(QBrush(QtGui.QColor(QtCore.Qt.red)))
            #            item['qt'].setPen(QPen(QtGui.QColor(QtCore.Qt.red)))
            else:
                Qitem.setBrush(QBrush(QtGui.QColor(QtCore.Qt.green)))

            Qitem.setPos(item['x'] * self.ratio + self.ratio, heigh - (item['y'] * self.ratio + self.ratio))
            self.scene.addItem(Qitem)

            self.itemHELLO = form.scene.addText("x:" + str(item['x']) + " y:" + str(item['y']))  #
            self.itemHELLO.setPos(item['x'] * self.ratio + self.ratio,
                                  heigh - (item['y'] * self.ratio + self.ratio + 15))
            item['qt'] = Qitem

        pen = QPen()
        pen.setColor(Qt.gray)
        pen.setStyle(Qt.DotLine)
        lineindex = 1
        while lineindex * self.ratio + 5 < heigh:
            LineItem = QGraphicsLineItem(0, self.ratio, width, self.ratio)
            LineItem.setPen(pen)
            LineItem.setPos(0, heigh - (lineindex * self.ratio + 5))
            form.scene.addItem(LineItem)
            lineindex = lineindex + 1
        LineItem = QGraphicsLineItem(0, self.ratio, width, self.ratio)
        LineItem.setPen(pen)
        LineItem.setPos(0, heigh - (lineindex * self.ratio + 5))
        self.scene.addItem(LineItem)

        lineindex = 0
        while lineindex * self.ratio + 5 < width:
            LineItem = QGraphicsLineItem(self.ratio, 0, self.ratio, heigh)
            LineItem.setPen(pen)
            LineItem.setPos((lineindex * self.ratio) - 5, 0)
            self.scene.addItem(LineItem)
            lineindex = lineindex + 1

    # 在table里显示
    def show_anthor_configure(self, Anthor_Node_Configure):
        index = 0
        for item in Anthor_Node_Configure:

            self.check = QtWidgets.QTableWidgetItem()
            if item['enable'] == 1:
                self.check.setCheckState(QtCore.Qt.Checked)  # 把checkBox设为未选中状态
            else:
                self.check.setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
            self.table_anthor.setItem(index, 0, self.check)  # 在(x,y)添加checkBox
            self.table_anthor.resizeColumnToContents(0)
            # checkbox居中对齐 参考https://stackoverflow.com/questions/16237708/align-checkable-items-in-qtablewidget
            #            cell_widget = QWidget()
            #            self.check = QCheckBox()
            #            self.check.setCheckState(Qt.Checked)
            #            lay_out = QHBoxLayout(cell_widget)
            #            lay_out.addWidget(self.check)
            #            lay_out.setAlignment(Qt.AlignCenter)
            #            lay_out.setContentsMargins(0,0,0,0)
            #            cell_widget.setLayout(lay_out)
            #            self.table_anthor.setCellWidget(index,0,cell_widget)

            temp = item['short_address']
            s = "0x%04X" % temp
            newItem = QTableWidgetItem(s)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_anthor.setItem(index, 1, newItem)

            temp = item['x']
            s = "%0.2f" % temp
            newItem = QTableWidgetItem(s)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_anthor.setItem(index, 2, newItem)

            temp = item['y']
            s = "%0.2f" % temp
            newItem = QTableWidgetItem(s)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_anthor.setItem(index, 3, newItem)

            temp = item['z']
            s = "%0.2f" % temp
            newItem = QTableWidgetItem(s)
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_anthor.setItem(index, 4, newItem)

            index = index + 1

    # tag 相关的方法
    def Remove_Tag_Pic(self, item):
        try:
            self.scene.removeItem(item)
        except Exception as e:
            print(e)

    def Show_Tag_Pic(self, item, point_x, point_y, color_index):
        heigh = self.graphicsView.height()
        width = self.graphicsView.viewport().width()

        Qitem = QGraphicsEllipseItem(-10, -10, 8, 8)
        Qitem.setPos(int(point_x * self.ratio + self.ratio), int(heigh - (point_y * self.ratio + self.ratio)))

        Qitem.setBrush(QBrush(self.gQtColor[color_index]))
        Qitem.setPen(QPen(self.gQtColor[color_index]))
        self.scene.addItem(Qitem)
        item['qt'] = Qitem

    # 将最新的Tag 结果显示在表格里
    def show_tag_result(self, shortaddress, avg_x, avg_y, avg_z, index):
        #    temp = item['short_address']
        s = "0x%04X" % shortaddress
        newItem = QTableWidgetItem(s)
        self.table_tag.setItem(index, 0, newItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        newItem.setForeground(QBrush(self.gQtColor[index]))

        #        temp = coor_info['x']
        s = "%0.2f" % avg_x
        newItem = QTableWidgetItem(s)
        self.table_tag.setItem(index, 1, newItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #
        #        temp = coor_info['y']
        s = "%0.2f" % avg_y
        newItem = QTableWidgetItem(s)
        self.table_tag.setItem(index, 2, newItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #
        #        temp = coor_info['z']
        s = "%0.2f" % avg_z
        newItem = QTableWidgetItem(s)
        self.table_tag.setItem(index, 3, newItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    # 在TAG Result 数组里插入一组数据，并更新图像显示和表格
    def Insert_Tag_Result(self, short_address, coor_info):  # coor_info 是一个数组["x":0,"y":12,"z":0}]
        index = 0
        for item in self.gTag_Result:
            # 下面有if 修改为while，当MAX_HISTORY 设定从大减到小，多余的标签显示结果全部删除
            while len(item['result']) >= self.MAX_HISTORY:
                # 先删除图片中显示的item，然后删除数组中保存的内容
                self.Remove_Tag_Pic(item['result'][0]['qt'])
                del (item['result'][0])


            if item['short_address'] == short_address:
                # 第一步调整透明度
                #                total = len(item['result'])
                sum_x = 0
                sum_y = 0
                item['result'].append(coor_info)

                for i in range(len(item['result'])):
                    # setOpacity 0 不透明， 1 完全透明
                    item['result'][i]['qt'].setOpacity(1 - 1 / (i + 1))
                    # 计算历史平均x 和 y
                    sum_x = sum_x + item['result'][i]['x']
                    sum_y = sum_y + item['result'][i]['y']
                avg_x = sum_x / len(item['result'])
                avg_y = sum_y / len(item['result'])
                avg_z = 0
                # 检查下面为何一个定位结果执行两边？？？
                print("avg_x = %0.2f, avg_y = %0.2f" % (avg_x, avg_y))
                # 第二步将新数据追加到数据，透明度为0
                # 显示结果用平均结果显示，这里做到类似一个均值滤波
                self.Show_Tag_Pic(coor_info, avg_x, avg_y, index % 10)  # 一共10个颜色，第十一个和第一个颜色一样

                #                self.Show_Tag_Pic(coor_info,index%10)#一共10个颜色，第十一个和第一个颜色一样
                # 在table中显示坐标信息  update in datatable
                self.show_tag_result(short_address, avg_x, avg_y, avg_z, index)
                return
            index = index + 1

        self.gTag_Result.append({'short_address': short_address, 'result': [coor_info]})
        self.Show_Tag_Pic(coor_info, coor_info['x'], coor_info['y'], index % 10)  # 一共10个颜色，第十一个和第一个颜色一样
        #        self.Show_Tag_Pic(coor_info,index%10)#第十一个和第一个颜色一样
        self.show_tag_result(short_address, coor_info['x'], coor_info['y'], 0, index)
        # update in datatable
        return

    def do_tcp_server_start(self):
        if self.pushButton.text() == "OPEN":
            #            port = int(self.lineEdit_Port.text())
            self.tcp_server.tcp_init(int(self.lineEdit_Port.text()))
            self.lineEdit_Port.setReadOnly(True)
            # 新开一个线程，用于接收新连接
            thread = Thread(target=self.tcp_server.accept_client)  # 开启线程的函数不能加括号！！！
            thread.setDaemon(True)
            thread.start()

            self.pushButton.setText("CLOSE")
            self.label_port_state.setText("TCP Status:端口已经打开！")

            self.font = self.label_port_state.font()
            self.label_port_state.setStyleSheet('color: green')
            self.font.setBold(True)
            self.label_port_state.setFont(self.font)
            # 每次重新连接TCP，清理已经保存的tag结果
            self.gTag_Result = []
            self.scene.clear()

            self.gTag_Result = []
            self.table_tag.clearContents()
            #
            self.Display_Anthor(gAnthor_Node_Configure)
            #
            # # lock anthor and tag table
            # self.do_lock_Table()
            return

        if self.pushButton.text() == "CLOSE":
            reply = QtWidgets.QMessageBox.question(self,
                                                   '请确认',
                                                   "是否要关闭TCP？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                #                event.accept()
                self.lineEdit_Port.setReadOnly(False)
                self.tcp_server.tcp_close()

                self.pushButton.setText("OPEN")
                self.label_port_state.setText("TCP Status:端口没有打开！")

                self.font = self.label_port_state.font()
                self.label_port_state.setStyleSheet('color: red')
                self.font.setBold(True)
                self.label_port_state.setFont(self.font)
                self.do_unlock_Table()
                # unlock anthor and tag table
            return

    def do_adjust_maxhistory(self):
        print(self.spinBox.value())
        self.MAX_HISTORY = self.spinBox.value()

    def do_btn_clear(self):
        self.edit_log.clear()

    def do_insert_log(self, input_str):
        if self.enable_log == True:
            input_str = input_str[:-1]  # TCP数据已经有换行了，appendPlainText 会额外加一个换行
            dt = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')

            self.edit_log.appendPlainText(dt + input_str)

    def do_btn_start_log(self):
        if self.btn_start.text() == "START":
            self.enable_log = True
            self.btn_start.setText("STOP")
            return
        if self.btn_start.text() == "STOP":
            self.enable_log = False
            self.btn_start.setText("START")
            return

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()


def do_table_anthor_cellChanged(row, column):
    #    print("%d %d %0.2f"%(row, column,float(form.table_anthor.item(row,column).text())))
    global gAnthor_Node_Configure

    if column == 0:
        if form.table_anthor.item(row, column).checkState():
            gAnthor_Node_Configure[row]['enable'] = 1
        else:
            gAnthor_Node_Configure[row]['enable'] = 0
    if column == 1:
        gAnthor_Node_Configure[row]['short_address'] = int(form.table_anthor.item(row, column).text(), 16)

    if column == 2:
        gAnthor_Node_Configure[row]['x'] = float(form.table_anthor.item(row, column).text())
    if column == 3:
        gAnthor_Node_Configure[row]['y'] = float(form.table_anthor.item(row, column).text())
    if column == 4:
        gAnthor_Node_Configure[row]['z'] = float(form.table_anthor.item(row, column).text())
    form.scene.clear()
    form.gTag_Result = []
    globalvar.set_anthor(gAnthor_Node_Configure)
    form.Display_Anthor(gAnthor_Node_Configure)


# 每隔两秒执行一次任务
# 定时器任务，用来修改基站颜色，如果长时间没有report 信息，基站颜色为红色，否则为绿色
def DrawAnthor():
    global gAnthor_Node_Configure
    for item in gAnthor_Node_Configure:

        if item['enable'] == 0:  # 对于没有Enable的node
            continue
        if time.time() - item['time'] > 3:
            item['qt'].setBrush(QBrush(QtGui.QColor(QtCore.Qt.red)))
        #            item['qt'].setPen(QPen(QtGui.QColor(QtCore.Qt.red)))
        else:
            item['qt'].setBrush(QBrush(QtGui.QColor(QtCore.Qt.green)))
    t = Timer(2, DrawAnthor)
    t.start()


from twr_main import *
import select


class TCP_SERVER(QtCore.QThread):
    data_result = QtCore.pyqtSignal(object)
    data_draf = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TCP_SERVER, self).__init__()
        self.g_socket_server = None  # 负责监听的socket
        self.thread = None
        self.socketClosed = False

    def tcp_init(self, port):
        self.g_socket_server
        self.g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    g_socket_server.bind(ADDRESS)
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        #        port = int(form.lineEdit_Port.text())
        self.port = port
        self.g_socket_server.bind((self.ip, self.port))
        self.g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        print("server start，wait for client connecting...")
        self.socketClosed = False

    def message_handle(self, client, info):
        """
        消息处理
        """
        client.sendall("connect server successfully!".encode(encoding='utf8'))
        while True:
            if self.socketClosed:
                self.g_socket_server.close()
                break
            try:
                bytes = client.recv(1024)
                msg = bytes.decode(encoding='utf8')
                print(msg+"/n")
                self.data_draf.emit(msg)  # for debug only

                [location_result, location_seq, location_addr, location_x, location_y] = twr_main(msg)
                if location_result == 1:
                    self.data_result.emit(
                        '%d %d %0.2f %0.2f' % (location_seq, location_addr, location_x, location_y))
            except Exception as e:
                print(e)
                break

    def accept_client(self):
        """
        接收新连接
        """
        while True:
            # 参考文章:https://linzgame.com/191.html
            select.select([self.g_socket_server], [], [])
            if self.socketClosed:
                self.g_socket_server.close()
                break

            client, info = self.g_socket_server.accept()  # 阻塞，等待客户端连接
            # 给每个客户端创建一个独立的线程进行管理
            self.thread = Thread(target=self.message_handle, args=(client, info))
            # 设置成守护线程
            self.thread.setDaemon(True)
            self.thread.start()

    def tcp_close(self):
        self.socketClosed = True
        self.g_socket_server.close()


def insert_result(input_str):
    strlist = input_str.split(' ')
    location_addr = int(strlist[1])
    location_x = float(strlist[2])
    location_y = float(strlist[3])
    print("insert result")
    form.Insert_Tag_Result(location_addr,
                           {"x": location_x, "y": location_y, "z": 0, "qt": QGraphicsEllipseItem(-10, -10, 10, 10)})


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = HuiTu()
    form.show_anthor_configure(gAnthor_Node_Configure)
    form.Display_Anthor(gAnthor_Node_Configure)
    form.table_anthor.cellChanged.connect(do_table_anthor_cellChanged)
    DrawAnthor()
    form.show()
    app.exec_()
