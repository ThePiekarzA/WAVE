from scipy import io
from matplotlib import pyplot as plt
import numpy as np
from WAVE_functions import *

# load dataset
Name = "./test_data/sel114m"
matName = Name + ".mat"
ecg = io.loadmat(matName)
ecg = ecg['val'][0, :]

# mark R points
r_idx100 = [143, 347, 537, 720, 910, 1098, 1296, 1501, 1697, 1890, 2078, 2271]
r_idx102 = [148, 351, 555, 763, 979, 1197, 1404, 1601, 1800, 2004, 2213, 2422]
r_idx103 = [184, 400, 608, 819, 1029, 1246, 1477, 1697, 1905, 2113, 2324]
r_idx104 = [211, 416, 622, 817, 1019, 1228, 1428, 1633, 1838, 2043, 2242, 2434]
r_idx114 = [218, 507, 797, 1081, 1367, 1640, 1907, 2201]

r_idx = r_idx114

# constant definitions
frequency = 250
interval = 1/frequency

# # interval sizes
# probes_200ms = np.uint16(0.200 * frequency)  # number of probes within 200ms
# probes_15ms = np.uint16(0.015 * frequency) + 1  # number of probes within 15ms

# plot ecg
fig = plt.figure()
plt.plot(ecg)
plt.plot(r_idx, ecg[r_idx], 'rx')

# main loop over qrs values
for qrs_idx in r_idx:
    # find QRS-onset
    qrs_onset_tmp, qrs_onset = findQRSonset(ecg, qrs_idx, 0.200, 0.015, interval)

    qrs_end_tmp, qrs_end = findQRSend(ecg, qrs_idx, 0.200, 0.015, interval)

    # plot calculated points
    plt.plot(qrs_onset_tmp, ecg[qrs_onset_tmp], 'r*')
    plt.plot(qrs_onset, ecg[qrs_onset], 'ro')

    plt.plot(qrs_end_tmp, ecg[qrs_end_tmp], 'g*')
    plt.plot(qrs_end, ecg[qrs_end], 'go')
plt.show()
