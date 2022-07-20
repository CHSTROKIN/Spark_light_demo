import bones
import cv2
import os
import pandas as pd
from tqdm import tqdm
cap=cv2.VideoCapture(0)

path="D:\\IT\\PYTHON\\spark_light\\tes"
def func(path):
    os.chdir(path)
    print(os.listdir())
    dat=[]
    for file in tqdm(os.listdir()):
        imp=path+"\\"+file
        img=cv2.imread(imp,cv2.IMREAD_COLOR)
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        cord,struct=bones.get_hand_mark(img)
        dat.append(cord)
    return dat
dat=func(path+'\\five')
df=pd.DataFrame(dat)
print(df)
print(df.head(10))
print(df.shape)
df.to_csv("test.csv")
cap.release()
