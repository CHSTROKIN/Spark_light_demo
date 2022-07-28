import bones
import cv2
import os
import pandas as pd
from tqdm import tqdm
import sklearn

cap=cv2.VideoCapture(0)

path="spark_light\\tes"
def func(path):
    dat=[]
    os.chdir(path)
    print(os.listdir())
    for file in tqdm(os.listdir()):
        imp=path+"\\"+file
        print("_____________________")
        print(imp)
        img=cv2.imread(imp,cv2.IMREAD_COLOR)
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        cord=bones.get_hand_mark(img)
        for i in cord:
            print(i)
        dat.append(cord)
    return dat
dat5=func(path+'\\five')
dat2=func(path+"\\two")
dat0=func(path+"\\zero")
df0=pd.DataFrame([dat0])
