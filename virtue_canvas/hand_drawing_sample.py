import os,sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from cv2 import FILLED
import mediapipe as mp
import bones
import cv2
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
class hand_drawing(factory.factory):
    def __init__(self) -> None:
        super().__init__()
        self.point_series=[]
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, state.image_size[0])#x轴分辨率
        self.cap.set(4, state.image_size[1])#y轴分辨率
        self.mp_drawing = mp.solutions.drawing_utils
        self.fps=0
        self.start=time.time()
        self.final_text="this is drawing demo"
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
        self.drawing_spec1 = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
        self.first=True
        self.drop=False
        self.px,self.py=0,0
        self.fps=0
        self.pfps=""
        self.t1=time.time()
    def dis(self,x1,x2,y1,y2):
        return ((x2-x1)**2+(y2-y2)**2)**(1/2)
    def draw_list(self,points:list,img):
        px,py=0,0
        if(points):
            px=points[0].x
            py=points[0].y
        for p in range(len(points)):
            x,y=points[p].x,points[p].y
            if(x==-1 and p<len(points)-1):
                px=points[p+1].x
                py=points[p+1].y
                continue
            cv2.circle(img,(x,y),5,(0,255,0),FILLED)
            cv2.line(img,(px,py),(x,y),(255,0,0),5)
            px=x
            py=y    
    def bcurve(x1,y1,x2,y2,x3,y3):
        #贝塞尔曲线优化，同学自行填充
        pass
    def process_find_cord(self, frame):
        image=frame
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results =bones.get_hand_mark(image)#获取骨骼坐标
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image,results,state.conection
    def process_draw(self,frame,results,hand_connection):
        image=frame
        if results:
            for hand_marks in results:
                self.mp_drawing.draw_landmarks(image, hand_marks, hand_connection,landmark_drawing_spec=self.drawing_spec,connection_drawing_spec=self.drawing_spec1)
            img_h, img_w, img_c = image.shape
            cx, cy = int(hand_marks.landmark[8].x*img_w), int(hand_marks.landmark[8].y*img_h)#其中食指指的位置
            cx2,cy2=int(hand_marks.landmark[4].x*img_w), int(hand_marks.landmark[4].y*img_h)#其其中大拇指的位置
            cx3,cy3=int(hand_marks.landmark[12].x*img_w), int(hand_marks.landmark[12].y*img_h)#其其中中指的位置
            return image,cx,cy,cx2,cy2,cx3,cy3
        return image,0,0,0,0,0,0
    def process_control(self,frame,cx,cy,cx2,cy2,cx3,cy3):
            image=frame
            if(self.first):
                self.px=cx
                self.py=cy
                self.first=False
            if(self.dis(cx,cx2,cy,cy2)<10):#食指大拇指相触，落笔
                print("pan on is:",self.drop)
                self.point_series.append(point(-1,cy))
                self.drop=True
            if(self.dis(cx,cx3,cy,cy3)<30):#食指和中指相触，抬笔
                print("pan on is:",self.drop)
                self.drop=False
            if(self.drop):
                self.point_series.append(point(cx,cy))
            self.draw_list(self.point_series,image)
            cv2.putText(image,"pan status:"+str(self.drop), (260, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            cv2.putText(image,"thumb and index finger touch to laydown pen, middle finger and index finger touch to rise the pen", (100, 300),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
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
            image,results,hand_connection=self.process_find_cord(image)
            image,cx,cy,cx2,cy2,cx3,cy3=self.process_draw(image,results,hand_connection)
            image=self.process_control(image,cx,cy,cx2,cy2,cx3,cy3)
            self.end=time.time()
            image,self.fps,self.pfps,self.start,self.end=self.process_test_fps(image,self.fps,self.pfps,self.start,self.end)
            cv2.imshow('virtue canvas', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break 
        self.cap.release()
        return None
if __name__=='__main__':
    hd=hand_drawing()
    hd.run()
