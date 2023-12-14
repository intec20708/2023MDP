import cv2
# import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import dlib
import keyboard

detector = dlib.get_frontal_face_detector()
file_path = "C:/Users/user/Desktop/학교/MDP/cap"
startscreen_path = "C:/Users/user/Desktop/학교/MDP/startscreen.png"
cap = cv2.VideoCapture(0)

# 카메라로부터 사진을 찍는 함수
def capture_photo():
    # OpenCV를 사용하여 카메라로부터 사진을 찍는 코드
    cap = cv2.VideoCapture(0)

    try:
        # 카메라 설정 (해상도, 화면 회전 등)
        cap.resolution = (1920, 1080)
        
        # 카메라 뷰파인더 표시 (필수는 아니지만 테스트 용이)
        cap.start_preview()
        
        sticker_img = cv2.imread('imgs/bear.png', cv2.IMREAD_UNCHANGED)
        
        while True:
            ret, img = cap.read()
            
            if ret:
                cv2.imwrite(file_path, img)
            else:
                break
            
            dets = detector(img)
            
            for det in dets:
                        
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
            if cv2.waitKey(1) == ord('q'):
                break
            
            # 파일 이름 생성
            filename = "result1.jpg"

            # 사진 촬영 및 저장
            cap.capture(filename)

            # 카메라 뷰파인더 종료
            cap.stop_preview()

    finally:
        # 카메라 객체 정리
        cap.close()
    pass  



def on_press(key):
    if key.name == '1':  # 발판 스위치가 연결된 키를 사용. (예시-1)
        print("발판 스위치가 눌렸습니다.")
        # 발판 스위치가 눌렸을 때 수행할 동작
        capture_photo()

    keyboard.on_press(on_press)

    print("USB 발판 스위치를 대기 중입니다. 눌러보세요.")
    keyboard.wait('esc')  # 프로그램이 종료되지 않도록 대기


# 이전 사진들을 화면에 표시하는 함수
def display_previous_photos(photos):
    # 찍힌 사진을 저장할 리스트
    photos = []

    # 사진 4장 찍기
    for _ in range(4):
        ret, frame = cap.read()  # 카메라에서 프레임 읽기
        if ret:
            photos.append(frame)  # 찍은 사진을 리스트에 추가
            
    # 이미지 파일 경로 리스트 (여기서는 예시로 대체)
    image_paths = ['result1.jpg', 'result2.jpg', 'result3.jpg', 'result4.jpg']

    # 미리 찍힌 사진들을 리스트로 읽어들임
    images = [cv2.imread(image_path) for image_path in image_paths]

    # 이미지가 나란히 표시될 윈도우 생성
    cv2.namedWindow('Side-by-Side Images', cv2.WINDOW_NORMAL)

    # 이미지를 가로로 나란히 연결하여 새 이미지 생성
    side_by_side = cv2.hconcat(images)

    # 나란히 연결된 이미지를 윈도우에 표시
    cv2.imshow('Side-by-Side Images', side_by_side)

    pass  


# 사용자에게 이메일을 입력받는 함수
def ask_user_for_email():
    
    # 사용자에게 이메일 입력을 받는 코드
    receiver_email = input("이메일을 입력하세요: ")
    return receiver_email


# 이메일로 사진을 전송하는 함수
def send_photos_via_email(photos, receiver_email):

    global txtbox
    global cnt
    global resultPath
    
    txt = txtbox.get("1.0", "end")
    
    # 이메일 설정
    smtp_server = 'smtp.gmail.com' 
    smtp_port = 587  # Gmail의 경우 TLS 포트는 587입니다.
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    sender_email = "kko20_s23_20708@gclass.ice.go.kr"
    sender_password = "dlskduddlskdud"
    smtp.login(sender_email, sender_password)
    
    # 이메일 내용 설정
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "인공네컷 사진"
    content = "인공지능전자과 201 MDP 3조 인공네컷 사진 보내드립니다"
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    for i in range(cnt):
        image_name = resultPath[i]
        with open(image_name, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', 'filename=image_name')
            msg.attach(img)
                        
    smtp.sendmail(sender_email, txt, msg.as_string())
    smtp.quit()

    # 이메일 서버 연결 및 전송
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS 보안 연결 시작
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
        
       
# 모니터에 이미지를 표시하는 함수
def show_startscreen_on_monitor(startscreen):
    # 이미지 로드
    startscreen = cv2.imread("C:/Users/user/Desktop/학교/MDP/startscreen.png")

    # 이미지가 존재하는지 확인
    if startscreen is not None:
        # 이미지 윈도우 생성 및 이미지 표시
        cv2.imshow('Image Display', startscreen)
        cv2.waitKey(0)  # 사용자의 키 입력을 기다림
        cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기
    else:
        print("이미지를 찾을 수 없습니다.")



# 메인 함수 - 프로그램 시작점
def main():
    # 초기화 작업 등을 수행

    # 발판 스위치의 GPIO 핀 설정
    switch_pin = 18  # 발판 스위치의 GPIO 핀 번호 (예시)

    # # GPIO 설정
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(switch_pin, GPIO.RISING, callback=switch_pressed_callback, bouncetime=300)

    # 이미지 모니터에 특정 이미지 표시
    show_startscreen_on_monitor("C:/Users/user/Desktop/학교/MDP/startscreen.png")

    # 메인 루프
    if on_press():
        capture_photo()

    # 라즈베리 파이 GPIO 정리 (프로그램 종료 시)
    # GPIO.cleanup()
