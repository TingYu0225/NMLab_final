from math import sqrt
import numpy as np

def finger_dist(f1, f2):
    return sqrt((f1.x - f2.x) ** 2 + (f1.y - f2.y) ** 2 + (f1.y - f2.y) ** 2)

def vector_angle(v1, v2):
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def get_4_finger_array(lm):
    fingers = []
    for n in range(1, 5):
        fingers.append(np.array([[lm[i+n*4+1].x, lm[i+n*4+1].y, lm[i+n*4+1].z] for i in range(4)]))
    return np.array(fingers)

def finger_is_straight(finger):
    vector0 = finger[1] - finger[0]
    vector1 = finger[2] - finger[1]
    if vector_angle(vector0, vector1) > 0.75:
        return False

    vector2 = finger[3] - finger[2]
    if vector_angle(vector1, vector2) > 0.75:
        return False
    
    return True

def is_pinch(hand_world_lm):
    return finger_dist(hand_world_lm.landmark[4], hand_world_lm.landmark[8]) < 0.02

def is_scroll(hand_lm):
    lm = hand_lm.landmark

    # check hand is facing forward
    finger_base_vector = np.array([lm[17].x - lm[5].x, lm[17].y - lm[5].y, lm[17].z - lm[5].z])
    reference_vector = np.array([1, 0, 0])
    angle_between = vector_angle(finger_base_vector, reference_vector)
    # print(angle_between)
    if angle_between > 0.75:
        print("Not facing the right direction")
        return 0

    # check each finger is straight
    fingers = get_4_finger_array(lm)

    if not (finger_is_straight(fingers[0]) and finger_is_straight(fingers[1]) and finger_is_straight(fingers[2])):
        print("Not straight")
        return 0

    # check each finger is paralell
    fin_vec_0 = (fingers[0, 3] - fingers[0, 0])[:2]
    fin_vec_1 = (fingers[1, 3] - fingers[1, 0])[:2]
    fin_vec_2 = (fingers[2, 3] - fingers[2, 0])[:2]

    if vector_angle(fin_vec_0, fin_vec_1) > 0.3 or vector_angle(fin_vec_1, fin_vec_2) > 0.3:
        print("Not paralell")
        return 0

    # determine scroll direction and speed
    print("Scroll")
    width = np.linalg.norm(finger_base_vector[:2])
    height = np.linalg.norm(fin_vec_1[:2])
    sign = -1 if fin_vec_1[1] > 0 else 1
    ratio = height / width

    if ratio > 1.8:
        print(sign)
        return sign
    
    print(0)
    return 0

def number_of_fingers(hand_lm):
    lm = hand_lm.landmark
    fingers = get_4_finger_array(lm)
    cnt = 0

    if finger_is_straight(fingers[0]):
        cnt += 1
    last_fin_vec = (fingers[0, 3] - fingers[0, 0])[:2]

    for i in range(1, 4):
        fin_vec = (fingers[i, 3] - fingers[i, 0])[:2]
        if finger_is_straight(fingers[i]) and vector_angle(fin_vec, last_fin_vec) < 0.3:
            cnt += 1
            last_fin_vec = fin_vec
        else:
            break

    return cnt


