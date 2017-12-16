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


def cprint(color_fn, st, *args):
    if args:
        st = st % args
    print(color_fn(st), end='')
    sys.stdout.flush()


def dot_lead(st, *args, **kwargs):
    width = kwargs.pop('width', 60)
    if args:
        st = st % args
    dots = '.' * (width - len(st))
    return '%s%s' % (st, dots)


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


def color(s, fg=None, bg=None, style=None):
    sgr = []

    if fg:
        if fg in COLORS:
            sgr.append('%s' % (30 + COLORS.index(fg),))
        elif isinstance(fg, int) and 0 <= fg <= 255:
            sgr.append('38;5;%d' % int(fg))
        else:
            raise Exception('Invalid color [%s]' % fg)

    if bg:
        if bg in COLORS:
            sgr.append(str(40 + COLORS.index(bg)))
        elif isinstance(bg, int) and 0 <= bg <= 255:
            sgr.append('48;5;%d' % bg)
        else:
            raise Exception('Invalid color "%s"' % bg)

    if style:
        for st in style.split('+'):
            if st in STYLES:
                sgr.append(str(1 + STYLES.index(st)))
            else:
                raise Exception('Invalid style "%s"' % st)

    if sgr:
        prefix = '\x1b[' + ';'.join(sgr) + 'm'
        suffix = '\x1b[0m'
        return prefix + s + suffix
    else:
        return s


def strip_color(s):
    return re.sub('\x1b\[.+?m', '', s)


# Foreground shortcuts
black = partial(color, fg='black')
red = partial(color, fg='red')
green = partial(color, fg='green')
yellow = partial(color, fg='yellow')
blue = partial(color, fg='blue')
magenta = partial(color, fg='magenta')
cyan = partial(color, fg='cyan')
white = partial(color, fg='white')

# Style shortcuts
bold = partial(color, style='bold')
faint = partial(color, style='faint')
italic = partial(color, style='italic')
underline = partial(color, style='underline')
blink = partial(color, style='blink')
blink2 = partial(color, style='blink2')
negative = partial(color, style='negative')
concealed = partial(color, style='concealed')
crossed = partial(color, style='crossed')
