import os,sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from turtle import pos
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from new import *
from PIL import *
from bones import get_hand_mark
import time
import random
import numpy as np
import cv2
import state
class MyWindow(QMainWindow, Ui_detect):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
    def progress_bar(self,value):
        self.progressBar.setProperty("value", value)
    def fps(self,vlue):
        self.FPS.setProperty("value", 100.0)
    def image(self,image):
        pass
class detect_model:
    #暂未完成
    def __init__(self):
        self.model_path=""
        self.model_name="yolov5.pt"
    def detect(self,img)->list:
        x,y,w,h=0,0,0,0
        return [x,y,w,h]
    def process_img(self,image):
        x,y,w,h=self.detect(image)
        return image[x:x+w,y:y+h,:]
class bones_model:
    
    def __init__(self):
        self.model_path=""
        self.model_name="yolov5.pt"
    def detect(self,img)->list:
        #三维信息,21点
        position=[[0,0,0] for i in range(0,21)]
        res=get_hand_mark(img)
        for i in range(len(res)):
            position[i]=res[i]
        return position
        '''
    landmark 
    {
        x: 0.29452764987945557
        y: 0.6323007941246033
        z: 0.18804416060447693
    }
    '''

class classify_model:
    def __init__(self) -> None:
        self.model_path=""
        self.model_name=""
        pass
    def detect(self,img)->list:
        res=[0 for i in range(10)]#softmax regression
        return res
    

class detect_line():
    def __init__(self,windows:MyWindow,det:detect_model,clas:classify_model):
        self.wid=windows
        self.process=0
        self.det=det
        self.clas=clas
        pass
    def fps(self,value):
        pass
    def detect_process_block_1(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, state.image_size[0])#x轴分辨率
        cap.set(4, state.image_size[1])#y轴分辨率
        a=random.randint(10)
        image_path="spark_light\\hand_image\\"+str(a)+'.jpg'
        img=cv2.imread(image_path)
        self.wid(img)
        start=time.time()
        end=start
        while(end-start<=state.detect_times):
            cap = cv2.VideoCapture(0)
            success,image=cap.read()#获得帧M
            if not success:
                continue
            image=self.det.process_img(image)#定位模型获取手掌位置并裁剪图片
            res=self.clas.detect(image)#回归模型分类手势
            if(np.argmax(res)==a):#是否是同一个手势
                return True
            end=time.time()
        return False        
    def interaction(self):
        pass
    def pipeline(self):
        #这里是处理中心,处理每一个processs block。根据程序信息修改GUI，然后通过interaction 函数处理GUI传回的信息，如某个按键被按动了......
        self.detect_process_block_1()
        self.process+=25
        self.wid.progress_bar(self.process)
        self.interaction()
        self.wid.show()



        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    det=detect_line(myWin)
    myWin.progress_bar(55)
    det.pipeline()
    sys.exit(app.exec_())
