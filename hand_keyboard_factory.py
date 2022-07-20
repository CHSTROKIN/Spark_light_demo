import mediapipe as mp
import bones
import cv2
from pynput.keyboard import Controller
import time
import state
from time import sleep
import factory
import warnings
import logs
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
        results,hand_connection =bones.get_hand_mark(image)#获取骨骼坐标
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = self.drawAll(image, self.button_list)
        cx,cy,cx2,cy2=0,0,0,0
        if results:
            for hand_marks in results:
                self.mp_drawing.draw_landmarks(image, hand_marks, hand_connection,landmark_drawing_spec=self.drawing_spec,connection_drawing_spec=self.drawing_spec1)
            img_h, img_w, img_c = image.shape
            cx, cy = int(hand_marks.landmark[8].x*img_w), int(hand_marks.landmark[8].y*img_h)#其中食指指的位置
            cx2,cy2=int(hand_marks.landmark[4].x*img_w), int(hand_marks.landmark[4].y*img_h)#其其中大拇指的位置      
        return cx,cy,cx2,cy2,image
    def process_test_key(self,frame,cx,cy,cx2,cy2):
        image=frame
        for button in self.button_list:
            x,y=button.pos
            w,h=button.size
            if((x<cx<x+w) and (y<cy<y+h)):
                cv2.rectangle(image, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)#键盘按键变大
                cv2.putText(image, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if(self.dis(cx,cx2,cy,cy2)<state.detection_margin_1):#食指大拇指合拢
                    self.keyboard.press(button.text)
                    cv2.rectangle(image, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    self.final_text += button.text
                    self.final_text = self.final_text[-12:]
                    break 
        return image   
    def process_test_put_text(self,frame):
        image=frame
        cv2.rectangle(image, (250, 350), (900, 450), (0, 255, 0), cv2.FILLED)#
        cv2.putText(image, self.final_text, (260, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)#文本输入框
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
        self.process("none")
        start=time.time()
        while(self.cap.isOpened()):
            success,image=self.cap.read()#获得帧M
            if not success:
                continue
            x,y,x1,y1,image=self.process_find_hand(image)
            image=self.process_test_key(image,x,y,x1,y1)
            image=self.process_test_put_text(image)
            end=time.time()
            image,self.fps,self.pfps,start,end=self.process_test_fps(image,self.fps,self.pfps,start,end)
            cv2.imshow('virtue keyboard', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break  
        self.cap.release()
        

if __name__=='__main__':
    hk=hand_keyboard()
    hk.run()

