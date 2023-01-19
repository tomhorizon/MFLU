import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# graph testing
matplotlib.use('TkAgg')
x_len = 200                     # Number of points to display
y_range = [0, 40]               # Range of possible Y values to display
fig1 = plt.figure(facecolor = "black", edgecolor="white")              # figure 1 setup
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.5)

params = {"text.color" :        "white",
          "xtick.color" :       "white",
          "ytick.color" :       "white",
          "axes.facecolor":     "black",
          "axes.labelcolor":    "white",
          "figure.edgecolor":   "black",
          "axes.titlecolor":    "white"}             # color
plt.rcParams.update(params)


ax1 = fig1.add_subplot(2, 1, 1)   # add subplot 1 axis
ax2 = fig1.add_subplot(2, 1, 2)   # add subplot 2 axis
xs1 = list(range(-200, 0))       # x data limits
ys1 = [0] * x_len                # y data limits (starts empty)
xs2 = list(range(-200, 0))       # x data limits
ys2 = [0] * x_len                # y data limits (starts empty)
ax1.set_ylim(y_range)            # limit y axis values
ax2.set_ylim(y_range)            # limit y axis values
temp_init1 = 20                # dummy initial temp value
temp_init2 = 30
line1, = ax1.plot(xs1, ys1)
line1.set_color("white")
line2, = ax2.plot(xs2, ys2)
line2.set_color("white")
ax1.set(title="Furnace 1 (Oxidation)",
        xlabel="Time (s)",
        ylabel="Temperature (deg C)")
ax2.set(title="Furnace 2 (Diffusion)",
        xlabel="Time (s)",
        ylabel="Temperature (deg C)")


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

sg.theme('Black')
col1 = [[sg.Text('User Input', font=22)],
        [sg.Text('')],
        [sg.Text('Furnace Selection')],
        [sg.Button('F1', size=(6,3), button_color='white on grey', disabled = False, key="F1Status"), sg.Button('F2', size=(6,3), button_color='white on grey', disabled = True)],
        [sg.Text('')],
        [sg.Text('Oxygen Selection')],
        [sg.Button('Dry', size=(6,3), button_color='white on grey', disabled = True), sg.Button('Wet', size=(6,3), button_color='white on grey', disabled = True)],
        [sg.Text('')],
        [sg.Text('Oxidation Timer')],
        [sg.Button('00H', size=(6,3), button_color='white on grey', disabled = True), sg.Button('00M', size=(6,3), button_color='white on grey', disabled = True)]]

col2 = [[sg.Text('System Diagram', font=22)],
        [sg.Button('H2O', size=(6,3), button_color='white on grey', disabled = True), sg.Button('O2', size=(6,3), button_color='white on grey', disabled = True), sg.Button('N2', size=(6,3), button_color='white on grey', disabled = True)],
        [sg.Button('v', size=(1,2), button_color='white on grey', disabled = True), sg.Text('      '), sg.Button('v', size=(1,2), button_color='white on grey', disabled = True), sg.Button('v', size=(1,2), button_color='white on grey', disabled = True), sg.Text('      '), sg.Button('v', size=(1,2), button_color='white on grey', disabled = True)],
        [sg.Button('Bubbler', size=(10,3), button_color='white on grey', disabled = True), sg.Button('v', size=(1,3), button_color='white on grey', disabled = True), sg.Text('    '), sg.Button('v', size=(1,3), button_color='white on grey', disabled = True)],
        [sg.Text('    '), sg.Button('v')],
        [sg.InputText('F1 Temp', key = "-Temp1-")],
        [sg.Submit(key="submitted")]]

col3 = [[sg.Text('Current Temperatures', font=22)],
        [sg.Canvas(key='-CANVAS-', background_color="black")]]

layout = [[sg.Column(col1, element_justification='c', size=(200, 600)),
           sg.Column(col2, element_justification='c', size=(200, 600)),
           sg.Column(col3, element_justification='c', size=(600, 600))]]

window = sg.Window('Test1', layout, finalize=True, size=(1050, 525))
fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig1)


def animate(i, ys1, ys2):
    print(i)
    temp_c1 = temp_init1 + random.randint(-3, 3)
    temp_c2 = temp_init2 + random.randint(-3, 3)

    ys1.append(temp_c1)
    ys1 = ys1[-x_len:]
    line1.set_ydata(ys1)

    ys2.append(temp_c2)
    ys2 = ys2[-x_len:]
    line2.set_ydata(ys2)

    return line1, line2,

while True:
    event, values = window.read()
    ani = animation.FuncAnimation(fig1, animate, fargs=(ys1, ys2,), interval=1000, blit=True)
    plt.show()
    print(event)
    window['-Temp1-'].update(ys1[-1])
    if event == sg.WIN_CLOSED:
        break
    if event == 'F1Status':
        window["F1Status"].update(button_color='white on red')

window.close()