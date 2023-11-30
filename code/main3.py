import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')

cap = cv2.VideoCapture(0)
sticker_img = cv2.imread('imgs/pig.png', cv2.IMREAD_UNCHANGED)
sticker_img2 = cv2.imread('imgs/mouth.png', cv2.IMREAD_UNCHANGED)

while True:
    ret, img = cap.read()
    
    if ret == False:
        break
        
    dets = detector(img)
    
    for det in dets:
        shape = predictor(img, det)
        
        # for i, point in enumerate(shape.parts()):
        #     cv2.circle(img, center=(point.x, point.y), radius=2, color=(0, 0, 255), thickness=-1)
        #     cv2.putText(img, text=str(i), org=(point.x, point.y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)
            
        try:
            x1 = det.left()
            y1 = det.top()
            x2 = det.right()
            y2 = det.bottom()
            
            # cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)
            
            center_x = shape.parts()[4].x 
            center_y = shape.parts()[4].y - 7
            
            h, w, c = sticker_img.shape
            
            nose_w = int((x2 - x1) / 4) + 10
            nose_h = int(h / w * nose_w) 
            
            nose_x1 = int(center_x - nose_w / 2)
            nose_x2 = nose_x1 + nose_w
            
            nose_y1 = int(center_y - nose_h / 2)
            nose_y2 = nose_y1 + nose_h
            
        
            center_x2 = shape.parts()[4].x
            center_y2 = shape.parts()[4].y + 15
            
            h2, w2, c2 = sticker_img2.shape
            
            mouth_w = int((x2 - x1) / 4) + 10
            mouth_h = int(h2 / w2 * mouth_w) 
            
            mouth_x1 = int(center_x2 - mouth_w / 2)
            mouth_x2 = mouth_x1 + mouth_w
            
            mouth_y1 = int(center_y2 - mouth_h / 2)
            mouth_y2 = mouth_y1 + mouth_h
            
            overlay_img = sticker_img.copy()
            overlay_img = cv2.resize(overlay_img, dsize=(nose_w, nose_h))
            overlay_alpha = overlay_img[:, :, 3:4] / 255.0
            background_alpha = 1.0 - overlay_alpha
            img[nose_y1:nose_y2, nose_x1:nose_x2] = overlay_alpha * overlay_img[:, :, :3] + background_alpha * img[nose_y1:nose_y2, nose_x1:nose_x2]
            
            overlay_img2 = sticker_img2.copy()
            overlay_img2 = cv2.resize(overlay_img2, dsize=(nose_w, nose_h))
            overlay_alpha2 = overlay_img2[:, :, 3:4] / 255.0
            background_alpha2 = 1.0 - overlay_alpha2
            img[mouth_y1:mouth_y2, mouth_x1:mouth_x2] = overlay_alpha2 * overlay_img2[:, :, :3] + background_alpha2 * img[mouth_y1:mouth_y2, mouth_x1:mouth_x2]
            
        except:
            pass
    
    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
