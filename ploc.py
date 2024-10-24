from pathlib import Path
import sys

total_lines = 0
line_counts = []
folders = []
other_files = []

if '--help' in sys.argv:
    print('''usage: python -m ploc 
    **/*.py                                 (glob pattern)
    --comment="#"                           (don't count lines starting with this)
    --ignore="(\'folder_1\',\'folder_2\')"  (optional) 
    --list_all=True'                        (optional)
    ''')
    exit()


glob_pattern = '**/*.py'
if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
    glob_pattern = sys.argv[1]

print(glob_pattern)
if '.' not in glob_pattern:
    raise Exception(f'glob pattern: {glob_pattern} must contain a "." in order to know the file type')
file_type = '.' + glob_pattern.split('.')[1]


def get_arg(name, fallback=None):
    name = f'--{name}='
    for arg in sys.argv:
        if arg.startswith(name):
            return arg[len(name):]
    return fallback

comment_symbol = '#'
if glob_pattern.endswith('.cs'):
    comment_symbol = '//'

comment_symbol = get_arg('comment', fallback=comment_symbol)

ignore = get_arg('ignore', None)
if ignore is not None:
    ignore = eval(ignore)

print(f'counting lines... glob_pattern: {glob_pattern}, file_type: {file_type}, comment: {comment_symbol}, ignore: {ignore}')


paths = Path.cwd().glob(glob_pattern.split('.')[0])
paths = [f for f in paths if not any([p for p in f.resolve().parts if p.startswith('.')])]  # ignore folders and files starting with . (hidden)
paths = [f for f in paths if not any([p for p in f.resolve().parts if p.startswith('__')])] # ignore folders and files starting with __ (cache)
if ignore is not None:
    paths = [f for f in paths if not any([p for p in f.resolve().parts if p in ignore])]        # ignore custom names that was passed in 

for path in paths:
    if not path.is_file():
        folders.append(path)
        continue

    if not path.suffix == file_type:
        other_files.append(path)
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

for i, e in enumerate(line_counts):
    n, name, source_lines_of_code = e
    print(f"{i}  {name} {' '*(longest_name-len(name)+2)} {n:>4}     {source_lines_of_code:>4}")

print('\n  number of folders:', len(folders))
print('  number of other files:', len(other_files))
print(f'\n  number of files matching {glob_pattern}: {len(line_counts)}')
print('  total_lines:', total_lines, '     ', 'without comments:', sum(e[2] for e in line_counts), '\n')

if get_arg('list_all') == 'True':
    for f in folders:
        print('folder:', f)
        
    for f in other_files:
        print('other file:', f)

