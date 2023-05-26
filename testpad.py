import PySimpleGUI as sg
from datetime import datetime, timedelta

def format_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f'{hours:02d}:{minutes:02d}'

def main():
    menu_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    current_option_index = 0
    stored_values = [0] * len(menu_options)

    layout = [[sg.Text('Use arrow keys to scroll through menu options')]]

    # Add buttons with initial stored values
    for i in range(len(menu_options)):
        layout.append([sg.Button(f"{menu_options[i]} (Value: {format_time(stored_values[i])})", key=f'-OPTION{i}-', button_color=('white', 'lightgrey'))])

    layout.append([sg.Button('Exit')])

    window = sg.Window('Menu', layout, return_keyboard_events=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Up:38' and current_option_index > 0:
            current_option_index -= 1
        elif event == 'Down:40' and current_option_index < len(menu_options) - 1:
            current_option_index += 1
        elif event == 's':
            option_number = current_option_index + 1
            popup_title = f'Option {option_number} Popup'
            popup_layout = [[sg.Text(popup_title)],
                            [sg.Text('Use arrow keys to increment or decrement the value')],
                            [sg.Text('Value: '), sg.Text(format_time(stored_values[current_option_index]), key='-VALUE-', size=(5, 1))],
                            [sg.Button('OK')]]

            popup_window = sg.Window(popup_title, popup_layout, return_keyboard_events=True)

            while True:
                popup_event, popup_values = popup_window.read()

                if popup_event == sg.WINDOW_CLOSED or popup_event == 'OK' or popup_event == 's':
                    break
                elif popup_event == 'Up:38':
                    stored_values[current_option_index] += 5
                elif popup_event == 'Down:40':
                    stored_values[current_option_index] -= 5

                popup_window['-VALUE-'].update(format_time(stored_values[current_option_index]))

            popup_window.close()

            # Update button text with new stored value
            button_key = f'-OPTION{current_option_index}-'
            window[button_key].update(text=f"{menu_options[current_option_index]} (Value: {format_time(stored_values[current_option_index])})")

        # Update button colors
        for i in range(len(menu_options)):
            button_key = f'-OPTION{i}-'
            if i == current_option_index:
                window[button_key].update(button_color=('white', 'red'))
            else:
                window[button_key].update(button_color=('white', 'lightgrey'))

    window.close()

if __name__ == '__main__':
    main()
