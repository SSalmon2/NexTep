# NexTep

pc에 openpose를 설치 후 MainWindow.py를 실행시키시면 됩니다.

UI쪽 제작이 서툴러서 실행하실 때 해상도를 조절하실 필요가 있습니다.

---------------------------------------------------------

코드는 MainWindow.py, Dance_ex.py의 두 코드가 있습니다. MainWindow.py는 어플리케이션 UI를 구성하는 코드이며, 피쳐 추출과 유사도 측정은 모두 Dance_ex.py 코드에서 이루어집니다.

----------------------------------------------------------

데이터 셋은 총 9 종류, 18개의 K-pop 안무 영상(공연 영상, 안무 영상) 에서 추출한

레이블 1 - 같은 K-Pop 안무에 대한 Pose 데이터 (A, B - 245쌍)

레이블 0 - 다른 K-Pop 안무에 대한 Pose 데이터 (A, B - 245쌍) 이며


해당 코드는 데이터 셋 중 80% (196쌍)의 Pose 데이터에 정규화 등의 전 처리를 진행 후,

두 영상의 X, Y, Angle 값의 산술 평균, 표준편차, 제곱평균의 값을 feature로 사용하여 머신러닝을 진행하는 코드입니다.

현재 코드는 위의 feature 중 Angle 값을 제외한 6가지 feature를 사용하여 SVM으로 학습을 진행합니다. 


