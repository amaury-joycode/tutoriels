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
    "Calculatrice",
    layout,
    default_button_element_size=(5, 2),
    auto_size_buttons=False,
    resizable=True,
    finalize=True,
    return_keyboard_events=True,
)
window.bind("<Configure>", "Configure")

authorized_keys = [
    "7",
    "8",
    "9",
    "/",
    "4",
    "5",
    "6",
    "*",
    "1",
    "2",
    "3",
    "-",
    "0",
    ".",
    "+",
    "(",
    ")",
]

while True:
    event, values = window.read()
    # print(event, values)

    if window["output"].get() == "ERROR":
        window["output"].update("")

    if event in authorized_keys:
        window["output"].update(window["output"].get() + str(event))

    if "BackSpace" in event:
        window["output"].update(window["output"].get()[:-1])

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

    if event == "Configure":
        for widget in window.element_list():
            widget.expand(True, True)
        window["output"].expand(True, False)

window.close()
