from rich.console import Console

console = Console()

def cprint(text="", style: str = None, end: str = "\n", markup: bool = True): # Rich wrapper
    if style:
        console.print(f"[{style}]{text}[/]", end=end, markup=markup)
    else:
        console.print(text, end=end, markup=markup)
