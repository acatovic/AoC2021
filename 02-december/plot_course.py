from enum import Enum
import enum
from pathlib import Path
import sys
from typing import List, Tuple


class Cmd(str, Enum):
    forward = "forward"
    up = "up"
    down = "down"


def calc_final_pos_with_aim(commands: List[Cmd], vals: List[int]) -> int:
    aim = 0
    horiz_pos = 0
    depth = 0
    for i, cmd in enumerate(commands):
        if cmd == Cmd.down:
            aim += vals[i]
        elif cmd == Cmd.up:
            aim -= vals[i]
        elif cmd == Cmd.forward:
            horiz_pos += vals[i]
            depth += aim * vals[i]
        else:
            raise ValueError(f"Command '{cmd}' not found.")

    return horiz_pos * depth

def load_course_data(path: str) -> Tuple[List[Cmd], List[int]]:
    """Return tuple (commands, values)."""
    commands = []
    vals = []

    with Path(path).open() as f:
        for line in f:
            cmd_str, val = line.strip().split()
            commands.append(Cmd(cmd_str))
            vals.append(int(val))
    
    return commands, vals

def main():
    path = sys.argv[1]
    commands, vals = load_course_data(path)
    final_position = calc_final_pos_with_aim(commands, vals)
    print(final_position) 

if __name__ == "__main__":
    main()