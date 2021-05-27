
import sys
from PyQt5 import QtWidgets
from xUart.UartSerial import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from datetime import datetime

def uart_callback_handler(obj):
    if obj['code'] == 1:
        print('串口异常断开')
    else:
        buff = (obj['data'])
        now_time = datetime.now()  # 获取当前时间
        new_time = now_time.strftime('[%H:%M:%S]')  # 打印需要的信息,依次是年月日,时分秒,注意字母大小写
        if False:
            out_s = ''
            for i in range(0, len(buff)):
                out_s = out_s + '{:02X}'.format(buff[i]) + ' '
            print(new_time, '收到数据：', out_s)
        else:
            try:
                buff = buff.decode('utf-8', 'ignore')
                print(new_time, '收到数据：', buff)
            except:
                # 乱码显示
                pass

def OnClickSend():
    buff = "Hell World"
    mXUart.send_data(buff.encode('utf-8'))
    print("发送成功！！！")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    bt_send = QtWidgets.QPushButton(MainWindow)
    bt_send.setText("点击发送")
    bt_send.clicked.connect(OnClickSend)
    MainWindow.show()

    #  初始化mXUart
    mXUart = UartSerial()
    # 设置串口数据回调函数
    mXUart.setCallBack(uart_callback_handler)

    # 获取电脑可用的串口
    all_ports = mXUart.get_all_port()
    print("获取电脑可用的串口:", all_ports)

    # 设置通信串口
    get_port_array_str = []
    for item in all_ports:
        get_port_array_str.append(item)

    if len(get_port_array_str) == 0:
        print("获取电脑没有可用的串口！！！")
    else:

        # 设置通信串口，入参必须是字符串，比如 COM11
        baud = 115200
        port = get_port_array_str[0]
        str = '打开串口'

        # 设置打开串口参数
        mXUart.set_default_parity(
            'N')  # PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
        mXUart.set_default_stopbits(1)  # STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
        mXUart.set_default_bytesize(8)  # FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
        mXUart.set_default_port(port)
        mXUart.set_default_baudrate(baud)

        if str == '关闭串口':
            if mXUart.try_off_port(port, baud):
                print("关闭串口成功！！！")
            else:
                print('错误信息', '串口被占用或已拔开，无法打开')
        if str == '打开串口':
            if mXUart.try_port_open(port, baud):
                print("打开串口成功：", port)
            else:
                print('错误信息', '串口被占用或已拔开，无法打开')

    sys.exit(app.exec_())
