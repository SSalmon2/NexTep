# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse



class Opnenpose(object):
    def __init__(self):

        self.set_env()



    def set_env(self):

        dir_path = r"/mnt/openpose/openpose/build"
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
                #sys.path.append('D:\\Anaconda\\python');
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e


        params = dict()
        params["model_folder"] = "/mnt/openpose/openpose/models"
        params['disable_blending'] = False

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

        self.datum = op.Datum()


if __name__ == "__main__":
    OP = Opnenpose()
    cap = cv2.VideoCapture("E:\\1.TWICE(트와이스) - FEEL SPECIAL l 커버댄스 DANCE COVER  나영 NAYOUNG_Trim.mp4")
    while (cap.isOpened()):

        ret, frame = cap.read()

        if ret == True:

            OP.datum.cvInputData = frame
            OP.opWrapper.emplaceAndPop([OP.datum])

            cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", OP.datum.cvOutputData)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()



