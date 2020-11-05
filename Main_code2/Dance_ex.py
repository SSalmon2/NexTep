
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
import time
import cv2
import os
from PyQt5.QtMultimediaWidgets import QVideoWidget
import qtawesome
import functools
from MainWindow import *

import sys
from sys import platform
import argparse
from tqdm import tqdm
import numpy as np


from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import joblib
import pandas as pd

from numpy.linalg import norm
from numpy import (array, dot, arccos, clip)
import statistics
import math
from math import sqrt
from sklearn.svm import SVC
import datetime


class preprocess:
    def delcolumns(self, X):
        X = X[:, :, :2]

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    if (round(X[i, j, k], 5) == 0):
                        X[i, j, k] = np.nan
        return X

    def get_vector(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        Z = X - Y
        return Z.tolist()

    def vector_joint(self, A):
        get_vector = self.get_vector
        avlist = []

        for i in range(0, len(A)):
            vlist = []
            v1 = get_vector(A[i][6], A[i][5])
            v2 = get_vector(A[i][6], A[i][7])
            v3 = get_vector(A[i][3], A[i][2])
            v4 = get_vector(A[i][3], A[i][4])
            v5 = get_vector(A[i][13], A[i][12])
            v6 = get_vector(A[i][13], A[i][14])
            v7 = get_vector(A[i][10], A[i][9])
            v8 = get_vector(A[i][10], A[i][11])
            v9 = get_vector(A[i][5], A[i][1])
            v10 = get_vector(A[i][2], A[i][1])
            v11 = get_vector(A[i][12], A[i][8])
            v12 = get_vector(A[i][9], A[i][8])
            v13 = get_vector(A[i][1], A[i][0])
            vlist.extend(v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9 + v10 + v11 + v12 + v13)
            avlist.append(vlist)
        return avlist

    def norm_vec(self, X):
        r_list = []
        for i in range(len(X)):
            x_list = []
            y_list = []
            for j in range(len(X[i])):
                x = X[i][j]
                if j % 2 == 0:
                    x_list.append(x)
                else:
                    y_list.append(x)
            t = x_list + y_list
            r_list.append(t)
        return r_list

    def preprocessing(self, keypoint):
        df = self.delcolumns(keypoint)
        vector = self.vector_joint(df)
        # print(vector)
        norm_vector = self.norm_vec(vector)
        # print(norm_vector)
        return norm_vector


class prediction(preprocess):
    def __init__(self, model):
        self.model = joblib.load(model)

    def qmean(self, num):
        return sqrt(sum(n * n for n in num) / len(num))

    def get_feature(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        Xn = 0
        up_X = X
        up_Y = Y
        Xn = 0
        for i in range(0, 13):
            if (np.isnan(X[i]) == True) or (np.isnan(Y[i]) == True):
                up_X = np.delete(up_X, i - Xn)
                up_Y = np.delete(up_Y, i - Xn)
                Xn = Xn + 1
        Yn = 0
        for j in range(13, 26):
            if (np.isnan(X[j]) == True) or (np.isnan(Y[j]) == True):
                up_X = np.delete(up_X, j - Yn - Xn)
                up_Y = np.delete(up_Y, j - Yn - Xn)
                Yn = Yn + 1
        # print(up_X)

        Xx_vec = up_X[:13 - Xn]
        Xy_vec = up_X[13 - Xn:26 - Xn - Yn]

        Yx_vec = up_Y[:13 - Xn]
        Yy_vec = up_Y[13 - Xn:26 - Xn - Yn]
        # print("Xx_vec: ",Xx_vec)
        # print("Xy_vec: ",Xy_vec)
        # print("Yx_vec: ",Yx_vec)
        # print("Yy_vec: ",Yy_vec)

        # Xx_vec 노말라이즈
        Xx_max, Xx_min = max(Xx_vec), min(Xx_vec)
        Xx_term = Xx_max - Xx_min
        Xy_max, Xy_min = max(Xy_vec), min(Xy_vec)
        Xy_term = Xy_max - Xy_min
        for i in range(len(Xx_vec)):
            if Xx_term is not 0:
                Xx_vec[i] = (Xx_vec[i] - Xx_min) / Xx_term
        for j in range(len(Xy_vec)):
            if Xy_term is not 0:
                Xy_vec[j] = (Xy_vec[j] - Xy_min) / Xy_term
        Yx_max, Yx_min = max(Yx_vec), min(Yx_vec)
        Yx_term = Yx_max - Yx_min
        Yy_max, Yy_min = max(Yy_vec), min(Yy_vec)
        Yy_term = Yy_max - Yy_min
        for i in range(len(Yx_vec)):
            if Yx_term is not 0:
                Yx_vec[i] = (Yx_vec[i] - Yx_min) / Yx_term
        for j in range(len(Yy_vec)):
            if Yy_term is not 0:
                Yy_vec[j] = (Yy_vec[j] - Yy_min) / Yy_term

        X_dis = Xx_vec - Yx_vec
        Y_dis = Xy_vec - Yy_vec

        Xvec_std = statistics.stdev(X_dis)
        Xvec_avg = statistics.mean(X_dis)
        Xvec_rms = self.qmean(X_dis)

        Yvec_std = statistics.stdev(Y_dis)
        Yvec_avg = statistics.mean(Y_dis)
        Yvec_rms = self.qmean(Y_dis)

        flist = [Xvec_std, Xvec_avg, Xvec_rms, Yvec_std, Yvec_std, Yvec_rms]
        return flist

    def feature_list(self, preA, preB):
        features = []
        for i in range(0, len(preA)):
            flist = self.get_feature(preA[i], preB[i])
            # print(flist)
            features.append(flist)
        return features

    def score(self, keypoint_A, keypoint_B):

        preA = super().preprocessing(keypoint_A)

        preB = super().preprocessing(keypoint_B)

        features = self.feature_list(preA, preB)

        score = self.model.predict_proba(features)
        return score

class Motion_ex_window(QMainWindow):

    def __init__(self, video_path, video_csv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__init__()
        self.video_path = video_path
        self.video_csv = video_csv
        self.excount = 0
        self.gcount = 0
        self.bcount = 0
        self.total_score = 0
        self.ranking = pd.read_csv('ranking.csv')
        self.initUI()



    def initUI(self):
        self.resize(1920, 1200)

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  #
        self.setCentralWidget(self.main_widget)

        self.main_widget.setStyleSheet('''
         #main_widget{

        border-image:url(./Ui_images/blackB.jpg);

        border-radius:30px
        }

        }
        ''')

        self.gif = QMovie("./Ui_images/2.gif")
        self.scorelabel = QLabel(self.main_widget)
        self.scorelabel.setGeometry(800,700,140,70)

        self.scorelabel.setMovie(self.gif)
        self.gif.start()
        self.videoframe = QLabel(self.main_widget)
        self.videoframe.setGeometry(1000, 200, 800, 448)
        self.scoreframe = QLabel(self.main_widget)
        self.scoreframe.setGeometry(965, 712, 150, 50)


        self.scoreframe.setAlignment(Qt.AlignVCenter)

        self.th = Thread(self.video_csv)
        self.th.changePixmap.connect(self.setImage)
        self.th.score.connect(self.setText)
        #self.th.finished.connect(self.save_ranking)
        self.th.start()
        time.sleep(2)

        vw1 = QVideoWidget(self.main_widget)
        vw1.setGeometry(100, 200, 800, 448)

        player = QMediaPlayer(self.main_widget)
        player.setVideoOutput(vw1)
        player.setMedia(QMediaContent(QUrl("file:///"+self.video_path)))
        player.play()

        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        #self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.show()



    def setImage(self, image):
        self.videoframe.setPixmap(QPixmap.fromImage(image))

    def setText(self, text):
        if text == 'false':
            self.save_ranking()

            self.close()
            self.on_SecondWindow_clicked()
        else:
            if int(text) >= 80:
                self.excount += 1
                self.scoreframe.setStyleSheet("font: bold 50px;color:yellow")
            elif int(text) <50:
                self.bcount += 1
                self.scoreframe.setStyleSheet("font: bold 50px;color:red")
            else:
                self.gcount += 1
                self.scoreframe.setStyleSheet("font: bold 50px;color:white")
            self.total_score += int(text)
            self.scoreframe.setText(str(text))
    def mouseMoveEvent(self, QMouseEvent):
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
            self.m_flag = False
            self.setCursor(QCursor(Qt.ArrowCursor))

    def cap_isopend(self):
        if self.th.cap.isOpened() is False:
            print(self.th.all_score)

    def save_ranking(self):
        ok = False
        while not ok:
            player, ok = QInputDialog.getText(self, 'Save Record', '이름을 입력하세요(최대 5)')
            if len(str(player)) > 5:
                ok = False

        player = str(player)
        name = self.video_path.split('/video/')[1].split('.')[0]
        average_score = int(self.total_score/(self.excount+self.gcount+self.bcount))
        record = pd.Series([player, name, self.excount, self.gcount, self.bcount, self.total_score, average_score],
                   index=['Player', 'Name', 'Perfect', 'Good', 'Bad', 'Total Score', 'Average Score'])
        self.ranking = self.ranking.append(record, ignore_index=True)
        self.ranking.to_csv('ranking.csv', index=False)
        print("Saved!")
    windowList = []
    def on_SecondWindow_clicked(self):

        the_window = Ranking_window()
        self.windowList.append(the_window)  ##注：没有这句，是不打开另一个主界面的！
        # self.close()
        the_window.show()


class Thread(QThread):  # 采用线程来播放视频

    changePixmap = pyqtSignal(QImage)
    score = pyqtSignal(str)
    finished = pyqtSignal(int)
    #all_score  = pyqtSignal(int)
    predictor = prediction('SVM.sav')

    def __init__(self, video_csv):
        super().__init__()

        self.set_openpose_env()
        self.poseKeypoints = None

        label_1_C = pd.read_csv(video_csv)
        self.target = np.array(label_1_C.iloc[0:0 + len(label_1_C), 1:]).reshape(len(label_1_C), -1, 3)

    def set_openpose_env(self, ):

        dir_path = "/mnt/openpose/openpose/build"
        try:
            # Windows Import
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(r"E:\GitHub\openpose\build\python\openpose\Release");
                os.environ['PATH'] = os.environ[
                                         'PATH'] + ';' + "E:\\GitHub\\openpose\\build\\x64\\Release;" + 'E:\\GitHub\\openpose\\build\\bin;'
                import pyopenpose as op
            else:
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append('/usr/local/python')
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        params = dict()
        params["model_folder"] = "/mnt/openpose/openpose/models"
        params['disable_blending'] = False
        params['display'] = 0

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

        self.datum = op.Datum()

    def run(self):

        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture('/mnt/NexTep/Main_code2/video/eunseo(30).mp4')
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 448)
        self.cap.set(cv2.CAP_PROP_FPS, 10)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        #print(self.target)
        frameNum = 0
        wait = 1 / 10

        values = []
        all_values = []
        try:
            for i in range(len(self.target)):
            #for i in range(100):

                start_time = time.perf_counter()
                ret, frame = self.cap.read()

                fr = cv2.flip(frame, 1)
                if i:

                    self.datum.cvInputData = fr
                    self.opWrapper.emplaceAndPop([self.datum])
                    keypoint = []

                    if len(self.datum.poseKeypoints.flatten()) < 75:
                        #                 data= np.zeros(75).reshape(25,3)

                        #                 keypoint.append(data)
                        text = 0
                        values.append(text)
                        # retsr = cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                        rgbImage = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
                        # convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                        #                            rgbImage.shape[1] * 3, QImage.Format_RGB888)  # 在这里可以对每帧图像进行处理，
                        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                   QImage.Format_RGB888)  #
                        p = convertToQtFormat.scaled(800, 448, Qt.KeepAspectRatio)




                    else:
                        keypoint.append(self.datum.poseKeypoints[0])

                        score = self.predictor.score(self.target[i:i + 1], np.array(keypoint))

                        # print(score)
                        text = round(score[0][1] * 100)
                        values.append(text)

                        # retsr = cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

                        rgbImage = cv2.cvtColor(self.datum.cvOutputData, cv2.COLOR_BGR2RGB)
                        # convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                        #                            rgbImage.shape[1] * 3, QImage.Format_RGB888)  # 在这里可以对每帧图像进行处理，
                        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                   QImage.Format_RGB888)  #
                        p = convertToQtFormat.scaled(800, 448, Qt.KeepAspectRatio)

                    if i == 0:
                        self.changePixmap.emit(p)

                        continue


                    elapsed_microseconds = time.perf_counter() - start_time

                    delay = wait - elapsed_microseconds - 0.0014

                    if delay < 0:
                        delay = 0

                    time.sleep(delay)
                    self.changePixmap.emit(p)
                    # if len(values) >=10:
                    #     score = str(np.mean(values))
                    #     values = []
                    #
                    #     self.score.emit(score)

                    if len(values) >= 10:
                        score = str(int(np.mean(values)))
                        values = []

                        self.score.emit(score)
                    all_values.append(text)
            #print(all_values)
            self.score.emit("false")
            self.cap.release()
            #self.finished.emit(1)



        except Exception as e:
            print(e)

class Ranking_window(QMainWindow):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rank_df = pd.read_csv('ranking.csv')
        #self.rank_df = self.rank_df.sort_index(axis= 0,ascending=True,by=['Average Score'],)
        self.init_ranking_UI()
        #self.show()

    class TableModel(QAbstractTableModel):
        def __init__(self):
            QAbstractTableModel.__init__(self)
            self._data = pd.read_csv('ranking.csv')

            self._data.sort_values(by=['Total Score'], axis=0, ascending=False, inplace=True)
            self._data.index = pd.RangeIndex(len(self._data.index))
            self._data.reset_index(inplace=True)
            self._data.columns.values[0] = 'Ranking'
            self._data['Ranking'] += 1
            if len(self._data) > 15:
                self._data = self._data.head(15)

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return str(self._data.iloc[index.row(), index.column()])
            return None

        def rowCount(self, parent=None):
            return self._data.shape[0]

        def columnCount(self, parent=None):
            return self._data.shape[1]

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._data.columns[col]
            return None

    def init_ranking_UI(self):
        self.resize(1920, 1200)

        self.main_r_widget = QWidget()  # 创建窗口主部件
        self.main_r_widget.setObjectName("main_r_widget")
        self.main_r_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_r_widget.setLayout(self.main_r_layout)  #
        self.setCentralWidget(self.main_r_widget)

        self.main_r_widget.setStyleSheet('''
        #main_r_widget{
            border-image:url(./Ui_images/blackB.jpg);
            border-radius:30px;
        }
        ''')

        self.scoreboard = QLabel(self.main_r_widget)
        self.scoreboard.setText('Ranking')
        self.scoreboard.setGeometry(825, 100, 170, 100)
        self.scoreboard.setStyleSheet('font-size: 40px;'
                                      'font-weight: 900;'
                                      'color: white;')

        # self.rank_df.sort_values(by=['Total Score'],axis=0,ascending=False,inplace=True)
        # self.rank_df.reset_index(drop=True, inplace=True)
        # if len(self.rank_df) > 10:
        #     self.rank_df = self.rank_df.head(10)

        model = self.TableModel()
        self.rank_table = QTableView(self.main_r_widget)
        self.rank_table.setModel(model)
        self.rank_table.setGeometry(500, 300, 1500, 800)
        self.rank_table.resize(810, 500)
        self.rank_table.setStyleSheet("""
        #rank_table{
            color: white;
            background-color:transparent;
        }
        #rank_table::section{
            text-align: center;
        }
        """)

        # self.main_label = QLabel(self.main_r_widget)
        # self.main_label.setText('Back to Mainpage')
        # self.main_label.setGeometry(815, 170, 260, 100)
        # self.main_label.setStyleSheet('font-size: 20px;'
        #                               'font-weight: 900;'
        #                               'color: yellow;')
        self.back_main = QPushButton(self.main_r_widget)
        self.back_main.setText('Back to Mainpage')
        self.back_main.setGeometry(840, 210, 130, 40)
        self.back_main.setStyleSheet("background-color: blue;"
                                     #"margin-left: 50%;"
                                     #"margin-right: 50%;"
        )
        self.back_main.clicked.connect(self.back_to_main)

        #self.main_label.mouseClickEvent = functools.partial(Ranking_window.main_window, self.main_label)
        # self.back_main.setGeometry(825, 1100, 170, 100)
        # self.back_main.setStyleSheet('border:none;color:white;')

    def back_to_main(self):
        self.close()







if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Motion_ex_window("/mnt/NexTep/Main_code/video/2.webm",r"./value_csv/2.csv")
    win.th.quit()
    sys.exit(app.exec_())


