import numpy as np
from utils import *


def findQRSonset(ecg, qrs_idx, qrs_interval, qd_interval, interval):
    # calculate interval sizes
    probes_200ms = getIntervalSize(qrs_interval, 1/interval)
    probes_15ms = getIntervalSize(qd_interval, 1/interval)

    # calculate speed
    speed = []
    # searching 200ms before R-peak
    for speed_idx in range(qrs_idx, qrs_idx - probes_200ms, -1):
        # compute and save speed
        speed.append(np.abs((ecg[speed_idx] - ecg[speed_idx - 1]) / interval))
    speed_down = np.array(speed, dtype=np.float32)

    # find QD point
    velocity_threshold = 100.
    velocity_threshold_inc = 750.
    acc_pts = 5
    qd_temp = None
    while qd_temp is None:
        speed_down[speed_down < velocity_threshold] = 0.
        qd_temp = getInx(speed_down, probes_15ms)
        velocity_threshold += velocity_threshold_inc
    qd = qrs_idx - qd_temp

    # find Q-SAPR point
    speed = speed[::-1]
    q_sapr = qd
    for i in range(len(speed) - qd_temp, len(speed) - acc_pts):  # -5 added to avoid calculation of speed after R-peak
        sum_right = sum(speed[i + 1:i + acc_pts])
        sum_left = sum(speed[i - acc_pts:i - 1])

        acceleration = (sum_right - sum_left) / 5
        if acceleration > 100:
            q_sapr = qrs_idx - len(speed) + i
            break

    return qd, q_sapr


def findQRSend(ecg, qrs_idx, qrs_interval, qd_interval, interval):
    # calculate inteval size
    probes_200ms = getIntervalSize(qrs_interval, 1/interval)
    probes_15ms = getIntervalSize(qd_interval, 1/interval)

    # calculate speed
    speed = []
    # searching 200ms after R-peak
    for speed_idx in range(qrs_idx, qrs_idx + probes_200ms):
        # compute and save speed
        speed.append(np.abs((ecg[speed_idx + 1] - ecg[speed_idx]) / interval))
    speed_arr = np.array(speed, dtype=np.float32)

    # find QD point
    velocity_threshold = 100.
    velocity_threshold_inc = 750.
    acc_pts = 5
    qd_temp = None
    while qd_temp is None:
        speed_arr[speed_arr < velocity_threshold] = 0.
        qd_temp = getInx(speed_arr, probes_15ms)
        velocity_threshold += velocity_threshold_inc
    qd = qrs_idx + qd_temp

    # find Q-SAPR point
    #speed = speed[::-1]
    q_sapr = qd
    for i in range(qd_temp, acc_pts, -1):
        sum_right = sum(speed[i + 1:i + acc_pts])
        sum_left = sum(speed[i - acc_pts:i - 1])

        acceleration = (sum_right - sum_left) / 5
        if acceleration > 100:
            q_sapr = qrs_idx + i
            break

    return qd, q_sapr
