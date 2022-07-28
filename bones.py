import cv2
import mediapipe as mp
import time
from PIL import Image
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
drawing_spec1 = mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
def test():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec1)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    hands.close()
    cap.release()
def get_hand_mark(image):
    #image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    return results.multi_hand_landmarks
def render_image_bone(image):
    #image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    print(mp_hands.HAND_CONNECTIONS)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec1)
        cv2.imshow('MediaPipe Hands', image)
        cv2.waitKey(0)

if __name__=="__main__":
    image=cv2.imread("spark_light\\test.jpg")
    #cv2.imshow('img',image)
    print(get_hand_mark(image))
    render_image_bone(image)
    test()



