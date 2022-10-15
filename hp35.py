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
    # When the calculator off, the display should be blank.
    #
    if off:
        led_display = '               '
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
    print('off   on')
    print('xy', '   log', '   ln', '  ex', '  clr')
    print('rx', '   arc', '   sin', ' cos', ' tan')
    print('1x', '   rv', '    dn', '  sto', ' rcl')
    print('e(nter)', '     chs', ' eex', ' clx')
    print('-', '      7', '      8', '     9')
    print('+', '      4', '      5', '     6')
    print('x', '      1', '      2', '     3')
    print('/', '      0', '      .', '    pi')
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
        if choice == 'pi':
            choice = '3.141592654    '
            a_number = True
            break
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


def process_action_keys(key):
    action = key
    if action == 'clr':
        # Will need to clear stack, etc.
        chars = "0.             "
        return chars, True
    elif action == 'on':
        print("HP-35 is already on")
        return action, False
    pass


def main():
    python_check()
    # Define initial stack
    try:
        chars = "0.             "
        existing_display = chars
        show_calc(chars, False)
        key = ''
        while True:
            display_key_menu()
            key, a_number = get_key(key)
            if not a_number:
                new_display, need_update = process_action_keys(key)
                if need_update:
                    show_calc(new_display, False)
                else:
                    show_calc(existing_display, False)
            else:
                numeric_chars = f"{key:<15}"
                show_calc(numeric_chars, False)
                existing_display = numeric_chars
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
