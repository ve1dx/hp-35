# hp-35

An emulation of the classic Hewlett-Packard Model 35 RPN calculator introduced in 1972.

Requires Python version 3.5 or higher and has been tested on Debian 11 (64-bit), Ubuntu 22.04.1 and MAC OS X (macOS Ventura 13.0.1). This program should run on Windows equipped with Python 3.5 or later.

To install, download hp-35-main.zip, and extract and install it:

1) unzip hp-35-main.zip

2) optionally create new virtual environment & activate it

3) pip install -r requirements.txt
   (this will install numpy, getkey and termcolor)

4) pip install -e .

The hp35 command should then work from anywhere.

To remove:

pip uninstall hp35

Use hp35 --help for more info.  Also refer to the documentation file 'hp-35_emulator.pdf'


Python libraries required:

numpy
getkey
termcolor
