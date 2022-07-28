import os,sys

from py import process
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from cv2 import FILLED
import mediapipe as mp
import bones
import cv2
from pynput.keyboard import Controller
import time
from time import sleep
import state
import factory
import warnings

'''
操作
食指和中指靠拢，抬笔
食指和拇指靠拢，落笔
'''

class point:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
class paper_scissors_stone(factory.factory):
    def __init__(self) -> None:
        super().__init__()
        self.point_series=[]
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, state.image_size[0])#x轴分辨率
        self.cap.set(4, state.image_size[1])#y轴分辨率
        self.mp_drawing = mp.solutions.drawing_utils
        self.keyboard = Controller()#键盘
        self.start=time.time()
        self.final_text="this is drawing demo"
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
        self.drawing_spec1 = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
        self.fps=0
        self.pfps=""
        self.t1=time.time()
    def dis(self,x1,x2,y1,y2):
        return ((x2-x1)**2+(y2-y2)**2)**(1/2)
    def process_gesture(self,frame):
        image=frame
        ans_list=["paper","scissors","stone"]
        '''
        想办法通过图片得出手势是剪刀，石头，还是布
        '''
        ans="paper"
        return image,ans
    def process_draw(self,frame,gesture):
        image=frame
        cv2.putText(image,gesture, (100, 200),cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        return image
    def process_test_fps(self, frame,fps:int,pfps:str,start:time.time,end:time.time)->list:
        fps+=1
        image=frame
        if(end-start>=1):
            pfps=str(self.fps)
            if(self.fps<=state.FPS):
                warnings.warn("FPS too low！")
            start=end
            fps=0
        cv2.putText(image,"FPS:"+pfps, (200, 600),cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        return image,fps,pfps,start,end


    def run(self):
        self.start=time.time()
        while self.cap.isOpened():#摄像头打开
            t2=time.time()
            success,image=self.cap.read()#获得帧M
            if not success:
                continue
                #忽略空白帧
            image,ans=self.process_gesture(image)
            image=self.process_draw(image,ans)
            self.end=time.time()
            image,self.fps,self.pfps,self.start,self.end=self.process_test_fps(image,self.fps,self.pfps,self.start,self.end)
            cv2.imshow('virtue canvas', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break 
        self.cap.release()
        return None
if __name__=='__main__':
    hd=paper_scissors_stone()
    hd.run()