##########################
#  actors.py
#
#  This file defines classes that make up the main actors in a simulation of a
#  bus picking up passengers from bus stops.
##########################

import random, time

from busstop.objects import BusStop, Bus, BusPassenger, BusNetwork


class LinearBusRouteModel(BusNetwork):
    """Linear bus route with stops and buses

    Parameters
    ==========

    start: int, coordinate of start of the route
    end: int, coordinate of end of the route
    stops: list[BusStop], list of bus stops
    buses: list[Bus], list of the buses on the route
    rates: dict[str,float] (optional) rates of passengers arriving

    A LinearBusRoute instances holds a complete model of the state of all
    buses, bus stops and passengers along its route.

    Examples
    ========

    First create passengers, buses and bus stops:

        >>> dave = BusPassenger('Dave', 'West St', 'East St')
        >>> joan = BusPassenger('Joan', 'West St', 'East St')
        >>> bus = Bus('Number 47', (20, 0), 1, [dave])
        >>> busstops = [BusStop('West St', (0, 100), [joan]),
        ...             BusStop('East St', (100, 100), [])]

    Finally we are ready to create a complete linear bus route model with two
    stops and one bus:

        >>> model = LinearBusRouteModel(0, 100, busstops, [bus])

    This model has a route going from coordinate 0 to 100 with a bus stop at
    each end. There are two passengers Dave and Joan both wanting to go from
    East St to West St. Joan is waiting at the West St bus stop. Dave is on
    the bus which is already heading to East St and is currently at
    coordinate 20.
    """

    def init(self):

        """Initialise the model and return initial events.

        Computes and returns the initial events of the simulation e.g.

            >>> sally = BusPassenger('Sally', 'West St', 'East St')
            >>> bus = Bus('56', (0, 0), 1, [sally])
            >>> model = LinearBusRouteModel(0, 100, [], [bus])
            >>> events = model.init()
            >>> events
            [('boards', 'Sally', '56')]

        This shows that at the start of the simulation Sally boards the number
        56 bus.
        """

        # Sorts all bus stops into stops on x axes and stops on y axes.
        global avg_wait_time
        self.start_time = time.time()
        self.revenue_list = []
        self.plot_times = []
        avg_wait_time = [0] * 9
        self.passenger_count = 0
        self.passenger_num = 0
        self.board_passengers = 0
        self.leave_passengers = 0
        self.busstop = ['Centre St', 'South St', 'North St', 'West St', 'Queens St', 'East St', 'Abbey St', 'Harr St', 'Steph St', 'Kenn St']
        self.busstop_coordinates = {'West St': (0, 0), 'Queens St': (25, 0), 'Centre St': (75, 0), 'South St': (75, -30), 'North St': (75, 30),
                                      'Abbey St': (50, 0), 'East St': (100, 0), 'Harr St': (55, 30), 'Kenn St': (5, -20), 'Steph St': (100, 30)}
        self.busstop_y = ['South St', 'North St', 'Centre St']
        self.busstop_x = ['West St', 'Queens St', 'Abbey St', 'East St', 'Centre St']
        self.busstop_s = ['Queens St', 'North St', 'Harr St', 'Kenn St', 'Steph St']
        self.income = 0
        self.fixed_cost = 0
        self.oil_cost = 0

        events = []
        for stop in self.stops:
            for passenger in stop.passengers:
                events.append(('--WAITS--', '   PAX NAME: ', passenger.name, '   DEP: ', stop.name, '   DES: ',
                               passenger.destination, '   DIR: ', passenger.map_direction))

        for bus in self.buses:
            self.fixed_cost += 25
            for passenger in bus.passengers:
                events.append(('--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ', stop.name, '   DES: ',
                               passenger.destination, '   DIR: ', passenger.map_direction))

        return events

    def update(self):

        """Update the state of the model by one time step.

        Returns any events that take place during that step:

            >>> dave = BusPassenger('Dave', 'West St', 'North St', 1, 1, 'North East', time.time(), True, False, False)
            >>> stop = BusStop('East St', (0, 0), [dave])
            >>> bus = Bus('56', (-1, 0), 1, [])
            >>> model = LinearBusRouteModel(-40, 40, 0, 100, stops, horizontal_stops, vertical_stops, buses, rates)
            >>> model.init()
            [(--WAITS--   PAX NAME: Dave   DEP: West St   DES: North St   DIR: North East)]
            >>> model.update()
            [(--BUS STOP--    BUS NO.  Rapid1    STOP NAME:  West St), (--BOARDS--   PAX NAME: Dave   DEP: West St   DES: North St   DIR: North East)]
            >>> model.update()
            []

        This shows that at the start of the simulation Sally boards the number
        56 bus. In the first time step Sally gets on the bus. In the second
        timestep there are no events.
        """

        events = []

        for bus in self.buses:
            if bus.move == 'h':
                events += self.update_bus_hori(bus)
            elif bus.move == 'v':
                events += self.update_bus_vert(bus)
            elif bus.move == 's':
                events += self.update_bus_s(bus)

        for stop in self.stops:
            events += self.update_stop(stop)

        for stop in self.stops:
            events += self.leave_stop(stop)

        return events

    def update_bus_vert(self, bus):

        """Update simulation state of bus."""

        events = []

        # If the bus is not stopped then continue forming new y coordinate

        if not bus.stopped:
            old_x, old_y = bus.position
            new_y = old_y + bus.speed * bus.direction
            new_x = old_x  # Buses move vertically
            bus.position = (old_x, new_y)

            # Does the bus turn around?

            if not (self.vert_start <= new_y <= self.vert_end):
                bus.direction = - bus.direction
                bus.busdir['v'] = - bus.busdir['v']
                events.append(('--BUS TURNS--', '   BUS NO. ', bus.name))
                self.oil_cost += 2.5

        # stops the bus from moving

        else:
            old_x, old_y = bus.position
            new_y = old_y
            old_y = old_y - bus.speed * bus.direction
            bus.position = (old_x, new_y)

        if bus.direction == 1:

            # The bus is travelling bottom to top

            for stop in self.vert_stops:
                stop_x, stop_y = stop.position
                if old_y < stop_y <= new_y:
                    events += self.stop_at(bus, stop)
        else:

            # The bus is travelling top to bottom

            for stop in self.vert_stops:
                stop_x, stop_y = stop.position
                if old_y > stop_y >= new_y:
                    events += self.stop_at(bus, stop)

        return events

    def update_bus_hori(self, bus):

        """Update simulation state of bus."""

        events = []

        # If the bus is not stopped then continue forming new x coordinate

        if not bus.stopped:
            old_x, old_y = bus.position
            new_x = old_x + bus.speed * bus.direction
            new_y = old_y  # Buses move horizontally
            bus.position = (new_x, old_y)

            # Does the bus turn around?

            if not (self.hori_start <= new_x <= self.hori_end):
                bus.direction = - bus.direction
                bus.busdir['h'] = - bus.busdir['h']
                events.append(('--BUS TURNS--', '   BUS NO. ', bus.name))
                self.oil_cost += 2.5


        # stops the bus from moving

        else:
            old_x, old_y = bus.position
            new_x = old_x
            old_x = old_x - bus.speed * bus.direction
            bus.position = (new_x, old_y)

        if bus.direction == 1:

            # The bus is travelling left to right

            for stop in self.hori_stops:
                stop_x, stop_y = stop.position
                if old_x < stop_x <= new_x:
                    events += self.stop_at(bus, stop)
        else:

            # The bus is travelling right to left

            for stop in self.hori_stops:
                stop_x, stop_y = stop.position
                if old_x > stop_x >= new_x:
                    events += self.stop_at(bus, stop)

        return events

    def update_bus_s(self, bus):

        """Update simulation state of bus."""

        events = []

        # If the bus is not stopped then continue forming new y coordinate

        if not bus.stopped:
            old_x, old_y = bus.position
            if old_y >= 30:
                old_y = 30
            elif old_y <= -20:
                old_y = -20
            if old_y >= 30 and old_x > 55:
                new_x = old_x + bus.speed * bus.direction
                new_y = 30  # Buses move horizontally
                bus.position = (new_x, new_y)
            elif old_y <= -20 and old_x < 5:
                new_x = old_x + bus.speed * bus.direction
                new_y = -20  # Buses move horizontally
                bus.position = (new_x, new_y)
            else:
                new_x = old_x + bus.speed * bus.direction
                new_y = old_y + bus.speed * bus.direction
                if new_y >= 30:
                    new_y = 30
                elif new_y <= -20:
                    new_y = -20
                bus.position = (new_x, new_y)

            # Does the bus turn around?

            if not (self.s_start <= new_x <= self.s_end):
                bus.direction = - bus.direction
                bus.busdir['s'] = - bus.busdir['s']
                events.append(('--BUS TURNS--', '   BUS NO. ', bus.name))
                self.oil_cost += 2.5


        # stops the bus from moving

        else:
            old_x, old_y = bus.position
            new_x = old_x
            old_x = old_x - bus.speed * bus.direction
            bus.position = (new_x, old_y)

        if bus.direction == 1:

            # The bus is travelling bottom to top

            for stop in self.s_stops:
                stop_x, stop_y = stop.position
                if old_x < stop_x <= new_x:
                    events += self.stop_at(bus, stop)
        else:

            # The bus is travelling top to bottom

            for stop in self.s_stops:
                stop_x, stop_y = stop.position
                if old_x > stop_x >= new_x:
                    events += self.stop_at(bus, stop)

        return events

    def stop_at(self, bus, stop):

        """Handle bus stopping at stop."""

        events = []

        """The buses board and alight passengers according to their H/V/S (horizontal/vertical/inclined)directions,
         HVS direction indicated the direction of passengers direction on each line. If direction is 0 then it means
         that this passenger will not take bus on that line. After a passenger alights, the previous direction will be
         set to zero so it won't take the bus on the same line again."""

        if bus.move == 'v':
            dir = 'leaving_passengers[0].vertical_direction'
        elif bus.move == 'h':
            dir = 'leaving_passengers[0].horizontal_direction'
        elif bus.move == 's':
            dir = 'leaving_passengers[0].inclined_direction'

        # Check whether this bus is a Local or not
        # If not local, get all stations from bus.stations and append them into a list

        stations = []
        if len(bus.stations) != 0:
            for item in bus.stations:
                stations.append(item.name)

        # Outputs bus stops message

        if not bus.stopped:
            print('--BUS STOP--', '   BUS NO. ', bus.name, '   STOP NAME: ', stop.name)

        # Put all passengers who intends to leave on bus into a list
        # On a transfer station, if the passenger's direction on the two lines where the transfer station shares aren't
        # zero, the passenger will get off.

        if len(bus.passengers) != 0:
            leaving_passengers = []
            for passenger in bus.passengers:
                if passenger.destination == stop.name:
                    leaving_passengers.append(passenger)
                    passenger.changed_and_alight = True
                elif stop.name == 'Centre St' and passenger.horizontal_direction != 0 and passenger.vertical_direction != 0:
                    leaving_passengers.append(passenger)
                elif stop.name == 'Queens St' and passenger.horizontal_direction != 0 and passenger.inclined_direction != 0:
                    leaving_passengers.append(passenger)
                elif stop.name == 'North St' and passenger.vertical_direction != 0 and passenger.inclined_direction != 0:
                    leaving_passengers.append(passenger)

            # Alight passengers one by one if there are passengers getting off at this stop

            if len(leaving_passengers) != 0:
                bus.stopped = True
                bus.passengers.remove(leaving_passengers[0])

                # If this passenger is changing bus then he will be removed from bus and added to Centre St station

                if leaving_passengers[0].change and not leaving_passengers[0].changed_and_alight:
                    stop.passengers.append(leaving_passengers[0])

                    # Resets passenger arrive time.

                    leaving_passengers[0].arrive_time = time.time()
                    events.append(
                    ('--CHANGES--', '   PAX NAME: ', leaving_passengers[0].name, '   DEP: ', passenger.source, '   DES: ',
                        leaving_passengers[0].destination, '   H/V/S DIR: ', passenger.horizontal_direction, passenger.vertical_direction, passenger.inclined_direction))

                # Otherwise simply remove the passenger from bus

                else:
                    events.append(
                    ('--ALIGHTS--', '   PAX NAME: ', leaving_passengers[0].name, '   DEP: ', passenger.source, '   DES: ',
                        leaving_passengers[0].destination, '   H/V/S DIR: ', passenger.horizontal_direction, passenger.vertical_direction, passenger.inclined_direction))
                exec("%s = %d" % (dir, 0))
                leaving_passengers.remove(leaving_passengers[0])
                return events

            # Boards the passengers from the stop one by one

            else:

                # Maximum capacity of buses

                max_capacity = bus.capacity

                for passenger in stop.passengers:

                    if bus.move == 'v':
                        direction = passenger.vertical_direction
                        not_same_axes = (passenger.destination not in self.busstop_y) and (stop.name in stations)
                    elif bus.move == 'h':
                        direction = passenger.horizontal_direction
                        not_same_axes = (passenger.destination not in self.busstop_x) and (stop.name in stations)
                    elif bus.move == 's':
                        direction = passenger.inclined_direction
                        not_same_axes = (passenger.destination not in self.busstop_s) and (stop.name in stations)

                    # When this is a rapid bus.

                    if bus.rapid_express_local == 'r':

                        dest_in_stations = (passenger.destination in stations) and (stop.name in stations)

                        # if the passenger's destination is in the station that this bus will stop.
                        # or the passenger's source is on x axes but destination is on y axes
                        # this passenger will get on.

                        if dest_in_stations or not_same_axes:

                            # if current bus movement direction is same as the passenger.

                            if bus.busdir[bus.move] == direction:

                                # Boards the passenger if maximum capacity is not exceeded.

                                if len(bus.passengers) < max_capacity:
                                    current_time = time.time()
                                    wait_time = current_time - passenger.arrive_time
                                    wait_time = round(wait_time)
                                    avg_wait_time[wait_time - 5] += 1
                                    self.passenger_count += 1
                                    self.income += 3.5
                                    plot_time = round(current_time - self.start_time, 1)
                                    self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                                    self.store_time(plot_time)
                                    self.board_passengers += 1
                                    bus.stopped = True
                                    bus.passengers.append(passenger)
                                    bus.passenger_count += 1
                                    events.append(
                                        (
                                            '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ',
                                            passenger.source,
                                            '   DES: ',
                                            passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction, passenger.vertical_direction, passenger.inclined_direction))
                                    stop.passengers.remove(passenger)
                                    return events
                                else:
                                    break

                    # When this is a express bus.

                    elif bus.rapid_express_local == 'e':

                        dest_in_stations = (passenger.destination in stations) and (stop.name in stations)

                        # Checks whether the passenger's destination is in the station that this bus will stop.

                        if dest_in_stations:

                            # if current bus movement direction is same as the passenger.

                            if bus.busdir[bus.move] == direction:

                                # Boards the passenger if maximum capacity is not exceeded.
                                if len(bus.passengers) < max_capacity:
                                    current_time = time.time()
                                    wait_time = current_time - passenger.arrive_time
                                    wait_time = round(wait_time)
                                    avg_wait_time[wait_time - 5] += 1
                                    self.passenger_count += 1
                                    self.income += 5
                                    plot_time = round(current_time - self.start_time, 1)
                                    self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                                    self.store_time(plot_time)
                                    self.board_passengers += 1
                                    bus.stopped = True
                                    bus.passengers.append(passenger)
                                    bus.passenger_count += 1
                                    events.append(
                                        (
                                            '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ',
                                            passenger.source,
                                            '   DES: ',
                                            passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction, passenger.vertical_direction, passenger.inclined_direction))
                                    stop.passengers.remove(passenger)
                                    return events
                                else:
                                    break

                    # When this is a local bus.

                    elif bus.rapid_express_local == 'l':

                        # if current bus movement direction is same as the passenger.

                        if bus.busdir[bus.move] == direction:

                            # Boards the passenger if maximum capacity is not exceeded.

                            if len(bus.passengers) < max_capacity:
                                current_time = time.time()
                                wait_time = current_time - passenger.arrive_time
                                wait_time = round(wait_time)
                                avg_wait_time[wait_time - 5] += 1
                                self.passenger_count += 1
                                self.income += 2
                                plot_time = round(current_time - self.start_time, 1)
                                self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                                self.store_time(plot_time)
                                self.board_passengers += 1
                                bus.stopped = True
                                bus.passengers.append(passenger)
                                bus.passenger_count += 1
                                events.append(
                                    (
                                        '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ', passenger.source,
                                        '   DES: ',
                                        passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction, passenger.vertical_direction, passenger.inclined_direction))
                                stop.passengers.remove(passenger)
                                return events
                            else:
                                break

        elif len(stop.passengers) != 0:

            # Maximum capacity of buses

            max_capacity = bus.capacity

            for passenger in stop.passengers:

                if bus.move == 'v':
                    direction = passenger.vertical_direction
                    not_same_axes = (passenger.destination not in self.busstop_y) and (stop.name in stations)
                elif bus.move == 'h':
                    direction = passenger.horizontal_direction
                    not_same_axes = (passenger.destination not in self.busstop_x) and (stop.name in stations)
                elif bus.move == 's':
                    direction = passenger.inclined_direction
                    not_same_axes = (passenger.destination not in self.busstop_s) and (stop.name in stations)

                # When this is a rapid bus.

                if bus.rapid_express_local == 'r':

                    dest_in_stations = (passenger.destination in stations) and (stop.name in stations)

                    # if the passenger's destination is in the station that this bus will stop.
                    # or the passenger's source is on x axes but destination is on y axes
                    # this passenger will get on.

                    if dest_in_stations or not_same_axes:

                        # if current bus movement direction is same as the passenger.

                        if bus.busdir[bus.move] == direction:

                            # Boards the passenger if maximum capacity is not exceeded.

                            if len(bus.passengers) < max_capacity:
                                current_time = time.time()
                                wait_time = current_time - passenger.arrive_time
                                wait_time = round(wait_time)
                                avg_wait_time[wait_time - 5] += 1
                                self.passenger_count += 1
                                self.income += 3.5
                                plot_time = round(current_time - self.start_time, 1)
                                self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                                self.store_time(plot_time)
                                self.board_passengers += 1
                                bus.stopped = True
                                bus.passengers.append(passenger)
                                bus.passenger_count += 1
                                events.append(
                                    (
                                        '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ',
                                        passenger.source,
                                        '   DES: ',
                                        passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction,
                                        passenger.vertical_direction, passenger.inclined_direction))
                                stop.passengers.remove(passenger)
                                return events
                            else:
                                break

                # When this is a express bus.

                elif bus.rapid_express_local == 'e':

                    dest_in_stations = (passenger.destination in stations) and (stop.name in stations)

                    # Checks whether the passenger's destination is in the station that this bus will stop.

                    if dest_in_stations:

                        # if current bus movement direction is same as the passenger.

                        if bus.busdir[bus.move] == direction:

                            # Boards the passenger if maximum capacity is not exceeded.

                            if len(bus.passengers) < max_capacity:
                                current_time = time.time()
                                wait_time = current_time - passenger.arrive_time
                                wait_time = round(wait_time)
                                avg_wait_time[wait_time - 5] += 1
                                self.passenger_count += 1
                                self.income += 5
                                plot_time = round(current_time - self.start_time, 1)
                                self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                                self.store_time(plot_time)
                                self.board_passengers += 1
                                bus.stopped = True
                                bus.passengers.append(passenger)
                                bus.passenger_count += 1
                                events.append(
                                    (
                                        '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ',
                                        passenger.source,
                                        '   DES: ',
                                        passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction,
                                        passenger.vertical_direction, passenger.inclined_direction))
                                stop.passengers.remove(passenger)
                                return events
                            else:
                                break

                # When this is a local bus.

                elif bus.rapid_express_local == 'l':

                    # if current bus movement direction is same as the passenger.

                    if bus.busdir[bus.move] == direction:

                        # Boards the passenger if maximum capacity is not exceeded.

                        if len(bus.passengers) < max_capacity:
                            current_time = time.time()
                            wait_time = current_time - passenger.arrive_time
                            wait_time = round(wait_time)
                            avg_wait_time[wait_time - 5] += 1
                            self.passenger_count += 1
                            self.income += 2
                            plot_time = round(current_time - self.start_time, 1)
                            self.store_cost(self.income, self.fixed_cost, self.oil_cost)
                            self.store_time(plot_time)
                            self.board_passengers += 1
                            bus.stopped = True
                            bus.passengers.append(passenger)
                            bus.passenger_count += 1
                            events.append(
                                (
                                    '--BOARDS--', '   PAX NAME: ', passenger.name, '   DEP: ', passenger.source,
                                    '   DES: ',
                                    passenger.destination, '   H/V/S DIR: ', passenger.horizontal_direction,
                                    passenger.vertical_direction, passenger.inclined_direction))
                            stop.passengers.remove(passenger)
                            return events
                        else:
                            break

        bus.stopped = False
        return events

    def update_stop(self, stop):

        """Update bus stop"""

        # New passengers arrive randomly at each bus stop. The probability of
        # a passenger arriving at particular stop is given by
        #     1 - self.rates[self.name].

        if stop.name in self.rates:
            rate = self.rates[stop.name]
            if rate > random.random():

                # Randomly selects the destination for the new passenger.

                valid = False
                while not valid:
                    destination = random.choice(self.busstop)
                    if stop.name != destination:
                        valid = True

                # Finds whether the passenger change at transfer stations.

                if stop.name == 'Centre St' and (destination in self.busstop_x or destination in self.busstop_y):
                    change = False
                elif stop.name == 'North St' and (destination in self.busstop_s or destination in self.busstop_y):
                    change = False
                elif stop.name == 'Queens St' and (destination in self.busstop_x or destination in self.busstop_s):
                    change = False
                elif stop.name in self.busstop_y and destination not in self.busstop_y:
                    change = True
                elif stop.name in self.busstop_x and destination not in self.busstop_x:
                    change = True
                elif stop.name in self.busstop_s and destination not in self.busstop_s:
                    change = True
                else:
                    change = False

                # Finds the horizontal, vertical and inclined direction of a passenger.

                if (stop.name == 'East St' and destination == 'Harr St') or\
                        (stop.name == 'South St' and destination == 'Kenn St'):
                    horizontal_direction = -1
                    vertical_direction = 1
                    inclined_direction = -1
                elif (stop.name == 'Harr St' and destination == 'East St') or\
                        (stop.name == 'Kenn St' and destination == 'South St'):
                    horizontal_direction = 1
                    vertical_direction = -1
                    inclined_direction = 1
                elif stop.name == 'East St' and destination == 'Steph St':
                    horizontal_direction = -1
                    vertical_direction = 1
                    inclined_direction = 1
                elif stop.name == 'Steph St' and destination == 'East St':
                    horizontal_direction = 1
                    vertical_direction = -1
                    inclined_direction = -1
                elif stop.name == 'Abbey St' and destination == 'Steph St':
                    horizontal_direction = 1
                    vertical_direction = 1
                    inclined_direction = 1
                elif stop.name == 'Steph St' and destination == 'Abbey St':
                    horizontal_direction = -1
                    vertical_direction = -1
                    inclined_direction = -1
                elif stop.name == 'Harr St' and destination == 'Centre St':
                    horizontal_direction = 0
                    vertical_direction = -1
                    inclined_direction = 1
                elif stop.name == 'Centre St' and destination == 'Harr St':
                    horizontal_direction = 0
                    vertical_direction = 1
                    inclined_direction = -1
                elif stop.name == 'West St' and destination == 'North St':
                    horizontal_direction = 1
                    vertical_direction = 0
                    inclined_direction = 1
                elif stop.name == 'North St' and destination == 'West St':
                    horizontal_direction = -1
                    vertical_direction = 0
                    inclined_direction = -1
                elif stop.name == 'Centre St' and destination == 'East St':
                    horizontal_direction = 1
                    vertical_direction = 0
                    inclined_direction = 0
                elif stop.name == 'East St' and destination == 'Centre St':
                    horizontal_direction = -1
                    vertical_direction = 0
                    inclined_direction = 0
                elif stop.name == 'Centre St' and destination == 'Steph St':
                    horizontal_direction = 0
                    vertical_direction = 1
                    inclined_direction = 1
                elif stop.name == 'Steph St' and destination == 'Centre St':
                    horizontal_direction = 0
                    vertical_direction = -1
                    inclined_direction = -1
                elif (stop.name == 'Kenn St' and destination == 'West St') or\
                        (stop.name == 'Abbey St' and destination == 'Harr St'):
                    horizontal_direction = -1
                    vertical_direction = 0
                    inclined_direction = 1
                elif (stop.name == 'West St' and destination == 'Kenn St') or\
                        (stop.name == 'Harr St' and destination == 'Abbey St'):
                    horizontal_direction = 1
                    vertical_direction = 0
                    inclined_direction = -1

                elif not change:

                    if (stop.name == 'Centre St' and destination in self.busstop_y) or\
                            (stop.name == 'North St' and destination in self.busstop_y):
                        horizontal_direction = 0
                        inclined_direction = 0
                        if self.busstop_coordinates[destination][1] > self.busstop_coordinates[stop.name][1]:
                            vertical_direction = 1
                        elif self.busstop_coordinates[destination][1] < self.busstop_coordinates[stop.name][1]:
                            vertical_direction = -1

                    elif (stop.name == 'Centre St' and destination in self.busstop_x) or\
                            (stop.name == 'Queens St' and destination in self.busstop_x):
                        vertical_direction = 0
                        inclined_direction = 0
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = -1

                    elif (stop.name == 'Queens St' and destination in self.busstop_s) or\
                            (stop.name == 'North St' and destination in self.busstop_s):
                        vertical_direction = 0
                        horizontal_direction = 0
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            inclined_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            inclined_direction = -1

                    elif stop.name in self.busstop_x:
                        inclined_direction = 0
                        vertical_direction = 0
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = -1
                    elif stop.name in self.busstop_s:
                        vertical_direction = 0
                        horizontal_direction = 0
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            inclined_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            inclined_direction = -1
                    elif stop.name in self.busstop_y:
                        inclined_direction = 0
                        horizontal_direction = 0
                        if self.busstop_coordinates[destination][1] > self.busstop_coordinates[stop.name][1]:
                            vertical_direction = 1
                        elif self.busstop_coordinates[destination][1] < self.busstop_coordinates[stop.name][1]:
                            vertical_direction = -1

                elif change:

                    if (stop.name in self.busstop_y and destination in self.busstop_x) or\
                            (stop.name in self.busstop_x and destination in self.busstop_y):
                        inclined_direction = 0
                        if self.busstop_coordinates[destination][1] > self.busstop_coordinates[stop.name][1]:
                            vertical_direction = 1
                        elif self.busstop_coordinates[destination][1] < self.busstop_coordinates[stop.name][1]:
                            vertical_direction = -1
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = -1

                    elif (stop.name in self.busstop_x and destination in self.busstop_s) or\
                            (stop.name in self.busstop_s and destination in self.busstop_x):
                        vertical_direction = 0
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            inclined_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            inclined_direction = -1
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            horizontal_direction = -1

                    elif (stop.name in self.busstop_y and destination in self.busstop_s) or\
                            (stop.name in self.busstop_s and destination in self.busstop_y):
                        horizontal_direction = 0
                        if self.busstop_coordinates[destination][1] > self.busstop_coordinates[stop.name][1]:
                            vertical_direction = 1
                        elif self.busstop_coordinates[destination][1] < self.busstop_coordinates[stop.name][1]:
                            vertical_direction = -1
                        if self.busstop_coordinates[destination][0] > self.busstop_coordinates[stop.name][0]:
                            inclined_direction = 1
                        elif self.busstop_coordinates[destination][0] < self.busstop_coordinates[stop.name][0]:
                            inclined_direction = -1

                name = 'random' + str(self.passenger_num)
                self.passenger_num += 1

                # The time each passenger arrives at the stop is now saved

                arrive_time = time.time()
                passenger = BusPassenger(name, stop.name, destination, horizontal_direction, vertical_direction,
                                         inclined_direction, arrive_time, change, False)
                stop.passengers.append(passenger)
                return [('--WAITS--', '   PAX NAME: ', passenger.name, '   DEP: ', stop.name, '   DES: ',
                         passenger.destination, '   H/V/S DIR: ', horizontal_direction, vertical_direction, inclined_direction)]

        return []

    def leave_stop(self, stop):
        events = []
        current_time = time.time()
        for passenger in stop.passengers:
            wait_time = current_time - passenger.arrive_time
            if wait_time > 12:
                events.append(('--LEFT--', '   PAX NAME: ', passenger.name))
                stop.passengers.remove(passenger)
                avg_wait_time[-1] += 1
                self.leave_passengers += 1
                return events

        return []

    def get_wait(self):
        return avg_wait_time

    def init_conditions(self, stops, buses):
        for stop in stops:
            stop.passengers = []
        for bus in buses:
            bus.passengers = []
            bus.stopped = False
            if bus.move == 's':
                bus.position = (random.randint(60, 90), 30)
            elif bus.move == 'h':
                bus.position = (random.randint(10, 90), 0)
            elif bus.move == 'v':
                bus.position = (75, random.randint(-20, 20))

    def get_tally(self):
        return self.passenger_count

    def store_cost(self, income, fixed_cost, oil_cost):
        self.revenue_list.append(self.income - self.fixed_cost - self.oil_cost)

    def store_time(self, plot_time):
        self.plot_times.append(plot_time)

    def get_revenue(self):
        return self.revenue_list

    def get_time(self):
        return self.plot_times

    def get_passenger(self):
        return [self.board_passengers, self.leave_passengers]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
