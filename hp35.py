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
            sys.exit('HP-35 powering off')
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
