"""
-- Day 21: Monkey Math --
"""
import re

with open('day21_input.txt', 'r') as f:
    exprs: list[str] = [
        line.strip().replace(': ', ' = ').replace('/', '//')
        for line in f
    ]
locals: dict = {}

while 'root' not in locals:
    for expr in exprs:
        try:
            exec(expr, None, locals)
        except NameError:
            pass
print(locals['root'])