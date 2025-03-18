import random
import time
from os import get_terminal_size

from rich.align import Align
from rich.console import Console
from rich.text import Text

TARGETS = bytearray(b"*.'+.")


def blink_art(art: bytearray) -> list[tuple[int, int]]:
    # todo)) properly calculate and avoid hard-coding
    max_changes = random.randint(1, 20)
    changes = [(-1, -1)] * max_changes

    for k in range(max_changes):
        n = random.randint(0, 127)
        for i, s in enumerate(art):
            if s in TARGETS:
                if n == 0:
                    ch = art[i]
                    art[i] = ord(" ")
                    changes[k] = (i, ch)
                    break
                n -= 1

    return changes, art


def start_animation(console: Console, art: bytearray) -> None:
    try:
        with console.screen(hide_cursor=True):
            st_time = time.time()
            t_x, t_y = get_terminal_size()

            art_lines = art.splitlines()
            y = len(art_lines)

            k = (t_y - y) // 2

            while True:
                changes, art = blink_art(art)

                art_txt = art.decode()
                art_txt = "\n" * k + art_txt

                console.update_screen(Align(Text(art_txt), align="center"))

                for i, ch in changes:
                    if i == -1 and ch == -1:
                        continue
                    art[i] = ch

                if time.time() - st_time >= 15:
                    break

                time.sleep(0.1)
    except KeyboardInterrupt:
        pass


def main() -> None:
    console = Console()

    with open("art.txt", "rb") as file:
        art = bytearray(file.read())

    start_animation(console, art)


if __name__ == "__main__":
    main()
