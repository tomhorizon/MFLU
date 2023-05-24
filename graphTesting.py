from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

matplotlib.use('TkAgg')
x_len = 200  # Number of points to display
y_range = [0, 40]  # Range of possible Y values to display

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

xs = list(range(-200, 0))  # x data limits
ys = [0] * x_len  # y data limits (starts empty)
line1, = ax.plot(xs, ys)
ax.set(title="Furnace 1 (Oxidation)",
        xlabel="Time (s)",
        ylabel="Temperature (deg C)")


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# sg.theme('Black')

col1 = [[sg.Text('Current Temperatures', font=22)],
        [sg.Canvas(key='-CANVAS-', background_color="White")]]
layout = [[sg.Column(col1, element_justification='c', size=(1200, 600))]]
window = sg.Window('Test1', layout, finalize=True, size=(1500, 600))
fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)


def animate(i, xs, ys):
    print(i)
    # Read temperature (Celsius) from TMP102
    temp_c = 20 + random.randint(-3, 3)

    # Add x and y to lists
    xs.append(.05)
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')


while True:
    event, values = window.read()
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10, blit=True)
    plt.show()
    if event == sg.WIN_CLOSED:
        break

window.close()
