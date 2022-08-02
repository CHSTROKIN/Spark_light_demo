import mediapipe as mp
FPS=10
image_size=(1980,1280)
init=True
hold=False
passed=False
detection_margin_1=40#virtue keyboard中的食指和拇指之间的检测距离
sleep_time=0.1
detect_times=10
hands= mp.solutions.hands
conection=hands.HAND_CONNECTIONS
max_detection_hand_number=1
