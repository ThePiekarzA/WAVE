from scipy import io
import matplotlib.plot as plt
import numpy as np
from utils import *

Name = "./test_data/sel100m"
matName = Name + ".mat"
data = io.loadmat(matName);
data = data.val[1,:];

infoName = Name + ".info"

interval = 0.004

time = [ i for i in range(1,len(data))] * interval;
# Rs = [0.596 1.408 2.224 3.056 3.92 4.792 5.62 6.408 7.204 8.02 8.856 9.692];
Rs = [.576, 1.392, 2.152, 2.884, 3.644, 4.396, 5.188, 6.008, 6.792, 7.564, 8.316, 9.088, 9.840];

fig = plt.figure()
plt.plot(time, data, 'LineWidth', 1.7)

for i in range(len(Rs)):
    Ridx = int(Rs[i]/interval)
    plt.plot(Rs[i], data[Ridx], 'r*');


for i in range(12):
    Ridx = int(Rs[i]/interval)

    # step 1 of algo
    # 200ms span calculated as number of indexes

    V=[]
    V_th = 50
    V_th_inc = 50
    probes = 6
    window = 0.2
    speed = np.zeros(1, 50)
    speed_idx = 0

    for j in range((Ridx - int(window / interval)) + 1, Ridx)[::-1]:
        speed[speed_idx] = abs((data[i-1] - data[i]) / interval);
        speed_idx += 1

    # speed = flip(speed);

    temp = speed
    found_idx = []

    # looking for len(probes) values in speed vector so that
    # all values in order are less than V_th

    while len(found_idx) == 0:
        # first value is added
        V_th = V_th + V_th_inc
        for j in range(len(speed)):
            if temp[j] < V_th:
                temp[j] = 0

        compare_vec = np.zeros(1,probes)
        tempStr = ''.join(map(str,temp))
        compare_vecStr = ''.join(map(str,compare_vec))

        found_idx = list(find_all(temp, compare_vec))


    # step 2 of algo
    QD_idx = Ridx - (found_idx[0] + probes);

    plt.plot(QD_idx * interval, data(QD_idx), 'go', 'MarkerSize', 4, 'LineWidth', 2)

