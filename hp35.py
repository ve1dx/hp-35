#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


# import hp35data as hpdata

def show_calc(display):
    spaced_chars = ' '.join(display)
    print("┌--------------------------------------┐")
    print("|    ", spaced_chars, "       |", sep="")
    print("|______________________________________|")
    print("|                                      |")
    print("|   OFF ═ON                            |")
    print("|                                      |")
    print("|   Xʸ     log    ln      eˣ    CLR    |")
    print("|                                      |")
    print("|   √x     arc    sin    cos    tan    |")
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
    print("1, 2, 3, 4, 5, 6, 7, 8, 9, 0 or '.'")
    print("xy for Xʸ, log, ln, ex for eˣ, clr, rx for √x, arc, sin, cos, tan")
    print("e for ENTER↑, CHS, eex, clx or off to to turn calculator off")


def get_key(choice):
    l1 = ['xy', 'log', 'ln', 'ex', 'clr', 'rx', 'arc', 'sin', 'cos', 'tan',
          'e', 'chs', 'eex', 'clx', 'off']
    legal_key = False
    while not legal_key:
        choice = input('> ')
        a_number = choice.isnumeric()
        decimal_point = choice.find(".") != -1
        if a_number or decimal_point:
            number = True
        else:
            number = False
        legal_key = choice in l1 or number
        print('choice, legal_key, a_number, decimal_point, number =', choice, legal_key, a_number,
              decimal_point, number)
    return str(choice), number


def main():
    python_check()
    try:
        chars = "0.            "
        show_calc(chars)
        key = ''
        while True:
            display_key_menu()
            key, a_number = get_key(key)
            if key == 'off':
                chars = "-1.23456789-35"
                show_calc(chars)
                return
            if key == a_number:
                if key.find(".") == -1:
                    key = key + '.'
            chars = f"{key:<14}"
            print(chars)
            show_calc(chars)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
