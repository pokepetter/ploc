from setuptools import setup

# with open("README.md", encoding="UTF-8") as f:
#     long_desc = f.read()

setup(
    name='ploc',
    description='Get a overview of files in folder and number of lines',
    # long_description=long_desc,
    # long_description_content_type="text/markdown",
    version='0',
    py_modules=['ploc'],
    entry_points='''
        [console_scripts]
        ploc=ploc:ploc
    ''',
    # url='https://github.com/pokepetter/ursina',
    author='Petter Amland',
    author_email='pokepetter@gmail.com',
    python_requires='>=3.8',
)
