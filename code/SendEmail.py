from tkinter import *
from PIL import Image
from picamera import PICamera, Color
from time import sleep
from gpiozero import Button
import dlib

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

detector = dlib.get_frontal_face_detector()

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
sticker_img = cv2.imread('imgs/cat.png', cv2.IMREAD_UNCHANGED)

# 전체 프레임
back_frame = tk.Frame(root, width=1920, height=900, bg="white")
back_frame.pack()

# 버튼, 로고 등의 프레임
left_frame = tk.Frame(back_frame, bg='white', borderwidth=2, relief="solid")
left_frame.pack(side="left", padx=10, pady=10)

# 사진 프레임
right_frame = tk.Frame(back_frame, bg='white')
right_frame.pack(side="right", padx=10, pady=10)

#사용할 폰트 설정
font = tkinter.font.Font(family="맑은 고딕", size=20)

# 초기 사진 설정
imgs = [0 for i in range(4)]
global imgLabels
imgLabels = [0 for i in range(4)]
index = [[0,0], [0,1], [1,0], [1,1]]

for i in range(len(imgs)):
    imgs[i] = tk.PhotoImage(file="/home/pi/Desktop/Img/back" + "1,2,3,4".split(".")[i] + ".png")
    imgLabels[i] = tk.Label(right_frame, bg="black", image=imgs[i])
    imgLabels[i].grid(row=index[i][0], column=index[i][1], padx=10, pady=10)

# 로고, 버튼 등 설정
Label(left_frame, text="AI PHOTO", background="white", fg="black", font=font, borderwidth=1, relief="solid").grid(row=0, column=0, ipadx=73)

logoImg = tk.PhotoImage(file="/home/pi/Desktop/Img/image/logo.png")
logo = tk.Label(left_frame, bg="white", image=logoImg, borderwidth=1, relief="solid")
logo.grid(row=1, column=0, ipadx=33)

tool_bar = tk.Frame(left_frame, bg="white", borderwidth=1, relief="solid", width=100)
tool_bar.grid(row=2, column=0)

group = IntVar()

rbtns = [0 for i in range(5)]

# 카메라 프리뷰와 카메라 실시간 크로마키
def cap():
    global cnt
    global imgLabels
    global capPath
    global backPath
    global resultPath
    
    if(cnt > 3):
        cnt = 0

    #찍은 사진의 경로
    capPath = "/home/pi/Desktop/Img/capPath.png"

    #opencv 켜기, 설정
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 실시간으로 크로마키 값을 바꿀 플래그 변수 
    flag = False
    flag2 = False
    
    def nothing(x):
        pass
    
    # 크로마키 값 바꾸기 위한 트랙바를 넣을 프레임
    panel = np.zeros([100,400], np.uint8)
    
    while True:
        
        #실시간 카메라 영상을 불러옴
        ret, frame = cap.read()

        #카메라 좌우반전
        frame = cv2.flip(frame, 1)

        #카메라 해상도 설정
        frame = cv2.resize(frame, (750, 450))
        
            
        ret, img = cap.read()
        
        if ret == False:
            break
        
        dets = detector(img)
        print('number of face : ', len(dets))
        
        for det in dets:
            print(det)
            
            x1 = det.left() - 40
            y1 = det.top() - 50
            x2 = det.right() + 40
            y2 = det.bottom() + 30
            
            try:
                overlay_img = sticker_img.copy()
                overlay_img = cv2.resize(overlay_img, dsize=(x2-x1,y2-y1))
                overlay_alpha = overlay_img[:, :, 3:4] / 255.0
                background_alpha = 1.0 - overlay_alpha
                img[y1:y2, x1:x2] = overlay_alpha * overlay_img[:, :, :3] + background_alpha * img[y1:y2, x1:x2]
            except:
                pass
        
        cv2.imshow('result', img)

        #찍은 사진 내보내기
        cv2.imwrite(capPath, frame)
        
        # 찍은 사진과 배경으로 쓸 사진 불러오기
        img = cv2.imread(capPath)
        window = cv2.imread(backPath)
        window = cv2.resize(window, (750,450))
                        
        # 입력받은 키 값
        imsi = (cv2.waitKey(30) & 0xFF)
        
        # 발판 값 읽어 옴
        inputIO = GPIO.input(17)
        
        if imsi == ord('x'):
            if flag == True:
                flag = False
            else:
                flag = True
            
        # 발판을 누르면
        if inputIO == 0:
            # 사진 추출
            cv2.imwrite(resultPath[cnt], frame)
            break
        
        if imsi == ord('c'):
            # 모든 창 닫기
            cv2.destroyAllWindows()
            break
                       
        cap.release()
        cv2.destroyAllWindows()
    
# 메일로 사진 보내는 함수
def send():
    global txtbox
    global cnt
    global resultPath
    
    txt = txtbox.get("1.0", "end")
    
    gmail_smtp = "smtp.gmail.com"  #gmail smtp 주소
    gmail_port = 465 #gmail smtp 포트번호
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    my_id = "kko20_s23_20708@gclass.ice.go.kr"
    my_password = "dlskduddlskdud"
    
    smtp.login(my_id, my_password)
    msg = MIMEMultipart()
    msg.set_charset('utf-8')
    msg["Subject"] = "인공네컷 사진"
    msg["From"] = "인공네컷"
    msg["To"] = txt
    content = "인공지능전자과 201 MDP 3조 인공네컷 사진 보내드립니다"
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)
    
    for i in range(cnt):
        image_name = resultPath[i]
        with open(image_name, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', 'filename=image_name')
            msg.attach(img)
            
    to_mail = txt
    
    smtp.sendmail(my_id, txt, msg.as_string())
    smtp.quit()
    
global txtbox
txtbox = tk.Text(tool_bar, font=font, width=20, height=2)
txtbox.grid(row=5)

sendBtn = tk.Button(tool_bar, text="사진 보내기", bg="white", font=font, width=11, height=1, borderwidth=1, relief="solid", command=send)
sendBtn.grid(row=6)

root.mainloop()
