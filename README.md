# hp-35

An emulation of the classic Hewlett-Packard Model 35 RPN calculator introduced in 1972.

Requires Python version 3.5 or higher and has been tested on Debian 11 (64-bit), Ubuntu 22.04.1 and MAC OS X (macOS Ventura 13.0.1). This program should run on Windows equipped with Python 3.5 or later.

To install, download hp-35-main.zip, and extract and install it:

unzip hp-35-main.zip

cd hp-35-main

pip install -e .

The hp-35 command should then work from anywhere.

To remove:

pip uninstall hp-35

Use hp-35 --help for more info.  Also refer to the documentation file 'hp-35_emulator.pdf'


Python libraries required (install with 'pip install <library_name>'):

numpy
getkey
termcolor
