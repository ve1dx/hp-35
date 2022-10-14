#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import hp35data as hpdata


def show_calc(display, off):
    led_display = str(display)
    #
    # There are only 15 7-segment led characters
    #
    led_display = led_display[:15]
    #
    # When the calculator off, technically the
    # display should be blank.  However, HP's original promotion
    # shows the digits -1.234567809-35, so we display that even
    # with the display off.
    #
    if off:
        led_display = '-1.234567809-35'
    #
    # Double space characters to make them
    # look more like the original LED display
    #
    spaced_chars = ' '.join(led_display)
    print("┌--------------------------------------┐")
    print("|   ", spaced_chars, "      |", sep="")
    print("|______________________________________|")
    print("|                                      |")
    #
    if off:
        print("|   OFF═ ON                            |")
    else:
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
        print("Python verson 3.5 or higher required to run hp35. This system is running Python version ",
              version_major, ".", version_minor, ".", version_micro, sep="")
        print()
        print("Exiting program.")
        sys.exit(0)


def display_key_menu():
    print()
    print("1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '.', xy for Xʸ log")
    print("ln, ex for eˣ, clr, rx for √x, arc, sin, cos, tan")
    print("e for ENTER↑, CHS, eex, clx")
    print()
    print("'off' to to turn calculator off")
    print()


def is_number(n):
    try:
        float(n)  # Type-casting the string to `float`.
        # If string is not a valid `float`,
        # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


def get_key(choice):
    legal_key = False
    a_number = False
    while not legal_key:
        choice = input('> ')
        choice = str(choice)
        if choice == 'off':
            chars = ''
            show_calc(chars, True)
            sys.exit(0)
        test = choice
        a_number = is_number(test)
        if a_number:
            if '.' in choice and choice[-1] != '.':
                pass
            else:
                choice = choice + '.'
        legal_key = choice in hpdata.key_list or a_number
        if not legal_key:
            print("Invalid entry")
            print()
    return choice, a_number


def main():
    python_check()
    try:
        chars = "0.             "
        show_calc(chars, False)
        key = ''
        while True:
            display_key_menu()
            key, a_number = get_key(key)
            chars = f"{key:<15}"
            show_calc(chars, False)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
