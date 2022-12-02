import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def avg_wait(avg_wait_time1, avg_wait_time2):
    labels = ["<=5", "6", "7", "8", "9", "10", "11", "12", ">12"]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    label1 = ax.bar(x - width/2, avg_wait_time1, width, label="More buses")
    label2 = ax.bar(x + width/2, avg_wait_time2, width, label="Less buses")
    ax.set_ylabel("Frequency")
    ax.set_title("Wait time for different number of buses")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(label1)
    autolabel(label2)

    fig.tight_layout()

    plt.show()

def rates(average_count1, average_count2, average_count3):
    plt.figure()
    rate = ("0.025", "0.05", "0.1")
    y_pos = np.arange(len(rate))
    frequency = [average_count1, average_count2, average_count3]
    plt.bar(y_pos, frequency, align = "center", alpha = 1.0)
    plt.xticks(y_pos, rate)
    plt.ylabel("Frequency")
    plt.xlabel("Rates")
    plt.title("Average number of passengers taking buses per minute")
    plt.show()

def revenues(revenue1, revenue2 ,revenue3, plot_time1, plot_time2, plot_time3):
    plt.figure
    x1 = plot_time1
    y1 = revenue1
    plt.plot(x1, y1, label = "Original model")

    x2 = plot_time2
    y2 = revenue2
    plt.plot(x2, y2, label = "2 buses removed")

    x3 = plot_time3
    y3 = revenue3
    plt.plot(x3, y3, label = "4 buses removed")

    plt.xlabel("Time(s)")
    plt.ylabel("Revenue")
    plt.title("Revenue vs Time for different number of buses")
    plt.legend()
    plt.show()

def pie(passenger_ratio):
    labels = "Board passengers", "Leave passengers"
    sizes = passenger_ratio
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode = explode, labels = labels, autopct = "%1.1f%%", shadow = True, startangle = 90)
    ax1.axis("Equal")
    plt.show()
        

if __name__ == "__main__":
    import doctest

    doctest.testmod()

