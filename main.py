import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame

# Setup MediaPipe Hands Tasks API
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

video = cv2.VideoCapture(0)

pygame.mixer.init()
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)

video.set(3, 1000)
video.set(4, 780)

img_1 = cv2.imread('magic_circles/magic_circle_cw.png', -1)
img_2 = cv2.imread('magic_circles/magic_circle_cw.png', -1)

deg = 0

def get_position_data(lmlist):
    wrist = (lmlist[0][0], lmlist[0][1])
    thumb_tip = (lmlist[4][0], lmlist[4][1])
    index_mcp = (lmlist[5][0], lmlist[5][1])
    index_tip = (lmlist[8][0], lmlist[8][1])
    midle_mcp = (lmlist[9][0], lmlist[9][1])
    midle_tip = (lmlist[12][0], lmlist[12][1])
    ring_tip = (lmlist[16][0], lmlist[16][1])
    pinky_tip = (lmlist[20][0], lmlist[20][1])
    return wrist, thumb_tip, index_mcp, index_tip, midle_mcp, midle_tip, ring_tip, pinky_tip


def draw_line(img, p1, p2, size=5):
    cv2.line(img, p1, p2, (50, 50, 255), size)
    cv2.line(img, p1, p2, (255, 255, 255), round(size / 2))


def calculate_distance(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1.0 / 2)
    return length


def transparent(img, targetImg, x, y, size=None):
    if size is not None:
        targetImg = cv2.resize(targetImg, size)

    newFrame = img.copy()
    b, g, r, a = cv2.split(targetImg)
    overlay_color = cv2.merge((b, g, r))
    mask = cv2.medianBlur(a, 1)
    
    h, w, _ = overlay_color.shape
    roi = newFrame[y:y + h, x:x + w]

    # Make sure ROI and overlay are the same size (fixes out of bounds errors)
    if roi.shape[0] != h or roi.shape[1] != w:
        return newFrame

    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)
    newFrame[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)

    return newFrame
 

while True:
    ret, img = video.read()
    if not ret:
        break
        
    img = cv2.flip(img, 1)
    rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbimg)
    result = detector.detect(mp_image)
    
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            lmList = []
            for idx, lm in enumerate(hand_landmarks):
                h, w, c = img.shape
                coorx, coory = int(lm.x * w), int(lm.y * h)
                lmList.append([coorx, coory])

            wrist, thumb_tip, index_mcp, index_tip, midle_mcp, midle_tip, ring_tip, pinky_tip = get_position_data(lmList)
            palm = calculate_distance(wrist, index_mcp)
            distance = calculate_distance(index_tip, pinky_tip)
            ratio = distance / palm if palm > 0 else 0
            
            print(ratio)
            
            if 1.3 > ratio > 0.5:
                draw_line(img, wrist, thumb_tip)
                draw_line(img, wrist, index_tip)
                draw_line(img, wrist, midle_tip)
                draw_line(img, wrist, ring_tip)
                draw_line(img, wrist, pinky_tip)
                draw_line(img, thumb_tip, index_tip)
                draw_line(img, thumb_tip, midle_tip)
                draw_line(img, thumb_tip, ring_tip)
                draw_line(img, thumb_tip, pinky_tip)
                
            if ratio > 1.3:
                centerx = midle_mcp[0]
                centery = midle_mcp[1]
                shield_size = 3.0
                diameter = round(palm * shield_size)
                x1 = round(centerx - (diameter / 2))
                y1 = round(centery - (diameter / 2))
                
                h, w, c = img.shape
                if x1 < 0:
                    x1 = 0
                elif x1 > w:
                    x1 = w
                if y1 < 0:
                    y1 = 0
                elif y1 > h:
                    y1 = h
                if x1 + diameter > w:
                    diameter = w - x1
                if y1 + diameter > h:
                    diameter = h - y1
                    
                shield_dim = (diameter, diameter)
                ang_vel = 2.0
                deg = deg + ang_vel
                if deg > 360:
                    deg = 0
                    
                if img_1 is not None and img_2 is not None:
                    hei, wid, col = img_1.shape
                    cen = (wid // 2, hei // 2)
                    M1 = cv2.getRotationMatrix2D(cen, round(deg), 1.0)
                    M2 = cv2.getRotationMatrix2D(cen, round(360 - deg), 1.0)
                    rotated1 = cv2.warpAffine(img_1, M1, (wid, hei))
                    rotated2 = cv2.warpAffine(img_2, M2, (wid, hei))
                    
                    if diameter != 0:
                        img = transparent(img, rotated1, x1, y1, shield_dim)
                        img = transparent(img, rotated2, x1, y1, shield_dim)


    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

pygame.mixer.music.stop()
pygame.quit()

video.release()
cv2.destroyAllWindows()
