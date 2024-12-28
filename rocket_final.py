# Student ID  : 2658466
# Project Name: Rocket
# Project ID  : S-Rocket
'''
Description : This code simulates the trajectory of falcon 9,a two-stage rocket, as it burns fuel, reduces mass, 
and transitions stages to achieve Earth's escape velocity. It accounts for gravitational force, thrust variations, 
and atmospheric pressure, plotting acceleration, velocity, and altitude over time.
'''

# Rocket: Falcon 9
'''
The Drag force is ignored in the calculations as it is negligible compared to thrust, hence does not affect the motion.
Even at max Q, the drag force is approximately 30 kN, while thrust is approx 7.6 mil N.
Moreover, the calculation for drag force is too complicated and seems to be outside the scope of this project,
due to the drag coefficient becoming dynamic from speeds near mach 1 and over, and there being no formula for calculating
drag coef without using drag force (we can't use drag force to calculate drag coef because we need drag coef for
drag force in the first place). The only plausible method was to use plots of drag coef against mach number from
experimental data and fit that onto a function, then use that function to get drag coef as a function of of mach number.
Then use that function of drag coef along with other variables to make a composite function of drag force.
However, this is a very complex task and is outside the scope of this project. 
Because A: I could not find the actual relevant data for this or any rocket. The closest I could find was of a cylinder. 
But that too had a domain of 0.5 < mach < 1.3, while the rocket reaches speeds way beyond that (around mach 33).
B: The curve fitting, which is also not a part of this course, will take a lot of time and effort.
'''
import math
from scipy import constants
import matplotlib.pyplot as plt

# data
dt = 1 # delta t
st1_m_fuel = 411000 # kg. Mass of fuel for stage 1
st2_m_fuel = 116000 # kg. Mass of fuel for stage 2
st1_flow_rate = 2750 # kg/s. Mass flow rate of fuel for stage 1
st2_flow_rate = 287 # kg/s. Mass flow rate of fuel for stage 2
rocket_mass_tot = 549054 # kg. Total mass of rocket
m_discarded_st1 = 26000 # kg. Mass of the part of rocket discarded after stage 1
H = 8500 # m. Scale height (the height over which pressure decreases by a factor of e)
st_sep_time = st1_m_fuel/st1_flow_rate # s. Time of stage separation

# outputs stage number. Stage changes when fuel for 1st stage is depleted.
def stage(t):
    time = st1_m_fuel/st1_flow_rate
    if t < time:
        return 1
    else:
        return 2
    
# calculates mass of rocket considering burning fuel and stage sepreation. Calls stage()
def mass(t):
    if stage(t) == 1:
        return rocket_mass_tot - st1_flow_rate*t
    else:
        t = t - st_sep_time
        return rocket_mass_tot - st2_flow_rate*t - m_discarded_st1 - st1_m_fuel

# calculates thrust. Calls stage()
def thrust(t,h):
    stage_num = stage(t)
    # specific impulses at sea level, stage 1 and stage 2
    I_sea = 282
    I_st1_vac = 311
    I_st2_vac = 348
    # choose value of specific impulse based on altitude
    def Impulse(h,stage):
        if stage == 1:
            if h <= 0:
                return I_sea
            else:
                return I_st1_vac
        else:
            return I_st2_vac
    # calculates the ambient pressure (external atmospheric pressure). Pa(h) = p0*(e**(-h/H))
    def Pa(h):
        P_0 = constants.atm
        if h <= 100000:
            return P_0 * math.exp(-h/H)
        else:
            return 0
    # chooses the mass flow rate of the fuel based on the stage
    def m_flow(stage):
        if stage == 1:
            return st1_flow_rate
        else:
            return st2_flow_rate
    # chooses the nozzle exit pressure based on stage
    def Pe(stage): 
        if stage == 1:
            return 40000
        else:
            return 500
    # calculates nozzle exit area
    def Ae(stage):
        if stage == 1:
            return 0.7
        else:
            return 1.1 
    # calculates the thrust based on the mass flow rate, specific impulse, ambient pressure and nozzle exit pressure
    # thrust = m_flow * I * g0 + (Pe - Pa(h)) Ae
    T = m_flow(stage_num) * Impulse(h,stage_num) * constants.g + (Pe(stage_num) - Pa(h))*Ae(stage_num)
    return T

# calculates gravitational force. Calls mass()
def f_grav(t,h):
    G = constants.gravitational_constant
    Me = 5.972e24 # mass of earth (kg)
    radius_earth = 6378000
    r = radius_earth + h
    f = G * Me * mass(t) / r**2
    return f

# calculates net force
def f_tot(t,h):
    f = thrust(t,h) - f_grav(t,h)
    return f

# simulates the trajectory of the rocket
def motion():
    acc = []
    vel = []
    pos = []
    time = [] 
    v = 0
    h = 0
    t = 0
    # stop calculating when escape velocity reached
    while v <= 11200: # approx escape vel
        a = f_tot(t,h) / mass(t)
        v = v + (a * dt)
        h = h + (v * dt)
        acc.append(a)
        vel.append(v)
        pos.append(h)
        time.append(t)
        # returns acceleration, velocity, position, and time as different arrays
        if v >= 11200:
            print(f"Escape velocity reached at time: {t} s and altitude: {h:.0f} m")
        t = t + dt
    return acc, vel, pos, time

# plots the graphs. calls force()      
def plot():
    acc, vel, pos, time = motion()
    plt.figure(figsize=(15,10))
    plt.subplot(3,1,1)
    plt.plot(time,acc)
    plt.xlabel("time (s)")
    plt.ylabel("acceleration (m/s^2)")
    plt.subplot(3,1,2)
    plt.plot(time,vel)
    plt.xlabel("time (s)")
    plt.ylabel("velocity (m/s)")
    plt.subplot(3,1,3)
    plt.plot(time,pos)
    plt.xlabel("time (s)")
    plt.ylabel("altitude (x10^6)(m)")
    plt.pause(0.01)
    plt.show()
    return


plot()