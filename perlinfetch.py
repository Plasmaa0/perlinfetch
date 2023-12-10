# -*- coding: utf-8 -*-
import tabulate
from system_info import *
from perlin import perlin_ascii
from itertools import zip_longest, cycle
import termcolor
import shutil
import click

@click.command()
@click.option('-s', '--scale', default=8, help='Scale of perlin noise', show_default=True)
@click.option("-v", '--vertical', is_flag=True, show_default=True, default=False, help="""Save horizontal space by printing information in vertical direction. It will look like this:
              
              <NOISE/ASCII-IMAGE>
              
              <DATA>
              
              instead of (without this flag):
              
              <NOISE/ASCII-IMAGE> <DATA>""")
@click.option('--prefer-noise', is_flag=True, show_default=True, default=True, help="Fill remaining horizontal space with noise if there is not enough place for information table")
@click.option('--no-emojis', is_flag=True, show_default=True, default=False, help="Turn off emojis in table with data")
@click.option('--only-noise', is_flag=True, show_default=True, default=False, help="Don't fetch any device data. Fill the entire width of the terminal with perlin noise. Doesn't work with --ascii-file flag, in this case you'd better use 'cat' command :)")
@click.option('--ascii-file', help="Print ascii image from file instead of perlin noise")
def fetch(scale, vertical, ascii_file, prefer_noise, no_emojis, only_noise):
    """
    `PerlinFetch` is a system fetch program that displays beautifully colored perlin noise amongst system information in a nice table. This program is useful for anyone who wants to monitor their system's performance on a regular basis while enjoying a visually pleasing display.
    
    Displaying the perlin noise is a priority. So...
    
    If the width of the terminal is not enough to fully display the table with data about your device, then it will not be displayed. See --prefer-noise and --only-noise flags.
    
    If your terminal isn't wide enough but you still want to see the table consider looking at -v flag. It will save the horizontal space.
    """
    # print(f'{scale=}, {vertical=}, {ascii_file=}, {prefer_noise=}, {no_emojis=}, {only_noise=}')
    if only_noise:
        terminal_width, _ = shutil.get_terminal_size()
        h = 15
        w = terminal_width
        print(perlin_ascii(h,w,scale))
        return
    data_with_emojis = [
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
    
    if no_emojis:
        prepared_data = [
            [j, k] for i,j,k in data_with_emojis
        ]
    else:
        prepared_data = [
            [(i+' '+j+chr(24)), k] for i,j,k in data_with_emojis
        ]

    colors = list(termcolor.COLORS.keys())
    colors.remove('black')
    colors.remove('grey')
    colors.remove('dark_grey')
    colors = cycle(colors)
    next(colors)
    for line in prepared_data:
        line[0] = termcolor.colored(line[0], next(colors))
    table = tabulate.tabulate(prepared_data, tablefmt="simple_outline")

    terminal_width, _ = shutil.get_terminal_size()
    h = 15
    w = 40
    if terminal_width < len(table.split('\n')[0])+1+(0 if vertical else w):
        table = ''
        if prefer_noise:
            w=terminal_width-1
    horizontal = not vertical
    perlin = ascii_file is None
    if horizontal:
        if perlin:
            lines = [i.rstrip('\n') for i in perlin_ascii(h,w,scale).split('\n')]
            l = len(lines[1])
            for artline, infoline in zip_longest(lines, table.split('\n')):
                infoline = infoline if infoline is not None else ''
                if artline is not None:
                    print(artline, infoline)
                else:
                    print(' '*w, infoline)
        else:
            with open(ascii_file, 'r') as f:
                lines = [i.rstrip('\n') for i in f.readlines()]
                l = len(lines[0])
                for artline, infoline in zip_longest(lines, table.split('\n'), ):
                    infoline = infoline if infoline is not None else ''
                    if artline is not None:
                        print(termcolor.colored(artline, next(colors)), infoline)
                    else:
                        print(' '*l, infoline)
    else:
        if perlin:
            print(perlin_ascii(h,w,scale))
            print(table)
        else:
            with open(ascii_file, 'r') as f:
                lines = [termcolor.colored(i, next(colors)) for i in f.readlines() if len(i.strip())>0]
                lines = ''.join(lines).rstrip('\n')
                print(lines)
            print(table)

if __name__ == '__main__':
    fetch()