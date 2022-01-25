import numpy as np
import random
import matplotlib.pyplot as plt
import math

def normalize(arr, val_min, val_max):
    norm_arr = []
    diff = val_max - val_min
    diff_arr = arr.max() - arr.min()
    for i in arr:
        temp = (((i - arr.min())*diff)/diff_arr) + val_min
        norm_arr.append(temp)
    return norm_arr


number_of_sampling = 24

samples = [0.544181156, 0.503066103, 0.473728166, 0.457491218, 0.454773477, 0.466620167, 0.489477253, 0.50822294,
             0.535958075, 0.570522563, 0.590940696, 0.598675916, 0.605505127, 0.595052237, 0.595679386, 0.599790856,
             0.628153282, 0.741045197, 0.770034773, 0.74724733, 0.718397114, 0.678536571, 0.618536543, 0.546202034]

mu_arr = np.arange(50, 58, 0.25) #flexible
loadprofile = np.zeros((5, number_of_sampling))
loadprofile_scale = np.zeros((5, number_of_sampling))

for e in range(5):
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


    for h in range(number_of_sampling):
        loadprofile[e, h] = samples[h] * (1 + curr_mu * abs(samples[h])) / np.log(1 + curr_mu)

    #Normalize 24 hours after this array is comleted
    loadprofile_scale = normalize(loadprofile, min(samples), max(samples))

loadprofile_scale = [list(row) for row in loadprofile_scale]
print (loadprofile_scale)
t = [i for i in range(number_of_sampling)]

# Plotting both the curves simultaneously
plt.plot(t, samples, color='c', label='original')
plt.plot(t, loadprofile_scale[0], color='r', label='m1')
plt.plot(t, loadprofile_scale [ 1] , color='g', label='m2')
plt.plot(t, loadprofile_scale[2 ], color='b', label='m3')
plt.plot(t, loadprofile_scale[3 ], color='k', label='m4')
plt.plot(t, loadprofile_scale[4 ], color='y', label='m5')
# Naming the x-axis, y-axis and the whole graph
plt.xlabel("hour")
plt.ylabel("power")
plt.title("power in 24-hours diffrent mu")

# Adding legend, which helps us recognize the curve according to it's color
plt.legend()

# To load the display window
plt.show()


