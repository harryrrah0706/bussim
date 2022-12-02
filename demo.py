#!/usr/bin/env python3

from busstop.objects import BusPassenger, Bus, BusStop
from busstop.linear import LinearBusRouteModel
from busstop.animation import animate_model
from busstop.plotting_function import avg_wait
from busstop.plot_demo import *
import random
import time


dave = BusPassenger('Dave', 'Centre St', 'Steph St', 0, 1, -1, time.time(), True, False)
# joan = BusPassenger('Joan', 'Queens St', 'South St', 1, -1, 'South East', time.time(), True, False)

# Initializing stops

West_St = BusStop('West St', (0, 0), [])
North_St = BusStop('North St', (75, 30), [])
Abbey_St = BusStop('Abbey St', (50, 0), [])
South_St = BusStop('South St', (75, -30), [])
East_St = BusStop('East St', (100, 0), [])
Queens_St = BusStop('Queens St', (25, 0), [])
Centre_St = BusStop('Centre St', (75, 0), [])
Harr_St = BusStop('Harr St', (55, 30), [])
Kenn_St = BusStop('Kenn St', (5, -20), [])
Steph_St = BusStop('Steph St', (100, 30), [])

stops = [West_St, North_St, Centre_St, South_St, East_St, Queens_St, Abbey_St, Harr_St, Steph_St, Kenn_St]
horizontal_stops = [West_St, Centre_St, East_St, Queens_St, Abbey_St]
vertical_stops = [North_St, Centre_St, South_St]
s_stops = [Harr_St, Kenn_St, Steph_St, North_St, Queens_St]

# Initializing buses
# Express buses only stops at West St and East St / North St and South St
# Rapid buses only stops at West St, Centre St, and East St.
# Local buses stops at all station.

Express1 = Bus('E1', (0, 0), 1, 3, [], False, [West_St, East_St], 'h', 'e', 4, 0, {'h': 1, 'v': 0, 's': 0})
Express2 = Bus('E2', (75, 30), -1, 3, [], False, [North_St, South_St], 'v', 'e', 4, 0, {'h': 0, 'v': -1, 's': 0})
Rapid1 = Bus('R1', (30, 0), -1, 2, [], False, [West_St, Centre_St, East_St], 'h', 'r', 6, 0, {'h': -1, 'v': 0, 's': 0})
Local1 = Bus('L1', (40, 0), 1, 1.5, [], False, [], 'h', 'l', 10, 0, {'h': 1, 'v': 0, 's': 0})
Local2 = Bus('L2', (75, 10), -1, 1.5, [], False, [], 'v', 'l', 10, 0, {'h': 0, 'v': -1, 's': 0})
Local3 = Bus('L3', (60, 0), -1, 1.75, [], False, [], 'h', 'l', 10, 0, {'h': -1, 'v': 0, 's': 0})
Local4 = Bus('L4', (65, 30), -1, 1.75, [], False, [], 's', 'l', 10, 0, {'h': 0, 'v': 0, 's': -1})
Local5 = Bus('L5', (35, 10), 1, 1.25, [], False, [], 's', 'l', 10, 0, {'h': 0, 'v': 0, 's': 1})
Local6 = Bus('L6', (15, -10), -1, 1.5, [], False, [], 's', 'l', 10, 0, {'h': 0, 'v': 0, 's': -1})


buses = [Local1, Local2, Local3, Local4, Local5, Local6, Rapid1, Express1, Express2]

rates = {
    'West St': 0.025,
    'North St': 0.025,
    'Centre St': 0.025,
    'South St': 0.025,
    'Queens St': 0.025,
    'Abbey St': 0.025,
    'East St': 0.025,
    'Kenn St': 0.025,
    'Harr St': 0.025,
    'Steph St': 0.025
}

# Simulation of the original model without any changes made to it

model_original = LinearBusRouteModel(-30, 30, 0, 100, 0, 100, stops, horizontal_stops, vertical_stops, s_stops, buses, rates)
start_time = time.time()
animate_model(model_original)
time_passed = time.time() - start_time
avg_wait_time1 = model_original.get_wait()
passenger_count1 = model_original.get_tally()
average_count1 = round(passenger_count1 / (time_passed / 60))
revenue1 = model_original.get_revenue()
plot_time1 = model_original.get_time()
passenger_ratio1 = model_original.get_passenger()


plot_pie(passenger_ratio1)


#############################

#Two buses "Local6" and "Express2" are removed

#############################

buses = [Local1, Local2, Local3, Local4, Local5, Rapid1, Express1]
model_wait2 = LinearBusRouteModel(-30, 30, 0, 100, 0, 100, stops, horizontal_stops, vertical_stops, s_stops, buses, rates)
model_wait2.init_conditions(stops, buses)
animate_model(model_wait2)
avg_wait_time2 = model_wait2.get_wait()
revenue2 = model_wait2.get_revenue()
plot_time2 = model_wait2.get_time()
passenger_ratio2 = model_wait2.get_passenger()


plot_pie(passenger_ratio2)
plot_avg_wait_time(avg_wait_time1, avg_wait_time2)


#############################

#Buses "Local6", "Express1" and "Express2" are removed

#############################

buses = [Local1, Local2, Local3, Local4, Local5, Rapid1]
model_revenue = LinearBusRouteModel(-30, 30, 0, 100, 0, 100, stops, horizontal_stops, vertical_stops, s_stops, buses, rates)
model_revenue.init_conditions(stops, buses)
animate_model(model_revenue)
revenue3 = model_revenue.get_revenue()
plot_time3 = model_revenue.get_time()
passenger_ratio3 = model_revenue.get_passenger()


plot_pie(passenger_ratio3)
plot_revenues(revenue1, revenue2 ,revenue3, plot_time1, plot_time2, plot_time3)


#############################

#Increased rate of passengers arriving to 0.05

#############################

buses = [Local1, Local2, Local3, Local4, Local5, Local6, Rapid1, Express1, Express2]
rates = {
    'West St': 0.05,
    'North St': 0.05,
    'Centre St': 0.05,
    'South St': 0.05,
    'Queens St': 0.05,
    'Abbey St': 0.05,
    'East St': 0.05,
    'Kenn St': 0.05,
    'Harr St': 0.05,
    'Steph St': 0.05

}
model_rates2 = LinearBusRouteModel(-30, 30, 0, 100, 0, 100, stops, horizontal_stops, vertical_stops, s_stops, buses, rates)
model_rates2.init_conditions(stops, buses)
start_time = time.time()
animate_model(model_rates2)
time_passed = time.time() - start_time
passenger_count2 = model_rates2.get_tally()
average_count2 = round(passenger_count2 / (time_passed / 60))


#############################

#Increased rate of passengers arriving to 0.1

#############################

buses = [Local1, Local2, Local3, Local4, Local5, Local6, Rapid1, Express1, Express2]
rates = {
    'West St': 0.1,
    'North St': 0.1,
    'Centre St': 0.1,
    'South St': 0.1,
    'Queens St': 0.1,
    'Abbey St': 0.1,
    'East St': 0.1,
    'Kenn St': 0.1,
    'Harr St': 0.1,
    'Steph St': 0.1
}
model_rates3 = LinearBusRouteModel(-30, 30, 0, 100, 0, 100, stops, horizontal_stops, vertical_stops, s_stops, buses, rates)
model_rates3.init_conditions(stops, buses)
animate_model(model_rates3)
passenger_count3 = model_rates3.get_tally()
average_count3 = round(passenger_count3 / (time_passed / 60))

plot_rates(average_count1, average_count2, average_count3)
