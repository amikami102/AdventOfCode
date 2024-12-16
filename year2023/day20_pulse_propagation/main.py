"""
Part 2 required peaking at the puzzle input to see which modules were connected to 'rx'.
It turns out 'rx' has only one module connected to it, 
which in turn has four conjunction modules connected to it:
    ... -> (&nx, &sp, &cc, &jq) -> &dd -> rx.
'rx' receives its first low pulse when 'dd' receives a high pulse from 
'nx', 'sp', 'cc', 'and 'jq'.
Count the button pushes it takes for these four conjunction modules
to send a high pulse to 'dd': p_nx, p_sp, p_cc, p_jq.
The least common multiple of p_nx, p_sp, p_cc, and p_jq is the solution.
Consulted https://github.com/wleftwich/aoc/blob/main/2023/20-pulse-propagation.ipynb,
accessed 2024-01-15.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass
from typing import Iterator, Callable
from enum import Enum, IntFlag
from collections import deque, Counter
from itertools import count
from math import lcm

MODULE_RE = re.compile(r'([%&])?(\w+) -> (.+)')


class ModuleType(Enum):
    FLIPFLOP = '%'
    CONJUNCTION = '&'
    BROADCAST = 'broadcaster'


class Pulse(IntFlag):
    LOW = 0
    HIGH = 1


class Switch(IntFlag):
    OFF = 0
    ON = 1


@dataclass
class Module:
    mtype: ModuleType
    name: str
    destinations: list[str]
    state: tuple[Switch, Pulse] | int | None = None
    
    def receive(self, sender: str, pulse: Pulse) -> Iterator[tuple[str, Pulse, str]]:
        pulse_sent = None
        match self.mtype:
            case ModuleType.FLIPFLOP:
                if pulse is Pulse.LOW:
                    self.state ^= 1
                    pulse_sent = Pulse.HIGH if self.state is Switch.ON else Pulse.LOW
                else:
                    return ()
            case ModuleType.CONJUNCTION:
                self.state[sender] = pulse
                pulse_sent = Pulse.LOW if \
                    all(previous is Pulse.HIGH for previous in self.state.values())\
                    else Pulse.HIGH
            case ModuleType.BROADCAST:
                pulse_sent = pulse
        return (
            (self.name, pulse_sent, dest) 
            for dest in self.destinations
        )


def initialize(modules: dict[str, Module]) -> None:
    """
    Initialize the `state` attribute of the module in `modules`
    according to their types.
    """
    for name, module in modules.items():
        match module.mtype:
            case ModuleType.BROADCAST:
                module.state = None
            case ModuleType.FLIPFLOP:
                module.state = Switch.OFF
            case ModuleType.CONJUNCTION:
                module.state = {
                    src: Pulse.LOW for src in modules 
                    if name in modules[src].destinations
                }


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def parse_configuration(configuration: list[str]) -> dict[str, Module]:
    modules = {
        name: module
        for name, module in 
        (parse_module(line) for line in configuration)
    }
    initialize(modules)
    return modules


def parse_module(line: str) -> Module:
    mtype, name, destinations = MODULE_RE.match(line).groups()
    return name, Module(
        ModuleType(mtype) if mtype else ModuleType.BROADCAST, 
        name,
        destinations.split(', ')
    )

def push_button(modules: dict[str, Module]) -> Iterator[Pulse]:
    """(Part 1)
    Push button by sending a low pulse to 'broadcaster' from 'button'.
    Queue pulses as they get generated and process them in FIFO order
    until there are no more pulses in the queue.
    """
    pulses = deque()
    pulses.append(('button', Pulse.LOW, 'broadcaster'))
    while pulses:
        sender, pulse, receiver = pulses.popleft()
        yield (sender, pulse, receiver)
        if module := modules.get(receiver):
            for next_pulse in module.receive(sender, pulse):
                pulses.append(next_pulse)


def send_high_pulse_to_dd(module_connected_to_dd: str) -> Callable:
    """(Part 2)
    Return a decorated function that returns True if 
    `module_connected_to_dd` sends a high pulse to 'dd', False otherwise.
    """
    def wrapper(sender: str, pulse: Pulse, receiver: str) -> bool:
        return (
            sender == module_connected_to_dd
            and pulse is Pulse.HIGH
            and receiver == 'dd'
        )
    return wrapper


def push_button_until(modules: dict[str, Module], check_condition: Callable) -> int:
    """(Part 2)
    Continually push button until `check_condition` is observed True twice
    and return their time interval.
    """
    history = []
    counter = count()
    while len(history) < 2:
        t = next(counter)
        for pulse in push_button(modules):
            if check_condition(*pulse):
                history.append(t)
    return max(history) - min(history)


def solve_part1(puzzle_input) -> int:
    modules = parse_configuration(puzzle_input)
    counts = Counter(
        pulse 
        for _ in range(1_000) 
        for _, pulse, _ in push_button(modules)
    )
    return counts[Pulse.LOW] * counts[Pulse.HIGH]


def solve_part2(puzzle_input) -> int:
    modules = parse_configuration(puzzle_input)
    assert sorted(modules['dd'].state.keys()) == sorted(['nx', 'sp', 'cc', 'jq'])
    nx_interval = push_button_until(modules, send_high_pulse_to_dd('nx'))
    sp_interval = push_button_until(modules, send_high_pulse_to_dd('sp'))
    cc_interval = push_button_until(modules, send_high_pulse_to_dd('cc'))
    jq_interval = push_button_until(modules, send_high_pulse_to_dd('jq'))
    return lcm(nx_interval, sp_interval, cc_interval, jq_interval)
    

if __name__ == '__main__':

    title = 'Day 20: Pulse propagation'
    print(title.center(50, '-'))

    assert Pulse.HIGH ^ 1 == Pulse.LOW
    assert Pulse.LOW ^ 1 == Pulse.HIGH

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = None
        if txtfile == 'input.txt':
            part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The product of total low pulses and total high pulses is {part1}.
        Part 2: The number of button pushes it takes to send a low pulse to 'rx' is {part2}.
        """)
