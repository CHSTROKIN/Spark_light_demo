import os,sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import mediapipe as mp
import bones
import cv2
from pynput.keyboard import Controller
import time
import state
from time import sleep
import factory
import warnings
'''
操作
食指放到键盘上，键盘按键待命，键盘按键会变色
食指和拇指靠拢，按下键盘按键
'''
class Button():
    def __init__(self, pos:list, text:str, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        pass
class hand_keyboard(factory.factory):
    def __init__(self) -> None:
        super().__init__()     
        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, state.image_size[0])#x轴分辨率
        self.cap.set(4, state.image_size[1])#y轴分辨率
        self.mp_drawing = mp.solutions.drawing_utils
        self.keyboard = Controller()#键盘
        self.button_list=[]
        self.final_text=""
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
        self.drawing_spec1 = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
        self.fps=0
        self.pfps=""
    def drawAll(self,img, buttonList:list)->None:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
        return img

    def generate_button_list(self):
        buttonList = []
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                buttonList.append(Button([200 + 100 * j + 50, 100 * i + 50], key))
        return buttonList

    def dis(self,x1,x2,y1,y2):
        return ((x2-x1)**2+(y2-y2)**2)**(1/2)
        
    def process(self,frame):
        self.button_list=self.generate_button_list()
    def process_find_hand(self,frame):
        image=frame
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results =bones.get_hand_mark(image)#获取骨骼坐标
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = self.drawAll(image, self.button_list)
        cx,cy,cx2,cy2=0,0,0,0
        if results:
            for hand_marks in results:
                self.mp_drawing.draw_landmarks(image, hand_marks, state.conection,landmark_drawing_spec=self.drawing_spec,connection_drawing_spec=self.drawing_spec1)
            img_h, img_w, img_c = image.shape
            cx, cy = int(hand_marks.landmark[8].x*img_w), int(hand_marks.landmark[8].y*img_h)#其中食指指的位置
            cx2,cy2=int(hand_marks.landmark[4].x*img_w), int(hand_marks.landmark[4].y*img_h)#其其中大拇指的位置      
        return cx,cy,cx2,cy2,image
    def process_key(self,frame,cx,cy,cx2,cy2):
        '''
        self.keyboard.press("text")可以打字
        cv2.rectangle()画正方形
        cv2.putText()在图片上插入文字，只能是英文
        self.final_text是最后用户输入的文字
        state.hold=True会暂停在每帧都调用这个函数
        state.hold=False，这个函数会每帧都运行
        frame是图片，不要忘了返回图片
        cx,cy,cx2,cy2是食指和拇指的坐标
        你的任务是通过给定的参数列表来实现虚拟键盘的部分功能。
        1：实现判断按键功能。客户按下了哪个按键，最后将按键代表的字符串append到列表self.final_text中
        2：实现按键休眠功能，客户按下案件后函数需要一段时间休眠，否则键盘会一直输出
        '''
        image=frame
        return image   
    def process_put_text(self,frame):
        image=frame
        cv2.rectangle(image, (250, 350), (900, 450), (0, 255, 0), cv2.FILLED)#
        cv2.putText(image, self.final_text, (260, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)#文本输入框
        return image
    def process_fps(self, frame,fps:int,pfps:str,start:time.time,end:time.time)->list:
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
        self.process("none")
        start=time.time()
        dormant=time.time()
        dormant_cur=time.time()
        while(self.cap.isOpened()):
            success,image=self.cap.read()#获得帧M
            if not success:
                continue
            if not state.hold:
                dormant=time.time()
            if state.hold:
                dormant_cur=time.time()
            if dormant_cur-dormant>=2:
                state.hold=False
            x,y,x1,y1,image=self.process_find_hand(image)
            if(not state.hold):
                image=self.process_key(image,x,y,x1,y1)
            image=self.process_put_text(image)
            end=time.time()
            image,self.fps,self.pfps,start,end=self.process_fps(image,self.fps,self.pfps,start,end)
            cv2.imshow('virtue keyboard', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break  
        self.cap.release()
        

if __name__=='__main__':
    sys.path.append("..")
    hk=hand_keyboard()
    hk.run()

