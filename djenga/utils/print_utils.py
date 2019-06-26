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


def _ansi_color(x, offset, ansi_code):
    if x:
        if x in COLORS:
            return [ f'{offset + COLORS.index(x)}' ]
        if isinstance(x, int) and 0 <= x <= 255:
            return [ f'{ansi_code};5;{x}' ]
        raise Exception('Invalid color [{x}]')
    return []


def _style_codes(style):
    codes = []
    if style:
        for st in style.split('+'):
            if st in STYLES:
                codes.append(f'{(1 + STYLES.index(st))}')
            else:
                raise Exception('Invalid style "{st}"')
    return codes


def color(s, fg=None, bg=None, style=None):
    sgr = _ansi_color(fg, 30, 38) + _ansi_color(bg, 40, 48)
    sgr += _style_codes(style)
    if sgr:
        return f"\x1b[{';'.join(sgr)}m{s}\x1b[0m"
    return s


def strip_color(s):
    return re.sub(r'\x1b\[.+?m', '', s)


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
