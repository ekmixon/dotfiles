#!/usr/bin/env python3

color_groups = [
    [('red', None), ('green', None), ('yellow', None), ('magenta', None),
     ('cyan', None)],
    [('black', 'light_red'), ('black', 'light_green'),
     ('black', 'light_yellow'), ('black', 'light_magenta'),
     ('black', 'light_cyan')]
]
cmd = ['git', 'blame', '--line-porcelain']


###############################################
# START Base16 Tomorrow Dark style for Pygments
###############################################
# https://github.com/idleberg/base16-pygments/blob/master/base16-tomorrow.dark.py

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal


BACKGROUND = "#1d1f21"
CURRENT_LINE = "#282a2e"
SELECTION = "#373b41"
FOREGROUND = "#ffffff"
COMMENT = "#969896"
RED = "#cc6666"
ORANGE = "#de935f"
YELLOW = "#f0c674"
GREEN = "#b5bd68"
AQUA = "#8abeb7"
BLUE = "#81a2be"
PURPLE = "#b294bb"




class base16_tomorrow_dark(Style):

    default_style = ''

    background_color = BACKGROUND
    highlight_color = SELECTION

    background_color = BACKGROUND
    highlight_color = SELECTION

    styles = {
        Text: FOREGROUND,
        Whitespace: "",
        Error: RED,
        Other: "",
        Comment: COMMENT,
        Comment.Multiline: "",
        Comment.Preproc: "",
        Comment.Single: "",
        Comment.Special: "",
        Keyword: PURPLE,
        Keyword.Constant: "",
        Keyword.Declaration: "",
        Keyword.Namespace: AQUA,
        Keyword.Pseudo: "",
        Keyword.Reserved: "",
        Keyword.Type: YELLOW,
        Operator: AQUA,
        Operator.Word: "",
        Punctuation: FOREGROUND,
        Name: FOREGROUND,
        Name.Attribute: BLUE,
        Name.Builtin: "",
        Name.Builtin.Pseudo: "",
        Name.Class: YELLOW,
        Name.Constant: RED,
        Name.Decorator: AQUA,
        Name.Entity: "",
        Name.Exception: RED,
        Name.Function: BLUE,
        Name.Property: "",
        Name.Label: "",
        Name.Namespace: YELLOW,
        Name.Other: BLUE,
        Name.Tag: AQUA,
        Name.Variable: RED,
        Name.Variable.Class: "",
        Name.Variable.Global: "",
        Name.Variable.Instance: "",
        Number: ORANGE,
        Number.Float: "",
        Number.Hex: "",
        Number.Integer: "",
        Number.Integer.Long: "",
        Number.Oct: "",
        Literal: ORANGE,
        Literal.Date: GREEN,
        String: GREEN,
        String.Backtick: "",
        String.Char: FOREGROUND,
        String.Doc: COMMENT,
        String.Double: "",
        String.Escape: ORANGE,
        String.Heredoc: "",
        String.Interpol: ORANGE,
        String.Other: "",
        String.Regex: "",
        String.Single: "",
        String.Symbol: "",
        Generic: "",
        Generic.Deleted: RED,
        Generic.Emph: "italic",
        Generic.Error: "",
        Generic.Heading: f"bold {FOREGROUND}",
        Generic.Inserted: GREEN,
        Generic.Output: "",
        Generic.Prompt: f"bold {COMMENT}",
        Generic.Strong: "bold",
        Generic.Subheading: f"bold {AQUA}",
        Generic.Traceback: "",
    }



#############################################
# END Base16 Tomorrow Dark style for Pygments
#############################################


from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import Terminal256Formatter
from tabulate import tabulate
from colored import fg, bg, attr

import subprocess
from sys import argv


def lines_starting_with(all_lines, prefix):
    grepped = [l for l in all_lines if l.startswith(prefix)]
    return [l.split(prefix)[1] for l in grepped]


def main():
    cmd.extend(argv[1:])

    gbl_raw = (subprocess.run(cmd, stdout=subprocess.PIPE).stdout
               .decode().split('\n'))
    code = '\n'.join(lines_starting_with(gbl_raw, '\t'))
    authors_by_line = lines_starting_with(gbl_raw, 'author ')
    authors_unique = sorted(list(set(authors_by_line)))

    formatter = Terminal256Formatter(style=base16_tomorrow_dark)
    highlighted_raw = highlight(code, guess_lexer(code), formatter)
    highlighted = highlighted_raw.split('\n')

    color_codes = []
    for group in color_groups:
        for fg_color, bg_color in group:
            color_code = fg(fg_color)
            if bg_color:
                color_code += bg(bg_color)
            color_codes.append(color_code)

    author_color_codes = {author: color_codes.pop(0)
                          for author in authors_unique}

    pretty_blame = []
    for i in range(min(len(authors_by_line), len(highlighted))):
        author = authors_by_line[i]
        pretty_blame.append((
            author_color_codes[author] + author,
            fg('dark_gray') + str(i),
            attr('reset') + highlighted[i]
        ))

    print(tabulate(pretty_blame, tablefmt='plain'))


if __name__ == '__main__':
    main()
