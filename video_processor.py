import cv2
import numpy as np

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    temp_output_path = "ball-tracker-raw.mp4"
    final_output_path = "ball-tracker-final.mp4"
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (w, h))

    last_known_ball_pos = None
    tracking_started = False
    tracked_cup_pos = None

    def detect_red_ball(frame):
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
            if cv2.contourArea(largest) > 100:
                x, y, w_box, h_box = cv2.boundingRect(largest)
                return (x + w_box // 2, y + h_box // 2)
        return None

    tracked_positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_ball_pos = detect_red_ball(frame)

        if not tracking_started:
            if current_ball_pos:
                last_known_ball_pos = current_ball_pos
                cv2.circle(frame, current_ball_pos, 10, (0, 255, 0), 2)
            elif last_known_ball_pos:
                tracking_started = True
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            min_distance = float('inf')
            closest_center = None

            for cnt in contours:
                if cv2.contourArea(cnt) < 300:
                    continue
                x, y, w_box, h_box = cv2.boundingRect(cnt)
                center = (x + w_box // 2, y + h_box // 2)
                if tracked_cup_pos is None:
                    distance = np.linalg.norm(np.array(center) - np.array(last_known_ball_pos))
                else:
                    distance = np.linalg.norm(np.array(center) - np.array(tracked_cup_pos))

                if distance < min_distance:
                    min_distance = distance
                    closest_center = center

            if closest_center:
                tracked_cup_pos = closest_center
                tracked_positions.append(tracked_cup_pos)
                cv2.circle(frame, tracked_cup_pos, 10, (255, 0, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    if tracked_cup_pos:
        cap = cv2.VideoCapture(temp_output_path)
        out = cv2.VideoWriter(final_output_path, fourcc, fps, (w, h))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.line(frame, (tracked_cup_pos[0]-20, tracked_cup_pos[1]-20),
                            (tracked_cup_pos[0]+20, tracked_cup_pos[1]+20), (0,0,255), 3)
            cv2.line(frame, (tracked_cup_pos[0]+20, tracked_cup_pos[1]-20),
                            (tracked_cup_pos[0]-20, tracked_cup_pos[1]+20), (0,0,255), 3)
            out.write(frame)
        cap.release()
        out.release()

    return final_output_path
            
