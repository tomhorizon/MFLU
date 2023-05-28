import PySimpleGUI as sg
from datetime import datetime, timedelta

def format_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f'{hours:02d}:{minutes:02d}'

def main():
    menu_options = ['Temperature Controlled', 'Auto Complete', 'Oxidation Time']
    current_option_index = 0
    stored_values = ['Yes', 'Yes', 0]
    option_formats = ['yesno', 'yesno', 'time']
    button_names = [
        ['Furnace 1', 'Off', 'Furnace 2'],
        ['Wet O2', 'N2', 'Dry O2']
    ]

    error_codes = {
        1: "Error 1: Something went wrong.",
        2: "Error 2: Another error occurred.",
        3: "Error 3: Oops, an error happened."
    }


    layout = [[sg.Text('Use left and right arrow keys to scroll through menu options')]]

    button_layout1 = []
    for i in range(len(menu_options)):
        if option_formats[i] == 'time':
            button_layout1.append(sg.Button(f"{menu_options[i]} (Value: {format_time(stored_values[i])})", key=f'-OPTION{i}-', button_color=('white', 'darkgrey')))
        elif option_formats[i] == 'yesno':
            button_layout1.append(sg.Button(f"{menu_options[i]} (Value: {stored_values[i]})", key=f'-OPTION{i}-', button_color=('white', 'darkgrey')))

    button_layout2 = []
    button_layout2.append([sg.Button(button_names[0][i], size=(10, 3), button_color=('white', 'darkgrey')) for i in range(3)])
    button_layout2.append([sg.Button(button_names[1][i], size=(10, 3), button_color=('white', 'darkgrey')) for i in range(3)])
    image = [sg.Image(key='-IMAGE-', size=(200, 200))]
    error_window = [sg.Multiline(size=(50, 5), key='-OUTPUT-', disabled=True, autoscroll=True)]

    layout.append([button_layout1])
    layout.append([button_layout2])
    layout.append(image)
    layout.append(error_window)
    layout.append([sg.Button('Exit')])


    window = sg.Window('Menu', layout, return_keyboard_events=True, size=(1024, 600))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Left:37':
            if current_option_index > 0:
                current_option_index -= 1
        elif event == 'Right:39':
            if stored_values[0] == 'No':
                current_option_index = 0
            elif stored_values[1] == 'No':
                if current_option_index < len(menu_options) - 2:
                    current_option_index += 1
            else:
                if current_option_index < len(menu_options) - 1:
                    current_option_index += 1

        elif event == 's':
            popup_title = f'Change {menu_options[current_option_index]} '

            if option_formats[current_option_index] == 'time':
                popup_layout = [[sg.Text(popup_title)],
                                [sg.Text('Use left and right arrow keys to increment or decrement the value')],
                                [sg.Text('Value: '), sg.Text(format_time(stored_values[current_option_index]), key='-VALUE-', size=(5, 1))],
                                [sg.Button('OK')]]
                increment_value = 5
            elif option_formats[current_option_index] == 'yesno':
                popup_layout = [[sg.Text(popup_title)],
                                [sg.Text('Use left and right arrow keys to toggle the value')],
                                [sg.Text('Value: '), sg.Text(stored_values[current_option_index], key='-VALUE-', size=(5, 1))],
                                [sg.Button('OK')]]
                increment_value = None

            popup_window = sg.Window(popup_title, popup_layout, return_keyboard_events=True)

            while True:
                popup_event, popup_values = popup_window.read()

                if popup_event == sg.WINDOW_CLOSED or popup_event == 'OK' or popup_event == 's':
                    break
                elif popup_event == 'Left:37':
                    if option_formats[current_option_index] == 'time':
                        stored_values[current_option_index] -= increment_value
                        stored_values[current_option_index] = max(stored_values[current_option_index], 0)  # Restrict to a minimum of 0
                    elif option_formats[current_option_index] == 'yesno':
                        stored_values[current_option_index] = 'No'
                elif popup_event == 'Right:39':
                    if option_formats[current_option_index] == 'time':
                        stored_values[current_option_index] += increment_value
                    elif option_formats[current_option_index] == 'yesno':
                        stored_values[current_option_index] = 'Yes'

                popup_window['-VALUE-'].update(format_time(stored_values[current_option_index])) if option_formats[current_option_index] == 'time' else popup_window['-VALUE-'].update(stored_values[current_option_index])

            popup_window.close()

            # Update button text with new stored value
            button_key = f'-OPTION{current_option_index}-'
            if option_formats[current_option_index] == 'time':
                window[button_key].update(text=f"{menu_options[current_option_index]} (Value: {format_time(stored_values[current_option_index])})")
            elif option_formats[current_option_index] == 'yesno':
                window[button_key].update(text=f"{menu_options[current_option_index]} (Value: {stored_values[current_option_index]})")

        # Update button colors
        for i in range(len(menu_options)):
            button_key = f'-OPTION{i}-'
            if i == current_option_index:
                window[button_key].update(button_color=('white', 'red'))
            else:
                window[button_key].update(button_color=('white', 'darkgrey'))

        # Enable/disable "Oxidation Time" based on "Temperature Controlled" value
        if stored_values[1] == 'No' and current_option_index == 2:
            current_option_index = 1

        # Update the image element
        image_filename = 'image1.png' #if all(gpio_statuses) else 'image2.jpg'
        window['-IMAGE-'].update(filename=image_filename)

        # Simulate error messages based on button events
        if event in error_codes:
            error_message = error_codes[event]
            window['-OUTPUT-'].print(error_message)

    window.close()

if __name__ == '__main__':
    main()
