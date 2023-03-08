from pathlib import Path
from operator import itemgetter


total_lines = 0
line_counts = []

for path in Path.cwd().glob('**/*.py'):
    if not path.is_file():
        continue

    relative_path = path.relative_to(Path.cwd())
    if 'build' in str(relative_path):
        continue

    with path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
        total_lines += len(lines)
        source_lines_of_code = [l for l in lines if l!='\n' and not l.lstrip().startswith('#')]

        line_counts.append((len(lines), str(relative_path), len(source_lines_of_code)))

line_counts = sorted(line_counts)
longest_name = max([len(e[1]) for e in line_counts])

print('lines of code in project:')
print(f" name{' '*longest_name}loc      sloc")

for e in line_counts:
    n, name, source_lines_of_code = e
    print(f"  {name} {' '*(longest_name-len(name)+2)} {n:>4}     {source_lines_of_code:>4}")

print('\n  number of files:', len(line_counts))
print('  total_lines:', total_lines, '     ', sum(e[2] for e in line_counts), '\n')
