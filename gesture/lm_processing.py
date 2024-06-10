import numpy as np

def align_points(A, B, C, points):
    # Step 1: Translate so that A is at the origin
    translation_vector = A
    translated_points = points - translation_vector
    translated_B = B - translation_vector
    translated_C = C - translation_vector
    
    # Step 2: Rotate to align B on the x-axis
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)
    
    def rotation_matrix_from_vectors(vec1, vec2):
        a, b = unit_vector(vec1), unit_vector(vec2)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[ 0, -v[2],  v[1]],
                         [ v[2],  0, -v[0]],
                         [-v[1],  v[0],  0]])
        rotation_matrix = np.eye(3) + kmat + np.dot(kmat, kmat) * ((1 - c) / (s ** 2))
        return rotation_matrix
    
    vec_AB = translated_B
    vec_x = np.array([1, 0, 0])
    R1 = rotation_matrix_from_vectors(vec_AB, vec_x)
    rotated_points = np.dot(R1, translated_points.T).T
    rotated_C = np.dot(R1, translated_C)
    
    # Step 3: Rotate around x-axis to place C in the xy-plane
    angle = np.arctan2(rotated_C[2], rotated_C[1])
    R2 = np.array([[1, 0, 0],
                   [0, np.cos(-angle), -np.sin(-angle)],
                   [0, np.sin(-angle),  np.cos(-angle)]])
    
    final_points = np.dot(R2, rotated_points.T).T / np.linalg.norm(translated_B)
    
    return final_points

def lm_to_np(lm, is_left):
    arr = np.array([[lm.landmark[i].x, lm.landmark[i].y, lm.landmark[i].z] for i in range(21)])
    if is_left:
        arr = arr * [-1, 1, 1]

    return arr

def remove_reference_points(arr):
    new_arr = np.delete(arr, 0, 0)     # remove after_tf[0]
    new_arr = np.delete(new_arr, 4, 0) # remove after_tf[5]
    return new_arr