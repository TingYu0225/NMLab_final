import cv2
import mediapipe as mp
import pyautogui
from math import sqrt


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


def finger_dist(thumb, index):
    return sqrt((thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2 + (thumb.y - index.y) ** 2)


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
# currentMouseX, currentMouseY = pyautogui.position()

clicked = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
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

            if results.multi_handedness[idx].classification[0].label == "Right":
                index_x = lm.landmark[8].x
                index_y = lm.landmark[8].y

                new_mouse_x = clamp(
                    map(index_x, 0.2, 0.8, 0, screen_width), 0, screen_width)
                new_mouse_y = clamp(
                    map(index_y, 0.2, 0.8, 0, screen_height), 0, screen_height)

                pyautogui.moveTo(new_mouse_x, new_mouse_y, _pause=False)

            if results.multi_handedness[idx].classification[0].label == "Left":
                left_thumb_index_dist = finger_dist(
                    world_lm.landmark[4], world_lm.landmark[8])
                if clicked and left_thumb_index_dist > 0.01:
                    clicked = False

                if not clicked and left_thumb_index_dist < 0.01:
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
