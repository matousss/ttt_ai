import PySimpleGUI as sg

sg.theme('black')
# ○ ⨉
layout = [[sg.Button(size=(7, 3), key=f'{i}-{j}', font=('Arial', 30)) for i in range(3)] for j in range(3)]
board = [[None for _ in range(3)] for _ in range(3)]

switch = False


def get_char():
    global switch
    switch = not switch
    return '◯' if switch else '⨉'


def check_if_win(x, y):
    p = board[x][y]
    for v in board[x]:
        if v != p:
            break
    else:
        return True
    for i in range(3):
        if board[i][y] != p:
            break
    else:
        return True

    for j in range(3):
        if board[j][j] != p:
            break
    else:
        return True

    for t in (board[0][2], board[1][1], board[2][0]):
        if t != p:
            break
    else:
        return True

    return False


window = sg.Window('Window Title', layout)


def click(e):
    s = e.split('-')
    x, y = int(s[0]), int(s[1])
    board[x][y] = switch
    c = get_char()
    window[e].update(text=c, disabled=True)
    return check_if_win(x, y), c

def main():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break

        win, c = click(event)
        if win:
            print('vyhrává: ' + c)
            break


if __name__ == '__main__':
    main()

    pass
