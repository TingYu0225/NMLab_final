import cv2
import mediapipe as mp
import pyautogui
from time import sleep
from math import sqrt
from gesture import is_pinch, is_scroll, number_of_fingers
from server import start_server, is_keyboard_mode

def clamp(val, min, max):
    if val > max:
        return max
    if val < min:
        return min
    return val

def map(v, range_min, range_max, map_min, map_max):
    ratio = (v - range_min) / (range_max - range_min)
    mapped_value = map_min + (ratio * (map_max - map_min))
    return mapped_value

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,  # Use for live video
    max_num_hands=2,  # Maximum number of hands to detect
    min_detection_confidence=0.5,  # Minimum confidence value for detection
    min_tracking_confidence=0.5)  # Minimum confidence value for tracking

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Get screen size
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

clicked = False
is_dragging = False
start_x_coord = -1
start_cursor_pos = 0

scroll_sleep_duration_default = 0.1
scroll_sleep_duration = 0.1

# start server
start_server()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    # Convert the frame color from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = hands.process(frame_rgb)

    # Draw hand annotations on the frame
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(zip(results.multi_hand_landmarks, results.multi_hand_world_landmarks)):
            lm = hand_landmarks[0]
            world_lm = hand_landmarks[1]
            label = results.multi_handedness[idx].classification[0].label

            if label == 'Right' and is_keyboard_mode():
                # detect cursor drag
                if is_pinch(world_lm):
                    if is_dragging:
                        new_cursor_pos = round((lm.landmark[8].x - start_x_coord) * 30)
                        if new_cursor_pos > cursor_pos:
                            for i in range(new_cursor_pos - cursor_pos):
                                pyautogui.press('right', _pause=False)
                        else:
                            for i in range(cursor_pos - new_cursor_pos):
                                pyautogui.press('left', _pause=False)
                        cursor_pos = new_cursor_pos
                    
                    else:
                        is_dragging = True
                        start_x_coord = lm.landmark[8].x
                        cursor_pos = 0

                # detect number of fingers
                else:
                    is_dragging = False
                    finger_count = number_of_fingers(lm)

                    index_x = lm.landmark[8].x
                    index_y = lm.landmark[8].y

                    new_mouse_x = clamp(map(index_x, 0.2, 0.8, 0, screen_width), 0, screen_width)
                    new_mouse_y = (finger_count + 1) * (screen_height / 6)

                    pyautogui.moveTo(new_mouse_x, new_mouse_y, _pause=False)

            elif label == 'Right' and not is_keyboard_mode():
                # detect scroll gesture
                scroll_level = is_scroll(lm)
                if scroll_level != 0:
                    pyautogui.moveTo(screen_width / 2, screen_height / 2, _pause=False)
                    pyautogui.scroll(1 if scroll_level > 0 else -1, _pause = False)
                    sleep(scroll_sleep_duration)
                    scroll_sleep_duration = max(0, scroll_sleep_duration - 0.003)

                # otherwise, move cursor
                else:
                    scroll_sleep_duration = scroll_sleep_duration_default
                    index_x = lm.landmark[8].x
                    index_y = lm.landmark[8].y

                    new_mouse_x = clamp(map(index_x, 0.2, 0.8, 0, screen_width), 0, screen_width)
                    new_mouse_y = clamp(map(index_y, 0.2, 0.8, 0, screen_height), 0, screen_height)

                    pyautogui.moveTo(new_mouse_x, new_mouse_y, _pause=False)

            elif label == 'Left':
                # TODO: prevent clicking when scrolling
                # detect pinch
                left_pinch = is_pinch(world_lm)

                if clicked and not left_pinch:
                    clicked = False

                if not clicked and left_pinch:
                    pyautogui.click(_pause=False)
                    print("Click!")
                    clicked = True

            mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
