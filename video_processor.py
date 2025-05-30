import cv2
import numpy as np
import os

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path = "outputs/processed_video.mp4"
    os.makedirs("outputs", exist_ok=True)
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    ball_position = None
    target_cup_position = None
    tracking = False

    for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 1️⃣ البحث عن الكرة الحمراء (في أول الفريمات فقط)
        if frame_idx < 30 and ball_position is None:
            lower_red1 = np.array([0, 70, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 70, 50])
            upper_red2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask1, mask2)

            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 5:
                    ball_position = (int(x), int(y))
                    cv2.circle(frame, ball_position, int(radius), (0, 0, 255), 2)

        # 2️⃣ بعد تحديد الكرة، نبحث عن الكأس اللي غطاها
        if ball_position and not tracking:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                x, y, w_cup, h_cup = cv2.boundingRect(c)
                if x < ball_position[0] < x + w_cup and y < ball_position[1] < y + h_cup:
                    target_cup_position = (x, y, w_cup, h_cup)
                    tracking = True
                    break

        # 3️⃣ تتبع الكأس
        if tracking and target_cup_position:
            x, y, w_cup, h_cup = target_cup_position
            cv2.rectangle(frame, (x, y), (x + w_cup, y + h_cup), (255, 0, 0), 2)

        out.write(frame)

    # 4️⃣ حفظ الموقع النهائي للكأس
    if tracking and target_cup_position:
        final_x, final_y, final_w, final_h = target_cup_position
        print("📍 الكأس اللي فيه الكرة صار هون:", (final_x, final_y))

    cap.release()
    out.release()
    return output_path
                    
