import cv2
import mediapipe as mp
import random
import time

# ---------------- MEDIAPIPE ----------------
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
finger_tips = [4, 8, 12, 16, 20]
# ---------------- GAME STATE ----------------
state = "START"

toss_choice = None
toss_done = False

user_score = 0
comp_score = 0
target = None
batting = None

last_time = time.time()

user_num = -1
comp_num = -1
toss_sum = None

# ---------------- FUNCTIONS ----------------

def reset_game():
    global state, toss_choice, toss_done, user_score, comp_score, target, batting
    global last_time, user_num, comp_num, toss_sum

    state = "START"
    toss_choice = None
    toss_done = False
    user_score = 0
    comp_score = 0
    target = None
    batting = None
    last_time = time.time()
    user_num = -1
    comp_num = -1
    toss_sum = None


def get_number(lm_list):
    fingers = []

    if lm_list[4][0] > lm_list[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in [8, 12, 16, 20]:
        if lm_list[i][1] < lm_list[i-2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    mapping = {
        (0,0,0,0,0):0,
        (0,1,0,0,0):1,
        (0,1,1,0,0):2,
        (0,1,1,1,0):3,
        (0,0,1,1,1):3,
        (0,1,1,1,1):4,
        (1,1,1,1,1):5,
        (1,0,0,0,0):6
    }

    return mapping.get(tuple(fingers), -1)


# ---------------- MAIN LOOP ----------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    detected_num = -1

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm_list = []
            h, w, _ = frame.shape
            for lm in hand.landmark:
                lm_list.append((int(lm.x * w), int(lm.y * h)))
            detected_num = get_number(lm_list)
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    now = time.time()
    elapsed = now - last_time

    # ---------------- STATES ----------------

    if state == "START":
        cv2.putText(frame, "Press S to Start", (180,220),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    elif state == "TOSS_CHOICE":
        cv2.putText(frame, "Choose Toss", (220,160),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
        cv2.putText(frame, "O = ODD , E = EVEN", (160,220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    # ----------- TOSS (RUNS ONLY ONCE) -----------

    elif state == "TOSS_SHOW":

        if not toss_done:

            if elapsed < 3:
                cv2.putText(frame, str(3 - int(elapsed)), (300,220),
                            cv2.FONT_HERSHEY_SIMPLEX, 4, (0,255,255), 5)
                cv2.putText(frame, "SHOW HAND", (210,180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            else:
                if detected_num != -1:
                    user_num = detected_num
                    comp_num = random.randint(0,6)
                    toss_sum = user_num + comp_num
                    toss_done = True
                    last_time = time.time()

        else:
            cv2.putText(frame, f"You: {user_num}", (50,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(frame, f"Comp: {comp_num}", (400,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            res_str = "EVEN" if toss_sum % 2 == 0 else "ODD"
            cv2.putText(frame, f"Sum: {toss_sum} ({res_str})", (150,250),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if elapsed > 3:
                is_even = toss_sum % 2 == 0
                if (is_even and toss_choice == "EVEN") or (not is_even and toss_choice == "ODD"):
                    state = "BAT_BOWL"
                else:
                    batting = random.choice(["USER", "COMP"])
                    state = "TOSS_RESULT"
                last_time = time.time()

    elif state == "TOSS_RESULT":
        cv2.putText(frame, "Computer Won Toss!", (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        choice_text = "BAT" if batting == "COMP" else "BOWL"
        cv2.putText(frame, f"Computer chose to {choice_text}", (20,250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        if elapsed > 3:
            state = "MATCH"
            last_time = time.time()

    elif state == "BAT_BOWL":
        cv2.putText(frame, "You won Toss!", (200,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
        cv2.putText(frame, "B = Bat , W = Bowl", (170,220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    # ---------------- MATCH ----------------

    elif state == "MATCH":

        if elapsed < 2:
            cv2.putText(frame, str(2 - int(elapsed)), (300,220),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (0,255,255), 5)
        else:
            if detected_num != -1:
                user_num = detected_num
                comp_num = random.randint(0,6)
                
                # Compute result but don't update aggregate score yet
                # We show the result first
                is_out = (user_num == comp_num)
                
                state = "MATCH_RESULT"
                last_time = time.time()

    elif state == "MATCH_RESULT":
        
        cv2.putText(frame, f"You: {user_num}", (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Comp: {comp_num}", (400,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
        is_out = (user_num == comp_num)
        res_text = "OUT!" if is_out else f"runs: {user_num if batting == 'USER' else comp_num}"
        color = (0,0,255) if is_out else (0,255,0)
        
        cv2.putText(frame, res_text, (200,250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

        if elapsed > 2:
            # Process result after showing it
            if batting == "USER":
                if is_out:
                    if target: # Chasing and got out
                        state = "GAME_OVER"
                    else: # 1st innings over
                        target = user_score + 1
                        batting = "COMP"
                        # user_score stays as target reference
                        # comp_score is already 0
                        state = "MATCH"
                else:
                    user_score += user_num
                    if target and user_score >= target:
                        state = "GAME_OVER"
                    else:
                        state = "MATCH"
            else: # Batting is COMP
                if is_out:
                    if target: # Chasing and got out
                        state = "GAME_OVER"
                    else: # 1st innings over (Comp batted first)
                        target = comp_score + 1
                        batting = "USER"
                        # comp_score stays
                        # user_score is already 0
                        state = "MATCH"
                else:
                    comp_score += comp_num
                    if target and comp_score >= target:
                        state = "GAME_OVER"
                    else:
                        state = "MATCH"
            
            last_time = time.time()

    elif state == "GAME_OVER":
        text = "YOU WIN" if not (target and comp_score >= target) else "COMPUTER WINS"
        cv2.putText(frame, text, (180,220),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 4)
        cv2.putText(frame, "Press R to Restart", (160,280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    # ---------------- UI ----------------

    cv2.putText(frame, f"User: {user_score}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    cv2.putText(frame, f"Comp: {comp_score}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    if target:
        cv2.putText(frame, f"Target: {target}", (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("Hand Cricket AI", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if state == "START" and key == ord('s'):
        state = "TOSS_CHOICE"

    elif state == "TOSS_CHOICE":
        if key == ord('o'):
            toss_choice = "ODD"
            state = "TOSS_SHOW"
            last_time = time.time()
        elif key == ord('e'):
            toss_choice = "EVEN"
            state = "TOSS_SHOW"
            last_time = time.time()

    elif state == "BAT_BOWL":
        if key == ord('b'):
            batting = "USER"
            state = "MATCH"
            last_time = time.time()
        elif key == ord('w'):
            batting = "COMP"
            state = "MATCH"
            last_time = time.time()

    elif key == ord('r'):
        reset_game()

cap.release()
cv2.destroyAllWindows()
