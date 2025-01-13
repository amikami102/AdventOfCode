# year2024/day17/main.py
import sys
from pathlib import Path
from typing import Type, Literal, Iterator, Sequence
import re
from dataclasses import dataclass, field

COMMA = ','
Bit7 = Type[Literal[0|1|2|3|4|5|6|7]]


def get_integers(string: str) -> tuple[int, ...]:
    return tuple(
        int(num) for num in re.findall(r'-?\d+', string)
    )


def parse(txtfile):
    return Path(txtfile).read_text().split('\n\n')


@dataclass 
class Computer:
    registers: tuple[int]
    program: tuple[int, ...]
    A: int = field(default=None, init=False)
    B: int = field(default=None, init=False)
    C: int = field(default=None, init=False)
    pointer: int = 0
    
    def __post_init__(self):
        self.A, self.B, self.C = self.registers 

    def literal(self, operand: Bit7) -> int:
        return operand 
    
    def combo(self, operand: Bit7) -> int:
        match operand:
            case 0|1|2|3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise ValueError('Combo operand 7 is invalid')
    
    def adv(self, operand: Bit7) -> None:
        self.A = self.A  // pow(2, self.combo(operand))
    
    def bxl(self, operand: Bit7) -> None:
        self.B = self.B ^ self.literal(operand)
    
    def bst(self, operand: Bit7) -> None:
        self.B = self.combo(operand) % 8
    
    def jnz(self, operand: Bit7) -> None:
        if self.A:
            self.pointer = self.literal(operand) 

    def bxc(self, operand: Bit7) -> None:
        self.B = self.B ^ self.C

    def out(self, operand: Bit7) -> int:
        return self.combo(operand) % 8

    def bdv(self, operand: Bit7) -> None:
        self.B = self.A  // pow(2, self.combo(operand))

    def cdv(self, operand: Bit7) -> None:
        self.C = self.A // pow(2, self.combo(operand))

    def cleanup(self):
        self.A, self.B, self.C = self.registers
        self.pointer = 0

    def run_program(self) -> Iterator[int]:
        while self.pointer < len(self.program) - 1:
            opcode, operand = self.program[self.pointer: self.pointer + 2]
            self.pointer += 2
            match opcode:
                case 0: self.adv(operand)
                case 1: self.bxl(operand)
                case 2: self.bst(operand)
                case 3: self.jnz(operand)
                case 4: self.bxc(operand)
                case 5: yield self.out(operand)
                case 6: self.bdv(operand)
                case 7: self.cdv(operand)
    
    def collect_output(self) -> Sequence[int]:
        return tuple(self.run_program())


def solve_part1(data) -> str:
    registers_str, program_str = data
    computer = Computer(
        get_integers(registers_str), 
        get_integers(program_str)
    )
    return COMMA.join(map(str, computer.collect_output()))

def solve_part2(data):
    pass


if __name__ == '__main__':
    title = 'Day 17: Chronospatial Computer'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The comma-joined output string is {part1}.
        Part 2: The  is {part2}.
        """)