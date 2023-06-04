# -*- coding: utf-8 -*-
import tabulate
from system_info import *
from perlin import perlin_ascii
from itertools import zip_longest, cycle
import termcolor
import shutil

data = [
    ["🏠","host", f"{hostname()}"],
    ["💻","machine", f"{machine()}"],
    ["🐧","kernel", f"{kernel()}"],
    ["📦","distro", f"{distro()}"],
    ["🎨","WM", f"{wm()}"],
    ["📦","pkg", f"{packages()}"],
    ["🌐","IP", f"{ip()}"],
    ["💻","term", f"{term()}"],
    ["🐚","shell", f"{shell()}"],
    ["⏳","uptime", f"{uptime()}"],
    ["💻","CPU", f"{cpu()}"],
    ["🎮","GPU", f"{gpu()}"],
    ["💻","resolution", f"{screen_res()}"],
    ["💾","RAM", f"{ram_load()}"]
]
data_with_emojis = [
    [(i+' '+j+chr(24)), k] for i,j,k in data
]

colors = list(termcolor.COLORS.keys())
# print(colors)
colors.remove('black')
colors.remove('grey')
colors.remove('dark_grey')
# for color in colors:
#     print(termcolor.colored('test', color), color)
# print(termcolor.colored('Hello, World!', random.choice(colors)))
colors = cycle(colors)
next(colors)
for line in data_with_emojis:
    line[0] = termcolor.colored(line[0], next(colors))
table = tabulate.tabulate(data_with_emojis, tablefmt="simple_outline")

h = 15
w = 40
terminal_width, _ = shutil.get_terminal_size()
# terminal_width = min(int(os.environ.get("COLUMNS")), terminal_width)
# print(terminal_width,len(table.split('\n')[0])+w)
if terminal_width < len(table.split('\n')[0])+w:
    table = ''
# next(colors)
horizontal = True
perlin = True
if horizontal:
    if perlin:
        lines = [i.rstrip('\n') for i in perlin_ascii(h,w).split('\n')]
        l = len(lines[1])
        for artline, infoline in zip_longest(lines, table.split('\n')):
            infoline = infoline if infoline is not None else ''
            if artline is not None:
                print(artline, infoline)
            else:
                print(' '*w, infoline)
    else:
        with open('art.txt', 'r') as f:
            lines = [i.rstrip('\n') for i in f.readlines()]
            l = len(lines[0])
            for artline, infoline in zip_longest(lines, table.split('\n'), ):
                infoline = infoline if infoline is not None else ''
                if artline is not None:
                    print(termcolor.colored(artline, next(colors)), infoline)
                else:
                    print(' '*l, infoline)
else:
    with open('art.txt', 'r') as f:
        lines = [termcolor.colored(i, next(colors)) for i in f.readlines() if len(i.strip())>0]
        lines = ''.join(lines).rstrip('\n')
        print(lines)
    print(table)
