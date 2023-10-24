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


while True:
    #실시간 카메라 영상을 불러옴
    ret, frame = cap.read()

    #카메라 좌우반전
    frame = cv2.flip(frame, 1)

    #카메라 해상도 설정
    frame = cv2.resize(frame, (750, 450))

    #찍은 사진 내보내기
    cv2.imwrite(capPath, frame)
