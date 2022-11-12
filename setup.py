from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='hp35',
    version='1.1.0',
    description='A program to emulate the classic HP-35 scientific calculator.',
    long_description=readme,
    author='Paul Dunphy',
    include_package_data=True,
    packages=find_packages(),
    url='https://github.com/ve1dx/hp-35',
    entry_points={
        'console_scripts': ['hp-35=hp-35.hp-35:main'],
    },
)
