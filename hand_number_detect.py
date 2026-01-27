import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

finger_tips = [4, 8, 12, 16, 20]

score = 0
out = False
computer_num = None

last_ball_time = time.time()
countdown = 3
show_result = False

def reset_game():
    global score, out, computer_num, last_ball_time, countdown, show_result
    score = 0
    out = False
    computer_num = None
    last_ball_time = time.time()
    countdown = 3
    show_result = False


def get_number(lm_list):
    fingers = []

    if lm_list[finger_tips[0]][0] > lm_list[finger_tips[0]-1][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1, 5):
        if lm_list[finger_tips[i]][1] < lm_list[finger_tips[i]-2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0,0,0,0,0]: return 0
    if fingers == [0,1,0,0,0]: return 1
    if fingers == [0,1,1,0,0]: return 2
    if fingers == [0,1,1,1,0] or fingers == [0,0,1,1,1]: return 3
    if fingers == [0,1,1,1,1]: return 4
    if fingers == [1,1,1,1,1]: return 5
    if fingers == [1,0,0,0,0]: return 6

    return -1


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    user_num = -1

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            h, w, _ = frame.shape

            for lm in handLms.landmark:
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            user_num = get_number(lm_list)
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    current_time = time.time()
    elapsed = current_time - last_ball_time

    if not out:
        if elapsed < 3:
            countdown = 3 - int(elapsed)
            cv2.putText(frame, f"{countdown}", (280, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (0,255,255), 6)
        else:
            if not show_result and user_num != -1:
                computer_num = random.randint(0,6)

                if user_num == computer_num:
                    out = True
                else:
                    score += user_num

                show_result = True
                result_time = time.time()

            cv2.putText(frame, "SHOW!", (220, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 4)

            if show_result:
                cv2.putText(frame, f"You: {user_num}", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.putText(frame, f"Comp: {computer_num}", (20, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if time.time() - result_time > 1.5:
                    last_ball_time = time.time()
                    show_result = False

    cv2.putText(frame, f"Score: {score}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    if out:
        cv2.putText(frame, "OUT!", (240, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        cv2.putText(frame, "Press R to Restart", (180, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Hand Cricket - You Batting", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        reset_game()

cap.release()
cv2.destroyAllWindows()
