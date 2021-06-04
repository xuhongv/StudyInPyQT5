import os
import sys

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QByteArray
from Ui_MainWindow import Ui_MainWindow
from xUart.UartSerial import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from io import BytesIO
from PIL import Image

DEFAULT_BAUD_ARRAY = ('4800', '74880', '9600', '115200', '576000', '921600',)
GET_PORT_ARRAY = []

picBuff = QByteArray()

pictrureName = 'what.JPG'


def uart_callback_handler(obj):

    if obj['code'] == 1:
        print('串口异常断开')
    else:
        buff = (obj['data'])
        length = obj['length']
        picBuff.append(buff)
        if buff[length - 1] == 217 and buff[length - 2] == 255:
            print('图片 buff', (picBuff))
            # 将bytes结果转化为字节流
            bytes_stream = BytesIO(picBuff)
            # 读取到图片
            roiimg = Image.open(bytes_stream)
            imgByteArr = BytesIO()  # 初始化一个空字节流
            roiimg.save(imgByteArr, format('PNG'))  # 把我们得图片以‘PNG’保存到空字节流
            imgByteArr = imgByteArr.getvalue()  # 无视指针，获取全部内容，类型由io流变成bytes。
            img_name = '1.jpg'
            with open(os.path.join('', img_name), 'wb') as f:
                f.write(imgByteArr)
            image = QPixmap(img_name)
            ui.label.setPixmap(image)
            picBuff.clear()

def OnClickSend():
    buff = [0xF0, 0xA1]
    input_s = bytes(buff)
    mXUart.send_data(input_s)
    print("发送成功！！！")


# 刷新串口
def refreshPort():
    # 获取电脑可用的串口
    _ports = mXUart.get_all_port()
    print("_ports:", _ports)
    # 设置通信串口
    get_port_array_str = []
    for item in _ports:
        get_port_array_str.append(item)
    ui.cb_ports.clear()
    GET_PORT_ARRAY.clear()
    if len(_ports) == 0:
        ui.cb_ports.addItem('')
    else:
        for item in _ports:
            ui.cb_ports.addItem(item)
            GET_PORT_ARRAY.append(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setCentralWidget(ui.centralwidget)
    MainWindow.show()

    # 设置点击下拉框刷新电脑可用串口
    ui.cb_ports.popupAboutToBeShown.connect(refreshPort)
    ui.bt_get_pic.clicked.connect(OnClickSend)
    #  初始化mXUart
    mXUart = UartSerial()
    # 设置串口数据回调函数
    mXUart.setCallBack(uart_callback_handler)
    refreshPort()

    # ui.graphicsView.setScene()

    # if len(get_port_array_str) == 0:
    #     print("获取电脑没有可用的串口！！！")
    # else:
    #     # 设置通信串口，入参必须是字符串，比如 COM11
    baud = 115200
    port = 'COM3'
    #     str = '打开串口'
    #
    #     # 设置打开串口参数
    mXUart.set_default_parity(
        'N')  # PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
    mXUart.set_default_stopbits(1)  # STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
    mXUart.set_default_bytesize(8)  # FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

    #
    #     if str == '关闭串口':
    #         if mXUart.try_off_port(port, baud):
    #             print("关闭串口成功！！！")
    #         else:
    #             print('错误信息', '串口被占用或已拔开，无法打开')
    #     if str == '打开串口':
    #         if mXUart.try_port_open(port, baud):
    #             print("打开串口成功：", port)
    #         else:
    #             print('错误信息', '串口被占用或已拔开，无法打开')

    if mXUart.try_port_open(port, 115200):
        print("打开串口成功：", port)
    else:
        print('错误信息', '串口被占用或已拔开，无法打开')

    sys.exit(app.exec_())
