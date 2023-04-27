import numpy as np
import math
import json

def K(theta_i_set, theta_a_i_t, delta_i, T_ON, T_OFF):
    K = ((theta_i_set + delta_i / 2 - theta_a_i_t) / (theta_i_set - delta_i / 2 - theta_a_i_t))**(T_ON / T_OFF)
    return K

def R(theta_a_i_t, theta_i_set, K_i, delta_i, P_rated_i):
    R = ((theta_a_i_t - theta_i_set) * (K_i - 1) - delta_i / 2 * (K_i + 1)) / (P_rated_i * (K_i - 1))
    return R

def C(R_i, theta_i_set, theta_a_i_t, delta_i, T_OFF):
    C = -T_OFF/3600 / R_i / math.log((theta_i_set + delta_i / 2 - theta_a_i_t) / (theta_i_set - delta_i / 2 - theta_a_i_t))
    return C

def T(R_i, theta_i_set, theta_a_i_t, delta_i, C_i, P_rated_i):
    T = -R_i* 3600 * C_i * math.log((theta_i_set - delta_i / 2 - theta_a_i_t + R_i * P_rated_i) / (theta_i_set + delta_i / 2 - theta_a_i_t + R_i * P_rated_i))
    return T

with open('config.json') as file:
    configuration = json.load(file)

theta_i_set = configuration["theta_i_set"]
theta_a_i_t = configuration["theta_a_i_t"]
delta_i = configuration["delta_i"]
T_ON = configuration["T_ON"]
T_OFF = configuration["T_OFF"]
P_rated_i = configuration["P_rated_i"]


K_i = K(theta_i_set, theta_a_i_t, delta_i, T_ON, T_OFF)
print(K_i)

R_i = R(theta_a_i_t, theta_i_set, K_i, delta_i, P_rated_i)
print(R_i)

C_i = C(R_i, theta_i_set, theta_a_i_t, delta_i, T_OFF)
print(C_i)

TON = T(R_i, theta_i_set, theta_a_i_t, delta_i, C_i, P_rated_i)
print(TON)