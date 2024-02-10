from pathlib import Path
from operator import itemgetter
import sys

total_lines = 0
line_counts = []
num_folders = 0
num_other_files = 0

glob_pattern = '**/*.py'
if len(sys.argv) > 1:
    glob_pattern = sys.argv[1]

file_type = '.' + glob_pattern.split('.')[1]

comment_symbol = '#'
if glob_pattern.endswith('.cs'):
    comment_symbol = '//'

for path in Path.cwd().glob(glob_pattern.split('.')[0]):
    if not path.is_file():
        num_folders += 1
        continue

    if not path.suffix == file_type:
        num_other_files += 1
        continue

    relative_path = path.relative_to(Path.cwd())
    if 'build' in str(relative_path):
        continue

    with path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
        total_lines += len(lines)
        source_lines_of_code = [l for l in lines if l!='\n' and not l.lstrip().startswith(comment_symbol)]

        line_counts.append((len(lines), str(relative_path), len(source_lines_of_code)))

line_counts = sorted(line_counts)
longest_name = max([len(e[1]) for e in line_counts])

print('lines of code in project:')
print(f" name{' '*longest_name}loc      sloc")

for e in line_counts:
    n, name, source_lines_of_code = e
    print(f"  {name} {' '*(longest_name-len(name)+2)} {n:>4}     {source_lines_of_code:>4}")

print('\n  number of folders:', num_folders)
print('  number of other files:', num_other_files)
print('\n  number of files:', len(line_counts))
print('  total_lines:', total_lines, '     ', sum(e[2] for e in line_counts), '\n')
