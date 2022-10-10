#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import hp35data as hpdata


def show_display():
    print(hpdata.display)
    minus = '-'
    print(minus, " ", hpdata.numeric_display)


def python_check():
    version_major = sys.version_info[0]
    version_minor = sys.version_info[1]
    version_micro = sys.version_info[2]
    if not (version_major == 3 and version_minor >= 5):
        print("Python verson 3.5 or higher required to run wee_trend. This system is running Python version ",
              version_major, ".", version_minor, ".", version_micro, sep="")
        print()
        print("Exiting program.")
        sys.exit(0)


def main():
    try:
        python_check()
        show_display()
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
