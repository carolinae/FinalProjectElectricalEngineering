import random
import numpy as np
import math

from dss_profile_solver import CIRCUIT_PROFILE_IEEE123

EXAMINE_EVERY_HOUR = 72
# EXAMINE_EVERY_HOUR = 8760
EXAMINE_EVERY_30_MINUTES = 17520
EXAMINE_EVERY_15_MINUTES = 26280

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = arr.max() - arr.min()
    for i in arr:
        temp = (((i - arr.min()) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def add_samplings_according_users_decision(samples, number_of_sampling):
    if number_of_sampling == EXAMINE_EVERY_HOUR:
        return samples

    t = [i for i in range(EXAMINE_EVERY_HOUR)]
    d = np.array([t, samples])

    new_x = np.linspace(min(d[0, :]), max(d[0, :]), num=number_of_sampling)
    new_y = np.interp(new_x, d[0, :], d[1, :])

    # plt.scatter(d[0, :], d[1, :], label='original', zorder=10)
    # plt.scatter(new_x, new_y, label='interpolated', s=0.5)
    #
    # plt.legend()
    #
    # plt.show()

    return new_y


def find_index_of_min_value(x_array, curr_mu):
    min_val = 1000
    Q_index = 0
    for i in range(len(x_array)):
        if math.isnan(x_array[i]):
            continue
        if ((abs(x_array[i] - curr_mu))) < min_val:
            min_val = ((abs(x_array[i] - curr_mu)))
            Q_index = i
    return Q_index


def create_powers_input_P_and_Q_according_users_decesion(number_of_sampling, samples, selected_circuit_type):
    mu_arr = np.arange(50, 95, 0.015)  # flexible

    if selected_circuit_type == CIRCUIT_PROFILE_IEEE123:
        number_of_loads = 90
        loadDataArr = np.zeros((91, number_of_sampling))
        loadDataArrQ = np.zeros((91, number_of_sampling))
    else:
        number_of_loads = 1379
        loadDataArr = np.zeros((1379, number_of_sampling))
        loadDataArrQ = np.zeros((1379, number_of_sampling))

    for e in range(number_of_loads):
        random_index_coise = []
        for item in range(0, len(mu_arr)):
            random_index_coise.append(item)

        index = random.choice(random_index_coise)
        while True:
            if math.isnan(mu_arr[index]):
                index = random.choice(random_index_coise)
            else:
                break

        curr_mu = mu_arr[index]
        mu_arr[index] = np.NaN
        index_of_min_val_for_Q = find_index_of_min_value(mu_arr, curr_mu)
        curr_muQ = mu_arr[index_of_min_val_for_Q]
        mu_arr[index_of_min_val_for_Q] = np.NaN

        # TODO add rescale function
        for h in range(number_of_sampling):
            loadDataArr[e, h] = samples[h] * (1 + curr_mu * abs(samples[h])) / np.log(1 + curr_mu)
            loadDataArrQ[e, h] = samples[h] * np.log(1 + curr_muQ * abs(samples[h])) / np.log(1 + curr_muQ)

        loadDataArr[e, :] = normalize(loadDataArr[e, :], min(samples), max(samples))
        loadDataArrQ[e, :] = normalize(loadDataArrQ[e, :], min(samples), max(samples))
        #print(min(loadDataArr[e, :]), max(loadDataArr[e, :]))
        # plt.plot(loadDataArr[1,:])
        # plt.show()
        # plt.plot(loadDataArr)
        # plt.show()
        ############################################ write data to csv files ###############################################
        if selected_circuit_type == CIRCUIT_PROFILE_IEEE123:
            np.savetxt(f"C:\\ieee123\\LS{e + 1}.csv", np.transpose(loadDataArr[e, :]), delimiter=",",
                       fmt="%s")
            np.savetxt(f"C:\\ieee123\\LS_Q{e + 1}.csv", np.transpose(loadDataArrQ[e, :]),
                       delimiter=",",
                       fmt="%s")
        else:
            np.savetxt(f"C:\\ck5\\LS{e + 1}.csv", np.transpose(loadDataArr[e, :]), delimiter=",", fmt="%s")
            np.savetxt(f"C:\\ck5\\LS_Q{e + 1}.csv", np.transpose(loadDataArrQ[e, :]), delimiter=",", fmt="%s")

    # plt.plot(loadDataArr[:, 1])
    # plt.show()
    # print(4)




