#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import hp35data as hpdata


def convert_to_scientific_notation(float_number):
    # Work on a copy because Python passes by reference
    number = float_number
    #
    # The HP-35 uses scientific notation if the number is not between
    # 0.01 (10⁻² and 1000000000 which is 10 billion or 10¹⁰.)  It has 9
    # digits of precision.
    # There some 'oddities' given the 1972 technology and design. The display
    # is limited to 15 LED characters and the first one is blank or a - sign
    # depending on the sign of the number. It also doesn't display an E or e,
    # but rather a space or a minus sign in LED location 13, indicating a
    # big or small number. It's overall display range is between
    #  9.999999999 99 and -9.999999999 99 (each is 15 digits.)  If the
    # exponential notation number has 'trailing 0s' we have to remove them:
    # e.g. 1.004500000 25 becomes 1.0045      25, and  1.000000000 55 becomes
    #  1.          55.                                123456789112345
    #  123456789112345
    # We have to take a Python float and convert it to a display string to
    # fit the above rules.
    #
    if number == 0.0:
        str_number = str(number)
        positive = True
        return str_number, positive
    positive = number >= 0.0
    number = abs(number)
    lo = 0.01
    hi = 1000000000.0
    # If it's in the scientific notation range, apply the rules above, otherwise
    # just return it "as is"
    in_range = min(lo, hi) < number < max(lo, hi)
    if not in_range:
        s_number = str(np.format_float_scientific(number, exp_digits=2, unique=False, precision=9))
        # Convert string to a list, so we can get at the characters
        sl = list(s_number)
        if positive:
            sl.insert(0, ' ')
        else:
            sl.insert(0, '-')
        # Remove the e and replace the + with a space if number is big or
        # with a - sign if the number is small.
        sl[12] = ''
        if max(lo, hi) < number:
            sl[13] = ' '
        else:
            sl[13] = '-'
        # Now deal with trailing zeros in the mantissa
        loc = 11
        while sl[loc] == '0':
            sl[loc] = ' '
            loc -= 1
        # Convert back into a string
        s_number = "".join(sl)
    else:
        s_number = str(number)
    return s_number, positive


def show_calc(display, off):
    if not off:
        number = float(display)
        led_display, positive = convert_to_scientific_notation(number)
        if not positive:
            led_display = '-' + led_display
        led_display = led_display.ljust(15, ' ')
    #
    # When the calculator off, the display should be blank.
    #
    else:
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
    print('off  on')
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
        if choice == 'on':
            print("Calculator is already on.")
            print()
            legal_key = False
    return choice, a_number


def push_stack(stack):
    new_stack = stack
    new_stack["T"] = new_stack["Z"]
    new_stack["Z"] = new_stack["Y"]
    new_stack["Y"] = new_stack["X"]
    return new_stack


def clear_stack(stack):
    new_stack = stack
    new_stack["T"] = float(0.0)
    new_stack["Z"] = float(0.0)
    new_stack["Y"] = float(0.0)
    new_stack["X"] = float(0.0)
    return new_stack


def mem_func(mem, stack, action):
    if action == 'sto':
        mem = stack["X"]
        return mem, stack
    elif action == 'rcl':
        stack["X"] = mem
        return mem, stack
    elif action == 'clr':
        mem = float(0.0)
        return mem, stack


def process_action_keys(key, stack, mem):
    action = key
    current_stack = stack
    if action == 'clr':
        chars = "0.             "
        stack = clear_stack(stack)
        mem, stack = mem_func(mem, stack, action)
        return chars, stack, mem, True
    elif action == 'e':
        stack = push_stack(current_stack)
        return action, stack, mem, True
    elif action == 'sto':
        mem, stack = mem_func(mem, stack, action)
        return action, stack, mem, True
    elif action == 'rcl':
        mem, stack = mem_func(mem, stack, action)
        return action, stack, mem, True
    elif action == 'clx':
        stack["X"] = float(0.0)
        return action, stack, mem, True
    pass


def main():
    python_check()
    # Define operational stack
    stack = {"T": 0.0,
             "Z": 0.0,
             "Y": 0.0,
             "X": 0.0}
    stack = clear_stack(stack)
    mem = float(0.0)
    try:
        chars = "0.             "
        existing_display = chars
        show_calc(chars, False)
        key = ''
        while True:
            display_key_menu()
            key, a_number = get_key(key)
            if not a_number:
                new_display, stack, mem, need_update = process_action_keys(key, stack, mem)
                if need_update:
                    show_calc(new_display, False)
                else:
                    show_calc(existing_display, False)
            else:
                stack["X"] = float(key)
                print(stack.values())
                numeric_chars = f"{key:<15}"
                show_calc(numeric_chars, False)
                existing_display = numeric_chars
            print('stack =', stack.values())
            print('mem =', mem)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
