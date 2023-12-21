import cv2
import dlib
import serial
import threading
from tkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

detector = dlib.get_frontal_face_detector()  # 얼굴 인식 모델
cap = cv2.VideoCapture(0)  # 카메라 초기화
sticker_img = cv2.imread('cat.png', cv2.IMREAD_UNCHANGED)  # 스티커 이미지 설정
photo_names = ['result1.jpg', 'result2.jpg', 'result3.jpg', 'result4.jpg']  # 찍힌 파일 저장할 곳 지정
ser = serial.Serial("COM6", 115200)
received_data2 = "No respond"

def read_serial_data2():
    global received_data2
    while True:
        received_data2 = ser.readline().decode().strip()
        print(received_data2)
        main()
    
# 이메일 설정 및 전송 함수
def sendemail():
    # 보내는 이메일 계정 설정
    sender_email = "kko20_s23_20708@gclass.ice.go.kr"
    sender_password = "wuwpdmlwzincttno"

    # 받는 이메일 주소 및 제목 설정
    receiver_email = ask_user_for_email()
    subject = "인공네컷"

    # 이메일 본문 내용
    body = "안녕하세요, 인공네컷 사진 보내드립니다."

    # 이메일 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # 본문 추가
    message.attach(MIMEText(body, "plain"))

    # 파일 첨부
    for file_name in photo_names[-4:]:  # 최근 4장의 파일만 선택
        attachment = open(file_name, "rb")  # 파일 오픈
        base = MIMEBase("application", "octet-stream")
        base.set_payload(attachment.read())
        encoders.encode_base64(base)
        base.add_header("Content-Disposition", f"attachment; filename={file_name}")
        message.attach(base) 

    # SMTP 세션 열기
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        
        # 이메일 보내기
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("이메일이 성공적으로 보내졌습니다.")


# 사용자에게 이메일을 입력받는 함수
def ask_user_for_email():
        receiver_email = input("이메일을 입력하세요: ")
        return receiver_email
    
def main():
    global cap
    if "Button1" in received_data2:

        num_photos = 4  # 찍을 사진 개수 설정
        space_counter = 0  # 스페이스바 카운터

        cap = cv2.VideoCapture(0)  # 카메라 캡처 객체 생성
        if not cap.isOpened():  # 카메라가 정상적으로 열리지 않은 경우
            print("카메라를 열 수 없습니다.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            dets = detector(frame)  # 이미지 내에서 얼굴을 감지

            for det in dets:
                x1 = det.left() - 40
                y1 = det.top() - 50
                x2 = det.right() + 40
                y2 = det.bottom() + 30

                try:
                    overlay_img = sticker_img.copy()
                    overlay_img = cv2.resize(overlay_img, dsize=(x2 - x1, y2 - y1))
                    overlay_alpha = overlay_img[:, :, 3:4] / 255.0
                    background_alpha = 1.0 - overlay_alpha
                    frame[y1:y2, x1:x2] = overlay_alpha * overlay_img[:, :, :3] + background_alpha * frame[y1:y2, x1:x2]
                except:
                    pass

            cv2.imshow('Camera', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # 'q' 키를 누르면 종료
            elif key == ord(' '):  # 스페이스바를 누르면 사진 촬영 모드
                space_counter += 1
                if space_counter <= num_photos:  # num_photos만큼의 스페이스바 입력이 있을 때
                    photo_name = f'result{space_counter}.jpg'  # 파일명 생성
                    cv2.imwrite(photo_name, frame)  # 현재 프레임을 파일로 저장
                    photo_names.append(photo_name)  # 파일명을 리스트에 추가

                    if space_counter == num_photos:  # 마지막 사진을 찍은 경우 종료
                        break
                
    elif "Button2" in received_data2:
        sendemail()

    cap.release()
    cv2.destroyAllWindows()



# 시리얼로부터 데이터를 읽고 변수에 저장합니다.
serial_thread2 = threading.Thread(target=read_serial_data2)
serial_thread2.daemon = True  
serial_thread2.start()

# 시작 화면을 띄우는 함수
def startscreen():
    w = Tk()
    w.title("screen")
    w.geometry("1260x891")

    photo = PhotoImage(file="startscreen.png")
    pLabel = Label(w, image=photo)
    pLabel.pack(expand=1, anchor=CENTER)

    w.mainloop()

startscreen()     
