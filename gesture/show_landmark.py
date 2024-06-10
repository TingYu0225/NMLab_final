import matplotlib.pyplot as plt
import numpy as np

def preprocess_lm(lm, is_left):
    arr = np.array([[lm.landmark[i].x, lm.landmark[i].y, lm.landmark[i].z] for i in range(21)])
    if is_left:
        arr = arr * [-1, 1, 1]

    return arr

def plot_points(A, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot before transformation
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue', label='Before Transformation')
    for idx, point in enumerate(points):
        # ax.plot([A[0], point[0]], [A[1], point[1]], [A[2], point[2]], color='red')
        ax.text(point[0], point[1], point[2], f'{idx}', color='blue')
    
    for i in range(5):
        for j in range(3):
            start = i * 4 + j + 1
            ax.plot([points[start][0], points[start + 1][0]], [points[start][1], points[start + 1][1]], [points[start][2], points[start + 1][2]], color='red')

    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

def plot_points_2(points0, points1, points2, points3):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points0[:, 0], points0[:, 1], points0[:, 2], color='red')
    ax.scatter(points1[:, 0], points1[:, 1], points1[:, 2], color='green')
    ax.scatter(points2[:, 0], points2[:, 1], points2[:, 2], color='blue')
    ax.scatter(points3[:, 0], points3[:, 1], points3[:, 2], color='black')
    # for idx, point in enumerate(points):
    #     # ax.plot([A[0], point[0]], [A[1], point[1]], [A[2], point[2]], color='red')
    #     ax.text(point[0], point[1], point[2], f'{idx}', color='blue')
    
    for i in range(5):
        for j in range(3):
            start = i * 4 + j + 1
            ax.plot([points0[start][0], points0[start + 1][0]], [points0[start][1], points0[start + 1][1]], [points0[start][2], points0[start + 1][2]], color='red')
            ax.plot([points1[start][0], points1[start + 1][0]], [points1[start][1], points1[start + 1][1]], [points1[start][2], points1[start + 1][2]], color='green')
            ax.plot([points2[start][0], points2[start + 1][0]], [points2[start][1], points2[start + 1][1]], [points2[start][2], points2[start + 1][2]], color='blue')
            ax.plot([points3[start][0], points3[start + 1][0]], [points3[start][1], points3[start + 1][1]], [points3[start][2], points3[start + 1][2]], color='black')

    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

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

lm_arrs = np.array([[[ 2.47903794e-01,  7.16937542e-01,  4.55435014e-07],
        [ 3.11046094e-01,  7.14679718e-01, -1.66735332e-02],
        [ 3.64991605e-01,  6.79710209e-01, -1.73103828e-02],
        [ 3.99869651e-01,  6.22183144e-01, -1.77668259e-02],
        [ 4.20039415e-01,  5.62332213e-01, -1.78329460e-02],
        [ 3.47778291e-01,  5.70024967e-01,  1.40210660e-02],
        [ 3.79584253e-01,  5.10108829e-01,  6.47388119e-03],
        [ 4.00062501e-01,  4.81629014e-01, -4.55939909e-03],
        [ 4.19535369e-01,  4.60604906e-01, -1.23433908e-02],
        [ 3.25132787e-01,  5.38784206e-01,  1.45440605e-02],
        [ 3.57234329e-01,  4.66180176e-01,  9.31197032e-03],
        [ 3.81895959e-01,  4.21558470e-01, -3.23532685e-03],
        [ 4.05475885e-01,  3.88876855e-01, -1.30925709e-02],
        [ 2.97432423e-01,  5.19765198e-01,  1.04591604e-02],
        [ 3.24466795e-01,  4.45383489e-01,  1.96378608e-03],
        [ 3.47215176e-01,  4.04478878e-01, -8.65624379e-03],
        [ 3.70153606e-01,  3.76890898e-01, -1.60087589e-02],
        [ 2.63496161e-01,  5.09341300e-01,  4.25644638e-03],
        [ 2.78403342e-01,  4.47283417e-01, -4.46178624e-03],
        [ 2.93077946e-01,  4.10510689e-01, -9.59154684e-03],
        [ 3.11106533e-01,  3.80141377e-01, -1.29437586e-02]],

       [[ 2.48720080e-01,  7.20434844e-01,  4.59414650e-07],
        [ 3.11463982e-01,  7.16403723e-01, -1.67388674e-02],
        [ 3.65549326e-01,  6.80881262e-01, -1.74745638e-02],
        [ 4.01059389e-01,  6.23930395e-01, -1.80985108e-02],
        [ 4.20289963e-01,  5.62158287e-01, -1.83646008e-02],
        [ 3.47420603e-01,  5.71168482e-01,  1.39446119e-02],
        [ 3.79588038e-01,  5.10874093e-01,  6.24996889e-03],
        [ 4.00577009e-01,  4.83532399e-01, -5.00792963e-03],
        [ 4.20737386e-01,  4.63747144e-01, -1.30097074e-02],
        [ 3.24928403e-01,  5.40202856e-01,  1.42370323e-02],
        [ 3.56736332e-01,  4.66973066e-01,  8.82864371e-03],
        [ 3.81765485e-01,  4.22291279e-01, -4.09785938e-03],
        [ 4.05778825e-01,  3.90216827e-01, -1.43794734e-02],
        [ 2.97233552e-01,  5.21459341e-01,  9.89203434e-03],
        [ 3.24566901e-01,  4.47197199e-01,  1.29441672e-03],
        [ 3.47774893e-01,  4.06144440e-01, -9.72046331e-03],
        [ 3.71134996e-01,  3.78585160e-01, -1.74973402e-02],
        [ 2.63448596e-01,  5.11607170e-01,  3.39903124e-03],
        [ 2.78622299e-01,  4.48439837e-01, -5.55874128e-03],
        [ 2.93561459e-01,  4.10654455e-01, -1.10837659e-02],
        [ 3.12127054e-01,  3.79834026e-01, -1.48466304e-02]],

       [[ 2.50158370e-01,  7.23740697e-01,  3.43694268e-07],
        [ 3.13010156e-01,  7.16215611e-01, -1.24541698e-02],
        [ 3.65535140e-01,  6.69784307e-01, -1.02721639e-02],
        [ 3.93175036e-01,  6.03510857e-01, -8.61065835e-03],
        [ 4.07896549e-01,  5.42881727e-01, -6.57885056e-03],
        [ 3.48293930e-01,  5.73787093e-01,  1.65520217e-02],
        [ 3.76692295e-01,  5.19252539e-01,  8.03396478e-03],
        [ 3.96584690e-01,  5.02294004e-01, -3.19572235e-03],
        [ 4.15866137e-01,  4.93453503e-01, -1.04225753e-02],
        [ 3.26910675e-01,  5.42580545e-01,  1.55669637e-02],
        [ 3.58681381e-01,  4.71841395e-01,  1.06350305e-02],
        [ 3.83223087e-01,  4.31405246e-01, -2.30480335e-04],
        [ 4.07880753e-01,  4.00835425e-01, -8.61664210e-03],
        [ 3.01127285e-01,  5.23572803e-01,  9.99835879e-03],
        [ 3.29918534e-01,  4.52252746e-01,  1.40154629e-03],
        [ 3.52368504e-01,  4.14513290e-01, -8.18261411e-03],
        [ 3.75531584e-01,  3.89093935e-01, -1.45319896e-02],
        [ 2.68201262e-01,  5.13663650e-01,  2.65451334e-03],
        [ 2.83413619e-01,  4.50868964e-01, -5.66960732e-03],
        [ 2.98819214e-01,  4.16169465e-01, -9.90795903e-03],
        [ 3.17787498e-01,  3.88769358e-01, -1.26371616e-02]],

       [[ 2.50324279e-01,  7.24894643e-01,  3.65388161e-07],
        [ 3.12598318e-01,  7.19706953e-01, -1.22345965e-02],
        [ 3.64068300e-01,  6.70204461e-01, -9.07070749e-03],
        [ 3.92445385e-01,  6.00530803e-01, -6.63002720e-03],
        [ 4.04979110e-01,  5.38480043e-01, -3.53744603e-03],
        [ 3.50663722e-01,  5.77628732e-01,  2.34070178e-02],
        [ 3.78425211e-01,  5.23946464e-01,  1.69524644e-02],
        [ 3.97736579e-01,  5.08371890e-01,  6.05695276e-03],
        [ 4.16316599e-01,  5.01967192e-01, -1.10945455e-03],
        [ 3.28932166e-01,  5.45102537e-01,  2.31888443e-02],
        [ 3.61335009e-01,  4.77763176e-01,  2.11727954e-02],
        [ 3.85672480e-01,  4.40615952e-01,  1.09260576e-02],
        [ 4.10668671e-01,  4.12262738e-01,  2.88419914e-03],
        [ 3.02849561e-01,  5.24905324e-01,  1.79303028e-02],
        [ 3.31574678e-01,  4.54194605e-01,  1.21254288e-02],
        [ 3.54537934e-01,  4.16037321e-01,  3.24135879e-03],
        [ 3.78462136e-01,  3.90434027e-01, -2.96414900e-03],
        [ 2.69420207e-01,  5.13572991e-01,  1.06708454e-02],
        [ 2.84982204e-01,  4.53548074e-01,  4.85176779e-03],
        [ 2.99789667e-01,  4.18587893e-01,  1.63209182e-03],
        [ 3.18112463e-01,  3.89961064e-01, -6.74328650e-04]]])


after0 = align_points(lm_arrs[0][0], lm_arrs[0][5], lm_arrs[0][17], lm_arrs[0])
after1 = align_points(lm_arrs[1][0], lm_arrs[1][5], lm_arrs[1][17], lm_arrs[1])
after2 = align_points(lm_arrs[2][0], lm_arrs[2][5], lm_arrs[2][17], lm_arrs[2])
after3 = align_points(lm_arrs[3][0], lm_arrs[3][5], lm_arrs[3][17], lm_arrs[3])

# plot_points(after[0], after)
plot_points_2(after0, after1, after2, after3)