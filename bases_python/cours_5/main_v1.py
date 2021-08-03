import PySimpleGUI as sg

sg.theme("BluePurple")

layout = [
    [
        sg.Text(
            "",
            background_color="#ffffff",
            size=(15, 1),
            font=("Cambria", 19),
            justification="right",
            key="output",
        )
    ],
    [sg.Button("7"), sg.Button("8"), sg.Button("9"), sg.Button("/")],
    [sg.Button("4"), sg.Button("5"), sg.Button("6"), sg.Button("*")],
    [sg.Button("1"), sg.Button("2"), sg.Button("3"), sg.Button("-")],
    [sg.Button("0"), sg.Button("."), sg.Button("="), sg.Button("+")],
    [sg.Button("("), sg.Button(")"), sg.Button("Effacer", size=(12, 2))],
]

window = sg.Window(
    "Calculatrice", layout, default_button_element_size=(5, 2), auto_size_buttons=False
)

while True:
    event, values = window.read()
    # print(event, values)

    if event != "=":
        window["output"].update(window["output"].get() + str(event))

    if event == "Effacer":
        window["output"].update("")

    if event == "=":
        try:
            result = eval(window["output"].get())
        except (SyntaxError, ZeroDivisionError):
            result = "ERROR"
        window["output"].update(result)

    if event == sg.WIN_CLOSED:
        break

window.close()
