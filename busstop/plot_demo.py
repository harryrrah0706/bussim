from busstop.plotting_function import *


def plot_avg_wait_time(avg_wait_time1, avg_wait_time2):
    avg_wait(avg_wait_time1, avg_wait_time2)

def plot_rates(average_count1, average_count2, average_count3):
    rates(average_count1, average_count2, average_count3)

def plot_revenues(revenue1, revenue2 ,revenue3, plot_time1, plot_time2, plot_time3):
    revenues(revenue1, revenue2 ,revenue3, plot_time1, plot_time2, plot_time3)

def plot_pie(passenger_ratio):
    pie(passenger_ratio)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
