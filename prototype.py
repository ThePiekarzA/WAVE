from scipy import io
from matplotlib import pyplot as plt
import numpy as np
from utils import *

Name = "./test_data/sel100m"
matName = Name + ".mat"
ecg = io.loadmat(matName)
ecg = ecg['val'][0, :]
infoName = Name + ".info"

acc_pts = 5
frequency = 250
interval = 1/frequency

probes_200ms = np.uint16(0.200 * frequency)  # number of probes within 200ms
probes_15ms = np.uint16(0.015 * frequency) + 1  # number of probes within 15ms
velocity_threshold_inc = 750.
r_idx = np.array((13, 1), dtype=np.uint16)
r_idx = [143, 347, 537, 720, 910, 1098, 1296, 1501, 1697, 1890, 2078, 2271, 2459]

fig = plt.figure()
plt.plot(ecg)
plt.plot(r_idx, ecg[r_idx], 'rx')

for qrs_idx in r_idx:  # main loop over qrs values
    speed = []
    for speed_idx in range(qrs_idx, qrs_idx - probes_200ms, -1):  # searching 200ms before R-peak
        speed.append(np.abs((ecg[speed_idx] - ecg[speed_idx-1]) / interval))  # compute and save speed
    speed_down = np.array(speed, dtype=np.float32)
    velocity_threshold = 100.

    qd_temp = None
    while qd_temp is None:
        speed_down[speed_down < velocity_threshold] = 0.
        qd_temp = getInx(speed_down, probes_15ms)
        velocity_threshold += velocity_threshold_inc
    qd = qrs_idx - qd_temp

    speed = speed[::-1]
    for i in range(len(speed) - qd_temp, len(speed) - acc_pts):  # -5 added to avoid calculation of speed after R-peak
        sum_right = sum(speed[i + 1:i + acc_pts])
        sum_left = sum(speed[i - acc_pts:i - 1])

        acceleration = (sum_right - sum_left)/5
        if acceleration > 100:
            q_sapr = qrs_idx - len(speed) + i
            break

    plt.plot(qd, ecg[qd], 'r*')
    plt.plot(q_sapr, ecg[q_sapr], 'go')
plt.show()
