import cv2
import numpy as np

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('ball-tracker.mp4', fourcc, fps, (w, h))

    last_position = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            (x, y, w_box, h_box) = cv2.boundingRect(largest)
            center = (x + w_box // 2, y + h_box // 2)
            last_position = center
            cv2.circle(frame, center, 10, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    if last_position:
        cap = cv2.VideoCapture('ball-tracker.mp4')
        out = cv2.VideoWriter('ball-tracker-final.mp4', fourcc, fps, (w, h))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.line(frame, (last_position[0]-20, last_position[1]-20),
                            (last_position[0]+20, last_position[1]+20), (0,0,255), 3)
            cv2.line(frame, (last_position[0]+20, last_position[1]-20),
                            (last_position[0]-20, last_position[1]+20), (0,0,255), 3)
            out.write(frame)

        cap.release()
        out.release()

    return 'ball-tracker-final.mp4'
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        (x, y, w_box, h_box) = cv2.boundingRect(largest)
        center = (x + w_box // 2, y + h_box // 2)
        last_position = center
        cv2.circle(frame, center, 10, (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release()

if last_position:
    cap = cv2.VideoCapture('ball-tracker.mp4')
    out = cv2.VideoWriter('ball-tracker-final.mp4', fourcc, fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.line(frame, (last_position[0]-20, last_position[1]-20),
                        (last_position[0]+20, last_position[1]+20), (0,0,255), 3)
        cv2.line(frame, (last_position[0]+20, last_position[1]-20),
                        (last_position[0]-20, last_position[1]+20), (0,0,255), 3)
        out.write(frame)

    cap.release()
    out.release()

return 'ball-tracker-final.mp4'
  
