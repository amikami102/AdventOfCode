"""
Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
    cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
    cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
    cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all files and directories immediately contained by the current directory:
    123 abc means that the current directory contains a file named abc with size 123.
    dir xyz means that the current directory contains a directory named xyz.

Find all directories with a total size of at most 100000.
What is the sum of the total sizes of those directories?
"""
from collections import defaultdict
import pprint
import re

cd_pattern = re.compile('^\$ cd (?P<dir>\S+)$')
ls_pattern = re.compile('^\$ ls$')
file_pattern = re.compile('^(?P<filesize>\d+) (?P<filename>\S+)$')
dir_pattern = re.compile('^dir (?P<dir>\w+)$')
max_size = 100000

directory_sizes = defaultdict(int)
path = []

# Build a dictionary of directory paths
with open('day07_input.txt', 'r') as f:
    for line in f:
        if line.startswith('$ cd'):
            dir = re.match(cd_pattern, line).group('dir')
            if dir == '/':
                path = ['/']
            elif dir == '..':
                path.pop()
            else:
                path.append(dir)
        elif line.startswith('$ ls'):
            continue
        else:
            if line.startswith('dir'):
                continue
            else:
                file = re.match(file_pattern, line)
                filesize = int(file.group('filesize'))

                for i in range(len(path)):
                    dirpath = '/'.join(path[:i+1])
                    directory_sizes.setdefault(dirpath, 0)
                    directory_sizes[dirpath] += filesize

total = sum(v for v in directory_sizes.values() if v <= max_size)
print(f'The sum of directory sizes less than {max_size:,} is {total:,}.')

"""
The total disk space available to the filesystem is 70000000. 
To run the update, you need unused space of at least 30000000. 
You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; 
this means that the size of the unused space must currently be 21618835, 
which isn't quite the 30000000 required by the update. 
Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. 
However, directories d and / are both big enough! 
Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. 
What is the total size of that directory?
"""
print(directory_sizes)

available, required_unused = 70000000, 30000000
current_unused = available - (directory_sizes['/'])
print(current_unused)

min_dir = directory_sizes['/']
for d, v in directory_sizes.items():
    if current_unused + v > required_unused and v < min_dir:
        min_dir = v

print(min_dir)
print(current_unused + min_dir > required_unused)