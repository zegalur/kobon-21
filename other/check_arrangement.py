# This script counts the non-overlapping triangles formed by a given arrangement 
# of straight lines. (CC0)

import sys
import numpy as np

# Triangles with a side shorter than this value are not counted.
EPS = 0.00001

if len(sys.argv) != 2:
    print("Usage:\ncheck_arrangement.py [file_name]\n\nFile format:")
    print("x1, y1, x2, y2\nx1, y1, x2, y2\n...")
    exit()

input = np.loadtxt(sys.argv[1], comments="#", delimiter=",", unpack=False)

# [x1, y1, x2, y2] -> [A, B, C] from Ax + By + C = 0.
def get_line_eq_coefficients(x1, y1, x2, y2):
    A = y2 - y1
    B = x1 - x2
    C = -(A * x1 + B * y1)
    return [A, B, C]

# For two given lines, this function calculates their intersection point.
def get_intersection_point(l1, l2):
    a = np.array([[l1[0], l1[1]], [l2[0], l2[1]]])  # [[A1, B1], [A2, B2]]
    b = np.array([-l1[2], -l2[2]])                  # [C1, C2]
    return np.linalg.solve(a, b)

# Returns the value of Ax + By + C.
def get_line_eq_value(line, point):
    return line[0] * point[0] + line[1] * point[1] + line[2]

# Calculate the line equation coefficients [A, B, C] for every line.
c = list(map(lambda p: get_line_eq_coefficients(p[0], p[1], p[2], p[3]), input))

# Count the number of non-overlapping triangles.
count = 0
for i in range(len(input)):
    for j in range(i + 1, len(input)):
        v1 = get_intersection_point(c[i], c[j])
        for k in range(j + 1, len(input)):
            v2 = get_intersection_point(c[i], c[k])
            v3 = get_intersection_point(c[j], c[k])

            # Triangles with a very small side are skipped.
            if np.linalg.norm(v1-v2) < EPS: continue
            if np.linalg.norm(v1-v3) < EPS: continue
            if np.linalg.norm(v2-v3) < EPS: continue

            is_non_overlapping = True
            for u in range(len(input)):
                if u in [i,j,k]: continue
                s1 = np.sign(get_line_eq_value(c[u], v1))
                s2 = np.sign(get_line_eq_value(c[u], v2))
                s3 = np.sign(get_line_eq_value(c[u], v3))
                if (s1 != s2) or (s1 != s3) or (s2 != s3):
                    is_non_overlapping = False
                    break
            if is_non_overlapping:
                count = count + 1

k = len(input)
print(str(k) + " lines")
print(str(count) + " non-overlapping triangles")

# Show the upper bound value.
upper_bound = 0
if k % 6 in [3,5]: upper_bound = k * (k - 2) // 3
if k % 6 in [0,2]: upper_bound = (k + 1) * (k - 3) // 3
if k % 6 in [1,4]: upper_bound = (k*k - 2*k - 2) // 3
print(str(upper_bound) + " upper bound")
