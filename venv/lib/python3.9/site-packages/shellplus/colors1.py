from rich.console import Console

colors = {
    'forest': "#0e3a0e",
    'hot pink': "#ff0055",
    'sky blue': "#0face9",
    'chili': "#df3b28",
    'salmon': "#df3b28",
    'gum pink': "#f8369d",
    'bubblegum': "#f8369d",
    'green apple': "#b3e52a",
    'sour apple': "#b3e52a",
    'greenyellow': "#b3e52a",
    'yellowgreen': "#b3e52a",
    'diva': "#ccace3",
    'navy': "#020563",
    'dark teal': "#55aa88",
    'dteal': "#55aa88"
}


def print(message, color):
    shell = Console()
    stil = colors.get(color, '')
    shell.print(f'[{stil}]{message}[/{stil}]')