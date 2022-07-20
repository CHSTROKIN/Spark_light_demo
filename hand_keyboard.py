import mediapipe as mp
import bones
import cv2
from pynput.keyboard import Controller
import time
import state
from time import sleep
import factory
'''
操作
食指放到键盘上，键盘按键待命，键盘按键会变色
食指和拇指靠拢，按下键盘按键
'''

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
class Button():
    def __init__(self, pos:list, text:str, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
def drawAll(img, buttonList:list)->None:
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
    return img
def generate_button_list():
    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([200 + 100 * j + 50, 100 * i + 50], key))
    return buttonList
def dis(x1,x2,y1,y2):
    return ((x2-x1)**2+(y2-y2)**2)**(1/2)

if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, state.image_size[0])#x轴分辨率
    cap.set(4, state.image_size[1])#y轴分辨率
    mp_drawing = mp.solutions.drawing_utils
    keyboard = Controller()#键盘
    button_list=generate_button_list()
    fps=0
    pfps=""
    start=time.time()
    final_text=""
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    drawing_spec1 = mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
    while cap.isOpened():#摄像头打开
        success,image=cap.read()#获得帧M
        if not success:
            continue
            #忽略空白帧
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results,hand_connection =bones.get_hand_mark(image)#获取骨骼坐标
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = drawAll(image, button_list)
        if results:
            for hand_marks in results:
                mp_drawing.draw_landmarks(image, hand_marks, hand_connection,landmark_drawing_spec=drawing_spec,connection_drawing_spec=drawing_spec1)
            img_h, img_w, img_c = image.shape
            cx, cy = int(hand_marks.landmark[8].x*img_w), int(hand_marks.landmark[8].y*img_h)#其中食指指的位置
            cx2,cy2=int(hand_marks.landmark[4].x*img_w), int(hand_marks.landmark[4].y*img_h)#其其中大拇指的位置
            for button in button_list:
                x,y=button.pos
                w,h=button.size
                if((x<cx<x+w) and (y<cy<y+h)):
                    cv2.rectangle(image, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)#键盘按键变大
                    cv2.putText(image, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if(dis(cx,cx2,cy,cy2)<state.detection_margin_1):#食指大拇指合拢
                        keyboard.press(button.text)
                        cv2.rectangle(image, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(image, button.text, (x + 20, y + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        final_text += button.text
                        final_text = final_text[-12:]
                        break
        cv2.rectangle(image, (250, 350), (900, 450), (0, 255, 0), cv2.FILLED)#
        cv2.putText(image, final_text, (260, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)#文本输入框
        end=time.time()
        fps+=1
        if(end-start>=1):
            pfps=str(fps)
            state.FPS=fps
            start=end
            fps=0
        cv2.putText(image,"FPS:"+pfps, (200, 600),cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        cv2.imshow('virtue keyboard', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        
    cap.release()

