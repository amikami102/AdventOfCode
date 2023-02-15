"""
-- Day 25: Full of Hot Air --

(Inspired by Peter Norvig's solution)

Decimal          SNAFU
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       11             21
       12             22
       13            1==
       14            1=-
       15            1=0
       16            1=1
       20            1-0
       21            1-1
       22            1-2
       23            10-       4, 3 => 5, -2
       24
       25            100
       26            101
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
"""

SNAFU = str
map_snafu: dict[str, int] = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
map_decimal: dict[int, str] = {v: k for k, v in map_snafu.items()}


def convert_snafu_to_decimal(snafu_str: SNAFU) -> int:
    """
    Convert a SNAFU string into a base 10 integer.
    """
    return sum(
        5 ** i * map_snafu[char]
        for i, char in enumerate(reversed(snafu_str))
    )


def convert_decimal_to_snafu(decimal: int) -> SNAFU:
    """
    Convert decimal integers to SNAFU recursively.
    Let x be a base 10 integer.
    1) x / 5 = q remainder r
    2) if r < 3: keep q and r
        else: increment q by 1 and convert r to r-5 (so r=3 becomes r=-2, r=4 becomes r=-1)
    3) convert q into SNAFU recursively except for when r = 0, in which case return ''
    4) since r is either 0, 1, 2, -1, or -2, attach r pulled from map_decimal to the right of result of step 3
    """
    q, r = divmod(decimal, 5)
    if 3 <= r <= 4:
        q, r = q + 1, r - 5
    return ''.join(
        (
            convert_decimal_to_snafu(q) if q else '',
            map_decimal[r]
        )
    )


with open('day25_input.txt', 'r') as f:
    decimals = [
        convert_snafu_to_decimal(line.strip())
        for line in f
    ]
part1 = convert_decimal_to_snafu(sum(decimals))
print(f'The SNAFU code to supply to Bob is "{part1}".')