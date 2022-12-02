import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from busstop.objects import Bus, BusStop, BusPassenger
from busstop.linear import LinearBusRouteModel


def animate_model(model):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax2 = fig.add_axes([0, 0, 1, 1])
    ax3 = fig.add_axes([0, 0, 1, 1])
    ay = fig.add_axes([0, 0, 1, 1])
    ay2 = fig.add_axes([0, 0, 1, 1])
    time = -1  # time
    events = model.init()

    # Output messages as a string variable

    for event in events:
        output_string = ''
        for element in event:
            output_string += str(element)
        print(output_string)

    def init():

        # Initialise the graphics

        return model.init_animation(ax, ay, ax2, ay2, ax3)

    def update(frame_number):

        # Update the simulation

        time = frame_number
        events = model.update()

        # Output messages as a string variable

        for event in events:
            output_string = ''
            for element in event:
                output_string += str(element)
            print(output_string)

        # Update the graphics

        return model.update_animation(ax)

    animation = FuncAnimation(fig, update, init_func=init, blit=True)
    plt.show()
