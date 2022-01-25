from IEEE123_profile_solver import run, PROFILE_IEEE123
from functions import add_samplings_according_users_decision, create_powers_input_P_and_Q_according_users_decesion, \
    EXAMINE_EVERY_30_MINUTES
from initial_data_vector_normalized import APARTMENTS, COMMERCIAL, COMMERCIAL_WITH_APARTMENTS


samples_according_users_decision = add_samplings_according_users_decision(APARTMENTS, EXAMINE_EVERY_30_MINUTES)

# plt.plot(samples_according_users_decision[:, 1])
# plt.show()

create_powers_input_P_and_Q_according_users_decesion(EXAMINE_EVERY_30_MINUTES, samples_according_users_decision)
run(PROFILE_IEEE123)
