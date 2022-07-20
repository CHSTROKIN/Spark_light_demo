from cv2 import FILLED
import mediapipe as mp
import bones
import cv2
from pynput.keyboard import Controller
import time
from time import sleep
import state

'''
操作
食指和中指靠拢，抬笔
食指和拇指靠拢，落笔
'''

class point:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
def dis(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y2)**2)**(1/2)
def draw_list(points:list,img):
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
if __name__=='__main__':
    point_series=[]
    cap = cv2.VideoCapture(0)
    cap.set(3, state.image_size[0])#x轴分辨率
    cap.set(4, state.image_size[1])#y轴分辨率
    mp_drawing = mp.solutions.drawing_utils
    keyboard = Controller()#键盘
    fps=0
    start=time.time()
    final_text="this is drawing demo"
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    drawing_spec1 = mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
    first=True
    drop=False
    px,py=0,0
    fps=0
    pfps=""
    t1=time.time()
    while cap.isOpened():#摄像头打开
        t2=time.time()
        success,image=cap.read()#获得帧M
        if not success:
            continue
            #忽略空白帧
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results,hand_connection =bones.get_hand_mark(image)#获取骨骼坐标
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results:
            for hand_marks in results:
                mp_drawing.draw_landmarks(image, hand_marks, hand_connection,landmark_drawing_spec=drawing_spec,connection_drawing_spec=drawing_spec1)
            img_h, img_w, img_c = image.shape
            cx, cy = int(hand_marks.landmark[8].x*img_w), int(hand_marks.landmark[8].y*img_h)#其中食指指的位置
            cx2,cy2=int(hand_marks.landmark[4].x*img_w), int(hand_marks.landmark[4].y*img_h)#其其中大拇指的位置
            cx3,cy3=int(hand_marks.landmark[12].x*img_w), int(hand_marks.landmark[12].y*img_h)#其其中中指的位置
            if(first):
                px=cx
                py=cy
                first=False
            if(dis(cx,cx2,cy,cy2)<10):#食指大拇指相触，落笔
                print("pan on is:",drop)
                point_series.append(point(-1,cy))
                drop=True
            if(dis(cx,cx3,cy,cy3)<30):#食指和中指相触，抬笔
                print("pan on is:",drop)
                drop=False
            if(drop):
                point_series.append(point(cx,cy))
        if cv2.waitKey(5) & 0xFF == 27:
            break
        if(t2-t1>=1):
            t1=t2
            state.FPS=fps
            pfps=str(fps)
            fps=0
        fps+=1
        cv2.putText(image,"pan status:"+str(drop), (260, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
        cv2.putText(image,"FPS:"+pfps, (200, 200),cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        cv2.putText(image,"thumb and index finger touch to laydown pen, middle finger and index finger touch to rise the pen", (100, 300),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        
        draw_list(point_series,image)
        cv2.imshow('virtue keyboard', image)
    cap.release()


