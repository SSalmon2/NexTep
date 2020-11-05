from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from PyQt5.QtGui import QIcon, QCursor

import qtawesome
from Dance_ex import *

class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.windowList = []
        self.init_ui()

    def init_ui(self):

        self.setFixedSize(800, 800)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        '''
        左侧菜单模块
        '''

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_visit.clicked.connect(self.MAx_show)
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(self.Min_show)

        self.left_label_2 = QtWidgets.QPushButton("My Vedio")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("Contact and Help")
        self.left_label_3.setObjectName('left_label')

        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "Local Video")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "Download Management")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), " My Collection")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "Feedback")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "Follow us")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "Problems")
        self.left_button_9.setObjectName('left_button')

        self.left_button_0 = QtWidgets.QPushButton(qtawesome.icon('fa.list-ol', color='white'), "Ranking")
        self.left_button_0.setObjectName('left_button')
        self.left_button_0.clicked.connect(self.chick_ranking)

        self.left_xxx = QtWidgets.QPushButton(" ")

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)

        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        # self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_0, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 12, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 13, 0, 1, 3)

        '''
        搜索模块


        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索 ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入歌手、歌曲或用户，回车进行搜索")

        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        '''

        '''
            今日推荐模块
        '''
        self.right_recommend_label = QtWidgets.QLabel("Recommendation")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("1.JENNIE - SOLO")  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('./Ui_images/1.JENNIE - SOLO .JPG'))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100, 100))  # 设置图标大小
        self.recommend_button_1.clicked.connect(self.chick_1video)
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("2.국민체조")
        self.recommend_button_2.setIcon(QtGui.QIcon('./Ui_images/2.국민체조.JPG'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.clicked.connect(self.chick_2video)
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("3.IDLE_덤디덤디 ")
        self.recommend_button_3.setIcon(QtGui.QIcon('./Ui_images/3.덤디덤디.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_3.clicked.connect(self.chick_3video)
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("4.Rain_깡")
        self.recommend_button_4.setIcon(QtGui.QIcon('./Ui_images/4.GANG.jpeg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_4.clicked.connect(self.chick_4video)
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_2, 0, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)

        '''
        左侧的最顶端是三个窗口控制按钮
        '''
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        '''
        左侧菜单按钮
        '''
        self.left_widget.setStyleSheet('''
        QWidget#left_widget{

        background:gray;

        border-top:1px solid white;

        border-bottom:1px solid white;

        border-left:1px solid white;

        border-top-left-radius:10px;

        border-bottom-left-radius:10px;

        }
        QPushButton{border:none;color:white;}
        QPushButton#left_label{
        border:none;
        border-bottom:1px solid white;

        font-size:18px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')

        # '''
        #  右侧背景、搜索框和模块文本
        # '''
        # self.right_bar_widget_search_input.setStyleSheet('''
        # QLineEdit{
        # border:1px solid gray;
        # width:300px;
        # border-radius:10px;
        # padding:2px 4px;}
        # ''')

        self.right_widget.setStyleSheet('''
        QWidget#right_widget{
        color:#232C51;
        background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        }
        QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')

        self.right_recommend_widget.setStyleSheet('''
        QToolButton{border:none;}
        QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        self.windowList.append(self)

    def Min_show(self):
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def MAx_show(self):
        self.setWindowState(QtCore.Qt.WindowMaximized)

    def chick_1video(self):
        video_path = "/mnt/NexTep/Main_code2/video/1.JENNIE_SOLO.mp4"
        video_csv = r"./value_csv/1.csv"
        self.on_SecondWindow_clicked(video_path, video_csv)

    def chick_2video(self):
        video_path = "/mnt/NexTep/Main_code2/video/2.webm"
        video_csv = r"./value_csv/2.csv"
        self.on_SecondWindow_clicked(video_path, video_csv)
    def chick_3video(self):
        video_path = "/mnt/NexTep/Main_code2/video/3.mp4"
        video_csv = r"./value_csv/3.csv"
        self.on_SecondWindow_clicked(video_path, video_csv)
    def chick_4video(self):
        video_path = "/mnt/NexTep/Main_code2/video/4.mp4"
        video_csv = r"./value_csv/4.csv"
        self.on_SecondWindow_clicked(video_path, video_csv)

    def chick_ranking(self):
        the_window = Ranking_window()
        self.windowList.append(the_window)
        the_window.show()

    #windowList = []

    def on_SecondWindow_clicked(self, video_path, video_csv):

        the_window = Motion_ex_window(video_path, video_csv)
        self.windowList.append(the_window)  ##注：没有这句，是不打开另一个主界面的！
        #self.close()
        the_window.show()


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

def main():
    app = QtWidgets.QApplication(sys.argv)

    gui = MainUi()

    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()