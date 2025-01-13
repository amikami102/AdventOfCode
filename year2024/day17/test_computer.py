# year2024/day17/test_computer.py
from main import *

import pytest 


@pytest.mark.parametrize(
    'registers, program, expected', [
    ((0, 0, 9), (2,6), 'computer.B == 1'),
    ((10, 0, 0), (5,0,5,1,5,4), "output == (0,1,2)"),
    (
        (2024, None, None), 
        (0,1,5,4,3,0), 
        'output == (4,2,5,6,7,7,7,7,3,1,0) and computer.A == 0'
    ),
    ((0, 29, 0), (1,7), 'computer.B == 26'),
    ((0, 2024, 43690), (4,0), 'computer.B == 44354')
])
def test_run_program(registers, program, expected):
    computer = Computer(registers, program)
    output = computer.collect_output()
    assert eval(expected)