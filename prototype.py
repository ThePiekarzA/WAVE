from scipy import io
from matplotlib import pyplot as plt
import numpy as np
from utils import *

Name = "./test_data/sel100m"
matName = Name + ".mat"
ecg = io.loadmat(matName)
ecg = ecg['val'][0, :]
infoName = Name + ".info"

frequency = 250
interval = 1/frequency

probes_200ms = np.uint16(0.200 * frequency)  # number of probes within 200ms
probes_15ms = np.uint16(0.015 * frequency) + 1  # number of probes within 15ms
r_idx = np.array((13, 1), dtype=np.uint16)
r_idx = [143, 347, 537, 720, 910, 1098, 1296, 1501, 1697, 1890, 2078, 2271, 2459]

print(type(r_idx[0]))
print(r_idx)

print("ecg type={}".format(type(ecg[0])))
print("ecg ={}".format(ecg))

# fig = plt.figure()
# plt.plot(ecg)
# plt.plot(r_idx, ecg[r_idx], 'rx')
# plt.show()

for qrs_idx in r_idx:  # main loop over qrs values
    speed = []
    for speed_idx in range(qrs_idx - probes_200ms, qrs_idx):  # searching 200ms before R-peak
        speed.append(np.abs((ecg[speed_idx+1] - ecg[speed_idx]) / interval))  # compute and save speed
    speed_down = np.array(speed)

    speed_down[speed_down < 1000] = 0.
    zer = np.array([0])

    print("speed_down={}".format(str(speed_down)))
    print("zer={}".format(str(zer)))

    print(str(speed_down)[0:3])
    print(str(zer)[0:3])

    # sp_list = speed_down.tolist()
    # zr_list = zer.tolist()
    # print(type(zr_list))
    # sp_list.index(zr_list)

    # TODO: how to get this index of first occurance :/



# 
# for i in range(len(Rs)):
#     Ridx = int(Rs[i]/interval)
#     plt.plot(Rs[i], data[Ridx], 'r*');
# 
# 
# for i in range(12):
#     Ridx = int(Rs[i]/interval)
# 
#     # step 1 of algo
#     # 200ms span calculated as number of indexes
# 
#     V = []
#     V_th = 50
#     V_th_inc = 50
#     probes = 6
#     window = 0.2
#     speed = np.zeros((1, 50))
#     speed_idx = 0
# 
#     for j in range((Ridx - int(window / interval)) + 1, Ridx, -1):
#         speed[speed_idx] = abs((data[j-1] - data[j]) / interval)
#         speed_idx += 1
# 
#     # speed = flip(speed);
# 
#     temp = speed
#     print(type(speed[0][0]))
#     found_idx = []
# 
#     # looking for len(probes) values in speed vector so that
#     # all values in order are less than V_th
# 
#     while len(found_idx) == 0:
#         # first value is added
#         V_th = V_th + V_th_inc
#         for j in range(len(speed)):
#             if temp[j] < V_th:
#                 temp[j] = 0
# 
#         compare_vec = np.zeros(1,probes)
#         tempStr = ''.join(map(str,temp))
#         compare_vecStr = ''.join(map(str,compare_vec))
# 
#         found_idx = list(find_all(temp, compare_vec))
# 
# 
#     # step 2 of algo
#     QD_idx = Ridx - (found_idx[0] + probes);
# 
#     plt.plot(QD_idx * interval, data(QD_idx), 'go', 'MarkerSize', 4, 'LineWidth', 2)
#

