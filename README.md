# 카메라 작동 코드
```
import time
import picamera

# 카메라 객체 생성
camera = picamera.PiCamera()

try:
    # 카메라 설정 (해상도, 화면 회전 등)
    camera.resolution = (1920, 1080)
    camera.rotation = 0  # 화면 회전 각도 (0, 90, 180, 270 중 선택)
    
    # 카메라 뷰파인더 표시 (필수는 아니지만 테스트 용이)
    camera.start_preview()

    # 5초 대기 후에 사진 촬영
    time.sleep(5)

    # 현재 시간을 기반으로 파일 이름 생성
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"photo_{timestamp}.jpg"

    # 사진 촬영 및 저장
    camera.capture(filename)

    # 카메라 뷰파인더 종료
    camera.stop_preview()

finally:
    # 카메라 객체 정리
    camera.close()

    
```
