##########################
#  actors.py
#
#  This file defines classes that make up the main actors in a simulation of a
#  bus picking up passengers from bus stops.
##########################

import time


class Printable:

    """Mixin to add printing functionality to subclasses.

    Examples
    ========

    A subclass just needs to define parameters and will print nicely::

        >>> class Thing(Printable):
        ...     parameters = 'foo', 'bar'
        ...     def __init__(self, foo, bar):
        ...         self.foo = foo
        ...         self.bar = bar
        >>> t = Thing(3, 'qwe')
        >>> t
        Thing(3, 'qwe')
    """

    def __repr__(self):
        classname = type(self).__name__
        args = [getattr(self, p) for p in self.parameters]
        return '%s(%s)' % (classname, ', '.join(map(repr, args)))


class BusPassenger(Printable):

    """Bus passenger going from A to B

    Parameters
    ==========

    name: str, the name of the passenger
    source: str, the name of the starting bus stop
    destination: str, the name of the ending bus stop
    direction: direction that the passenger wants to travel in
    map_direction: compass direction

    Examples
    ========

    Create a passenger:

        >>> dave = BusPassenger('Dave', 'West St', 'North St', 1, 1, 'North East', time.time(), True, False, False)
        >>> dave
        BusPassenger('Dave', 'West St', 'North St', 1, 1, 'North East', time.time(), True, False, False)

    All attributes are public:

        >>> dave.name
        'Dave'
    """

    parameters = 'name', 'source', 'destination', "1", "East", "arrive_time"

    def __init__(self, name, source, destination, horizontal_direction, vertical_direction, inclined_direction,
                 arrive_time, change, changed_and_alight):

        if not all(isinstance(p, str) for p in (name, source, destination)):
            raise TypeError('name, source, destination and map_direction should be strings')
        if not isinstance(arrive_time, float):
            raise TypeError("arrive_time should be a float number")
        if not isinstance(change, bool):
            raise TypeError("change should be a boolean")
        if not isinstance(changed_and_alight, bool):
            raise TypeError("changed should be a boolean")
        if not isinstance(vertical_direction, int):
            raise TypeError("vertical_direction should be a integer")
        if not isinstance(horizontal_direction, int):
            raise TypeError("horizontal_direction should be a integer")

        self.name = name
        self.source = source
        self.destination = destination
        self.horizontal_direction = horizontal_direction
        self.vertical_direction = vertical_direction
        self.arrive_time = arrive_time
        self.change = change
        self.inclined_direction = inclined_direction
        self.changed_and_alight = changed_and_alight


class BusStop(Printable):

    """Bus stop along a bus route with a position and passengers

    Parameters
    ==========

    name: str, name of the bus stop
    position: tuple(int,int), coordinates of the bus stop
    passengers: list[Passenger], list of the passengers at the stop

    Examples
    ========

    Create a pasenger and add to the bus stop:

        >>> dave = BusPassenger('Dave', 'West St', 'East St', 1, "East", "arrive_time")
        >>> busstop = BusStop('West St', (20, 0), [dave])
        >>> busstop
        BusStop('West St', (20, 0), [BusPassenger('Dave', 'West St', 'East St', 1, "East", "arrive_time")])

    """

    parameters = 'name', 'position', 'passengers'

    def __init__(self, name, position, passengers):

        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(c, int) for c in position)):
            raise TypeError('position should be a pair of ints')
        if not all(isinstance(p, BusPassenger) for p in passengers):
            raise TypeError('passengers should be a list of BusPassenger')
        if not all(p.source == name for p in passengers):
            raise ValueError('passenger at the wrong stop')

        self.name = name
        self.position = position
        self.passengers = list(passengers)

    def init_animation(self, ax):

        """Initialise matplotlib animation for axes ax"""

        self.stop_line, = ax.plot([], [], 'ro', markersize=10)
        self.queue_line, = ax.plot([], [], 'bo')

        # Impatient passengers are indicated as magenta circles

        self.impatient_line, = ax.plot([], [], 'mo')
        x, y = self.position
        self.text = ax.text(x, y - 3, self.name, rotation=0,
                            verticalalignment='top', horizontalalignment='center')
        return [self.stop_line, self.queue_line, self.text]

    def update_animation(self):

        """Update matplotlib animation for axes ax"""

        x, y = self.position
        current_time = time.time()
        impatient_count = 0
        leave_count = 0
        for passenger in self.passengers:

            wait_time = current_time - passenger.arrive_time

            # Passengers become impatient after 7 seconds and leaves after 12 seconds

            if wait_time > 12:
                leave_count += 1

            elif wait_time > 7:
                impatient_count += 1

        # Redraw the bus stop

        self.stop_line.set_data([x], [y])

        # Redraw the queueing passengers

        qspace = 2
        num_passengers = len(self.passengers) - leave_count
        xdata = [x] * num_passengers
        ydata = [y + qspace * (n + 1) for n in range(num_passengers)]
        impatient_x = [x] * impatient_count
        impatient_y = [y + qspace * (n + 1) for n in range(impatient_count)]
        self.queue_line.set_data(xdata, ydata)
        self.impatient_line.set_data(impatient_x, impatient_y)

        # Return the patches for matplotlib to update

        return [self.stop_line, self.queue_line, self.impatient_line, self.text]


class Bus(Printable):

    """Bus traversing a linear bus route

    Parameters
    ==========

    name: str, name of the bus
    position: tuple(int,int), position of the bus
    direction: int, 1 if moving right and -1 if moving left
    passengers: list[Passenger], list of passengers

    Examples
    ========

    Create passengers and add them to a bus:

        >>> dave = BusPassenger('Dave', 'West St', 'East St', 1, "East")
        >>> bus = Bus('Number 47', (20,0), 1, speed, [dave])
        >>> bus
        Bus('Number 47', (20, 0), 1, speed, [BusPassenger('Dave', 'West St', 'East St')])

    """

    parameters = 'name', 'position', 'direction', 'speed', 'passengers'

    def __init__(self, name, position, direction, speed, passengers, stopped, stations, move,
                 rapid_express_local, capacity, passenger_count, busdir):

        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(c, int) for c in position)):
            raise TypeError('position should be a pair of ints')
        if direction not in {1, -1}:
            raise TypeError('direction should be 1 or -1')
        if not all(isinstance(p, BusPassenger) for p in passengers):
            raise TypeError('passengers should be a list of BusPassenger')
        if not (isinstance(speed, float) or isinstance(speed, int)):
            raise TypeError("speed should be a number")
        if not isinstance(move, str):
            raise TypeError('vert_or_hori should be either "v" or "h" for vertical and horizontal respectively')
        if move == 'v' and not position[0] == 75:
            raise ValueError('if bus is vertical it must be placed on x coordinate 75')
        if move == 'h' and not position[1] == 0:
            raise ValueError('if bus is vertical it must be placed on y coordinate 0')
        if not isinstance(stopped, bool):
            raise TypeError('stopped should be a boolean')
        if not isinstance(capacity, int):
            raise TypeError('capacity should be an integer')


        self.name = name
        self.position = position
        self.direction = direction
        self.speed = speed
        self.passengers = list(passengers)
        self.stopped = stopped
        self.stations = list(stations)
        self.move = move
        self.rapid_express_local = rapid_express_local
        self.capacity = capacity
        self.passenger_count = passenger_count
        self.busdir = busdir

    def init_animation(self, ax):

        """Initialise matplotlib animation for axes ax"""

        self.bus_line, = ax.plot([], [], 'gs', markersize=10)
        self.passenger_line, = ax.plot([], [], 'bo')
        x, y = self.position
        self.text = ax.text(x, y + 3, self.name,
                            verticalalignment='bottom', horizontalalignment='center')
        return [self.bus_line, self.passenger_line, self.text]

    def update_animation(self):

        """Update matplotlib animation for axes ax"""

        # Redraw the bus

        x, y = self.position
        self.bus_line.set_data([x], [y])

        # Redraw the passengers

        pspace = 2
        num_passengers = len(self.passengers)
        xdata = [x] * num_passengers
        ydata = [y - pspace * (n + 1) for n in range(num_passengers)]
        self.passenger_line.set_data(xdata, ydata)

        # Update text position

        self.text.set_x(x)
        self.text.set_y(y + 3)

        # Return the patches for matplotlib to update

        return [self.bus_line, self.passenger_line, self.text]


class BusNetwork(Printable):

    """Network of bus stops and buses.

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
4
    First create passengers, buses and bus stops:

        >>> dave = BusPassenger('Dave', 'West St', 'East St')
        >>> joan = BusPassenger('Joan', 'West St', 'East St')
        >>> bus = Bus('Number 47', (20, 0), 1, [dave])
        >>> busstops = [BusStop('West St', (0, 0), [joan]),
        ...             BusStop('East St', (100, 0), [])]

    Finally we are ready to create a complete linear bus route model with two
    stops and one bus:

        >>> model = BusNetwork(0, 100, busstops, [bus])

    This model has a route going from coordinate 0 to 100 with a bus stop at
    each end. There are two passengers Dave and Joan both wanting to go from
    East St to West St. Joan is waiting at the West St bus stop. Dave is on
    the bus which is already heading to East St and is currently at
    coordinate 20.

    """

    def __init__(self, vert_start, vert_end, hori_start, hori_end, s_start, s_end, stops, hori_stops, vert_stops,
                 s_stops, buses, rates=None):
        self.vert_start = vert_start
        self.hori_start = hori_start
        self.vert_end = vert_end
        self.hori_end = hori_end
        self.stops = list(stops)
        self.buses = list(buses)
        self.hori_stops = list(hori_stops)
        self.vert_stops = list(vert_stops)
        self.s_start = s_start
        self.s_end = s_end
        self.s_stops = list(s_stops)

        if rates is None:
            rates = {}
        else:
            rates = dict(rates)
        self.rates = rates

    def init(self):

        """Initialise the model after creating nand return events"""

        raise NotImplementedError("Subclasses should override this method")

    def update(self):

        """Updates the model through one timestep"""

        raise NotImplementedError("Subclasses should override this method")

    def init_animation(self, ax, ay, ax2, ay2, ax3):

        """Initialise matplotlib animation for axes ax and ay"""

        # Initialise self before child objects

        patches = self._init_animation(ax, ay, ax2, ay2, ax3)

        # Initialise all buses

        for bus in self.buses:
            patches += bus.init_animation(ax)

        # Initialise all bus stops

        for stop in self.stops:
            patches += stop.init_animation(ax)

        # List of patches for matplotlib to update

        return patches

    def update_animation(self, ax):

        """Update matplotlib animation for axes ax and ay"""

        # Redraw self before child objects

        patches = self._update_animation()

        # Redraw bus stops

        for stop in self.stops:
            patches += stop.update_animation()

        # Redraw buses
        for bus in self.buses:
            patches += bus.update_animation()

        self.text  = ax.text(0, 43, '---- ' + str(len(self.buses)) + ' buses in operation ----', fontsize=8)
        self.text1 = ax.text(0, 40, 'No. of boarded passengers: ' + str(self.passenger_count), fontsize=8)
        self.text2 = ax.text(0, 37, 'Total revenue: $' + str(self.income), fontsize=8)
        self.text3 = ax.text(0, 34, 'Fixed cost: $' + str(self.fixed_cost), fontsize=8)
        self.text4 = ax.text(0, 31, 'Oil cost: $' + str(self.oil_cost), fontsize=8)
        self.text5 = ax.text(0, 28, 'Total cost: $' + str(self.fixed_cost + self.oil_cost), fontsize=8)
        self.text6 = ax.text(0, 25, 'Net profit: $' + str(self.income - self.fixed_cost - self.oil_cost), fontsize=8)

        patches += [self.text, self.text1, self.text2, self.text3, self.text4, self.text5, self.text6]

        # List of patches for matplotlib to update

        return patches

    def _init_animation(self, ax, ay, ax2, ay2, ax3):

        """Initialise self for animation in axes ax and ay"""

        size = self.hori_end - self.hori_start
        delta = size // 10
        ax.set_xlim([self.hori_start - delta, self.hori_end + delta])
        ax.set_ylim([-size // 2, size // 2])
        ay.set_xlim([self.hori_start - delta, self.hori_end + delta])
        ay.set_ylim([-size // 2, size // 2])
        ax2.set_xlim([self.hori_start - delta, self.hori_end + delta])
        ax2.set_ylim([-size // 2, size // 2])
        ay2.set_xlim([self.hori_start - delta, self.hori_end + delta])
        ay2.set_ylim([-size // 2, size // 2])
        ax3.set_xlim([self.hori_start - delta, self.hori_end + delta])
        ax3.set_ylim([-size // 2, size // 2])
        self.route_line, = ax.plot([], [], 'k-', linewidth=3)
        self.route_line1, = ay.plot([], [], 'k-', linewidth=3)
        self.route_line2, = ax2.plot([], [], 'k-', linewidth=3)
        self.route_line3, = ay2.plot([], [], 'k-', linewidth=3)
        self.route_line4, = ax3.plot([], [], 'k-', linewidth=3)
        return [self.route_line, self.route_line1, self.route_line2, self.route_line3, self.route_line4]

    def _update_animation(self):

        """Redraw self for animation in axes ax and ay"""

        self.route_line.set_data([-5, 105], [0, 0])
        self.route_line1.set_data([75, 75], [35, -35])
        self.route_line2.set_data([55, 105], [30, 30])
        self.route_line3.set_data([5, 55], [-20, 30])
        self.route_line4.set_data([-5, 5], [-20, -20])
        return [self.route_line, self.route_line1, self.route_line2, self.route_line3, self.route_line4]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
