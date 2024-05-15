from rich import style
from rich.console import Console

styles = {
    'info': 'bold blue',
    'warn': 'italic yellow',
    'warning': 'italic yellow',
    'err': 'bold red',
    'error': 'bold red',
    'serr': style.Style(color='#FA6E69', bold=True),
    'serror': style.Style(color='#FA6E69', bold=True),
    'softerr': style.Style(color='#FA6E69', bold=True),
    'softerror': style.Style(color='#FA6E69', bold=True),
    'note': 'dim italic',
    'worry': style.Style(color='#fdff8e'),
    'invalid': style.Style(color='#ff3d3d', underline=True, italic=True),
    'marked1': 'reverse yellow',
    'marked2': 'reverse green',
    'no_intr': 'strikethrough dim',
    'nointr': 'strikethrough dim',
    'no_interest': 'strikethrough dim',
    'nointerest': 'strikethrough dim',
    'unimportant': 'strikethrough dim',
    'comment': style.Style(color='#186218', dim=True),
}

def print_styled(message, style):
    shell = Console()
    stil = styles.get(style, '')
    shell.print(f'[{stil}]{message}[/{stil}]')
