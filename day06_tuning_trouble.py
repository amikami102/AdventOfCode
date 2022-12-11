"""
The device will send your subroutine a datastream buffer (your puzzle input);
your subroutine needs to identify the first position
where the four most recently received characters were all different.
Specifically, it needs to report the number of characters
from the beginning of the buffer
to the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb

After the first three characters (mjq) have been received,
there haven't been enough characters received yet to find the marker.
The first time a marker could occur is after the fourth character is received,
making the most recent four characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives.
Once it does, the last four characters received are jpqm, which are all different.
In this case, your subroutine should report the value 7
because the first start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

How many characters need to be processed before the first start-of-packet marker is detected?
"""
import itertools
import collections

with open('day06_input.txt', 'r') as f:
    line = f.readline()
n_char = 4
signal = iter(line)
window = collections.deque(itertools.islice(signal, n_char), maxlen=n_char)
counter = n_char
if len(set(window)) == n_char:
    print(counter)
for s in signal:
    counter += 1
    window.append(s)
    if len(set(window)) == n_char:
        break

print(f"The first marker appears after character {counter}.")

"""
Your device's communication system is correctly detecting packets, 
ut still isn't working. It looks like it also needs to look for messages.

A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
How many characters need to be processed before the first start-of-message marker is detected?
"""

n_char = 14
signal = iter(line)
window = collections.deque(itertools.islice(signal, n_char), maxlen=n_char)
counter = n_char
if len(set(window)) == n_char:
    print(counter)
for s in signal:
    counter += 1
    window.append(s)
    if len(set(window)) == n_char:
        break

print(f"The first start-of-message marker is detected after character {counter}.")