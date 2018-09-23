from __future__ import print_function
import sys
import re
from functools import partial


def flush_print(st, *args, **kwargs):
    end = kwargs.pop('end', '\n')
    if args:
        st = st % args
    print(st, end=end)
    if sys.stdout.isatty():
        sys.stdout.flush()


def cprint(st, *args, **kwargs):
    color = kwargs.get('color')
    if color and color not in COLORS:
        color = None
    style = kwargs.get('style')
    if style and style not in STYLES:
        style = None
    if args:
        st = st % args
    print(colorize(st, fg=color, style=style), end=kwargs.get('end', ''))
    sys.stdout.flush()


def dot_lead(st, *args, **kwargs):
    width = kwargs.pop('width', 60)
    if args:
        st = st % args
    dots = '.' * (width - len(st))
    return f'{st}{dots}'


def dot_leader(st, *args, **kwargs):
    width = kwargs.pop('width', 60)
    if args:
        st = st % args
    dots = '.' * (width - len(st))
    flush_print('%s%s', st, dots, **kwargs)


COLORS = (
    'black', 'red', 'green', 'yellow',
    'blue', 'magenta', 'cyan', 'white')
STYLES = (
    'bold', 'faint', 'italic', 'underline',
    'blink', 'blink2', 'negative',
    'concealed', 'crossed')


def colorize(s, fg=None, bg=None, style=None):
    sgr = []

    if fg:
        if fg in COLORS:
            sgr.append(f'{30 + COLORS.index(fg)}')
        elif isinstance(fg, int) and 0 <= fg <= 255:
            sgr.append(f'38;5;{fg}')
        else:
            raise Exception(f'Invalid color [{fg}]')

    if bg:
        if bg in COLORS:
            sgr.append(f'{40 + COLORS.index(bg)}')
        elif isinstance(bg, int) and 0 <= bg <= 255:
            sgr.append(f'48;5;{bg}')
        else:
            raise Exception(f'Invalid color "{bg}"')

    if style:
        for st in style.split('+'):
            if st in STYLES:
                sgr.append(str(1 + STYLES.index(st)))
            else:
                raise Exception(f'Invalid style "{st}"')

    if sgr:
        prefix = '\x1b[' + ';'.join(sgr) + 'm'
        suffix = '\x1b[0m'
        return f'{prefix}{s}{suffix}'
    else:
        return s


def strip_color(s):
    return re.sub('\x1b\[.+?m', '', s)


# Foreground shortcuts
black = partial(colorize, fg='black')
red = partial(colorize, fg='red')
green = partial(colorize, fg='green')
yellow = partial(colorize, fg='yellow')
blue = partial(colorize, fg='blue')
magenta = partial(colorize, fg='magenta')
cyan = partial(colorize, fg='cyan')
white = partial(colorize, fg='white')

# Style shortcuts
bold = partial(colorize, style='bold')
faint = partial(colorize, style='faint')
italic = partial(colorize, style='italic')
underline = partial(colorize, style='underline')
blink = partial(colorize, style='blink')
blink2 = partial(colorize, style='blink2')
negative = partial(colorize, style='negative')
concealed = partial(colorize, style='concealed')
crossed = partial(colorize, style='crossed')


def notice(st, lead_length=50, st_color=None):
    while len(st) > lead_length - 2:
        lead_length += 10
    f = dot_lead(st, width=lead_length)
    if st_color in COLORS:
        f = colorize(f, fg=st_color)
    flush_print(f, end='')


def notice_end(st=None, *args, **kwargs):
    if st:
        st_color = kwargs.get('color')
        st_style = kwargs.get('style')
        if st_color not in COLORS:
            st_color = 'yellow'
        if st_style not in STYLES:
            st_style = None
        flush_print(colorize(st, fg=st_color, style=st_style), *args, end='\n')
    else:
        flush_print('OK')


