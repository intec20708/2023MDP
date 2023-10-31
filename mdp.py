from tkinter import *
from PIL import Image
from picamera import PICamera, Color
from time import sleep
from gpiozero import Button

#메일을 보내기 위한 라이브러리
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import tkinter as tk
import tkinter.font
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import os
import smtplib
import tensorflow as tf

#버튼 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

#GUI 창 띄우기
root = Tk() #create root window
root.time("Basic GUI Layout")
root.geometry("1920x1080") #title of the GUI window
root.maxsize(2000, 2000) #specify the max size the window can expand to
root.config(bg="white") #specify background color

#전역 변수들
global backPath
Button = Button(17)
global cnt
global capPath
global resultPath

resultPath = ["/home/pi/Desktop/Img/result1.png", "/home/pi/Desktop/Img/result2.png", "/home/pi/Desktop/Img/result3.png", "/home/pi/Desktop/Img/result4.png"]
cnt = 0

#사용할 폰트 설정
font = tkinter.font.Font(family="맑은 고딕", size=20)

#찍은 사진의 경로
capPath = "/home/pi/Desktop/Img/capPath.png"

#opencv 켜기, 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# TensorFlow 모델 로드
model = tf.keras.applications.MobileNetV2(weights="imagenet")
target_size = (224, 224)

# 객체 인식 함수 정의
def detect_objects_from_camera():
    cap = cv2.VideoCapture(0)  # 카메라 열기

    while True:
        ret, frame = cap.read()  # 프레임 읽기

        if not ret:
            break

        # 프레임 크기 조정 및 전처리
        frame = cv2.resize(frame, target_size)
        input_data = np.expand_dims(frame, axis=0)
        input_data = tf.keras.applications.mobilenet.preprocess_input(input_data)

        # 객체 인식
        predictions = model.predict(input_data)

        # 결과를 화면에 표시
        decoded_predictions = tf.keras.applications.mobilenet.decode_predictions(predictions)
        object_name = decoded_predictions[0][0][1]  # 가장 확률이 높은 객체의 이름
        cv2.putText(frame, object_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 함수 호출하여 객체 인식 실행
detect_objects_from_camera()

while True:
    #실시간 카메라 영상을 불러옴
    ret, frame = cap.read()

    #카메라 좌우반전
    frame = cv2.flip(frame, 1)

    #카메라 해상도 설정
    frame = cv2.resize(frame, (750, 450))

    #찍은 사진 내보내기
    cv2.imwrite(capPath, frame)

    #찍은 사진과 배경으로 쓸 사진 불러오기
    img = cv2.imread(capPath)
    window = cv2.imread(backPath)
    window = cv2.resize(window, (750, 450))

    #발판 값 읽어 오기
    inputIO = GPIO.input(17)

    if imsi == ord('x'):

        if flag == True:
            flag == False
        else:
            flag = True
    #발판을 누루면
    if inputIO == 0:
        #사진 추출
        cv2.imwrite(resultPath[cnt], frame)
        break

    if imsi == ord('c'):
        #모든 창 닫기
        cv2.destoryAllWindows()
        break

    if flag == True:

        if flag2 == False:
            cv2.namedWindow('panel')

        cv2.resize(panel, (750, 450))
        cv2.imshow('panel', panel)
    
    cap.release()
    cv2.destroyAllWindows()

#메일로 사진을 보내는 함수
def send():

    global txtbox
    global cnt
    global resultPath

    txt = txtbox.get("1.0", "end")

    gmail_smtp = "smtp.gmail.com"  #gmail smtp 주소
    gmail_port = 465  #포트 번호
    smpt = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    my_id = "kko20_s23_20708@gclass.ice.go.kr"
    my_password = "dlskduddlskdud"
    smpt.login(my_id, my_password)
    msg = MIMEMultipart()
    msg.set_charset('utf-8')
    msg["Subject"] = "사진 보내드립니다."
    msg["From"] = "인공2-1-3"
    msg["To"] = txt
    content = "안녕하세요 인공지능전자과 201 MDP 3조에서 사진 보내드립니다."
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    for i in range(cnt):

        image_name = resultPath[i]
        with open(image_name, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition','attachment', filename = image_name)
            msg.attach(img)

    to_mail = txt

    smpt.sendmail(my_id, txt, msg.as_string())
    smpt.quit()

global txtbox
txtbox = tk.Text(tool_bar, font=font, width=20, height=2)
txtbox.grid(row=5)

sendBtn = tk.Button(tool_bar, text="사진 보내기", bg="white", font=font, width=11, height=1, borderwidth=1, relief="solid", command=send)
sendBtn.grid(row=6)

root.mainloop()
