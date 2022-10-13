#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


# import hp35data as hpdata

def show_calc(display):
    spaced_chars = ' '.join(display)
    x_sup_y = "Xʸ"
    e_sup_x = "eˣ"
    root_x = "√x"
    print("┌--------------------------------------┐")
    print("|    ", spaced_chars, "       |", sep="")
    print("|______________________________________|")
    print("|                                      |")
    print("|   OFF ═ON                            |")
    print("|                                      |")
    print("|   ", x_sup_y, "     log     ln     ", e_sup_x, "    CLR    |", sep="")
    print("|                                      |")
    print("|   ", root_x, "     arc    sin    cos    tan    |", sep="")
    print("|                                      |")
    print("|   1/x    x⇆y    R↓     STO    RCL    |")
    print("|                                      |")
    print("|   ENTER↑       CHS    E EX   CL x    |")
    print("|                                      |")
    print("|     -      7        8        9       |")
    print("|                                      |")
    print("|     +      4        5        6       |")
    print("|                                      |")
    print("|     X      1        2        3       |")
    print("|                                      |")
    print("|     ÷      0        ·        𝛑       |")
    print("|                                      |")
    print("|______________________________________|")
    print("|  h/p  H E W L E T T - P A C K A R D  |")
    print("└--------------------------------------┘")


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


def display_key_menu():
    pass


def get_key():
    pass


def main():
    python_check()
    try:
        chars = "-1.23456789-35"
        show_calc(chars)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
