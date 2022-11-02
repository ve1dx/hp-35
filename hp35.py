#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import RawTextHelpFormatter
import sys
import numpy as np
import math
import textwrap
import time
from getkey import getkey, keys
import hp35data as hpdata
from termcolor import cprint


def hp35_scientific_notation(float_number):
    # Work on a copy because Python passes by reference
    number = float_number
    # Assume we'll convert to scientific notation
    sci_note = True
    #
    # This is a complex function because the goal is to emulate the
    # behaviour of the HP-35, not to provide 100% floating point precision 21st
    # century Python math. The HP-35 was, and still is, 'good enough' for almost
    # any scientific or engineering project.
    #
    # The HP-35 uses scientific notation if the number is not between
    # 0.01 (10⁻² and 10,000,000,000 which is 10 billion or 10¹⁰.)  It has 9
    # digits of precision.
    #
    # There some 'oddities' given the 1972 technology and HP-35 design. The display
    # is limited to 15 LED characters and the first one is blank or a - sign
    # depending on the sign of the number. It also doesn't display an E or e,
    # but rather a space or a minus sign in LED location 13, indicating a
    # big or small number. It's overall display range is between
    # ' 9.999999999 99' and '-9.999999999 99' (each is 15 digits.)
    #
    # If the exponential notation number has 'trailing 0s' we have to remove them:
    # e.g. 1.004500000 25 becomes ' 1.0045      25', and ' 1.000000000 55' becomes
    # ' 1.          55'
    # Also, things like 4.562389e+16 need to be converted to ' 1.0045       25'
    #
    # Since the range of the calculator is between -9.99999999e+99 and 9.999999999e+99
    # and if we exceed that, the display becomes the appropriate 'edge' number in HP-35
    # limit of '-9.999999999 99' or ' 9.999999999 99'
    #
    # Finally, if there is no scientific notation required, the HP-35 doesn't display
    # trailing zeros on any numbers.
    #
    # This function takes a Python float and converts it to a display string observing
    # the above rules.
    #
    if number == 0.0:
        str_number = str(round(number, 9))
        positive = True
        sci_note = False
        return str_number, positive, sci_note
    positive = number >= 0.0
    over_flow = number > 9.99999999e+99
    if over_flow:
        str_number = ' 9.999999999 99'
        return str_number, True, True
    under_flow = number < -9.99999999e+99
    if under_flow:
        str_number = '-9.999999999 99'
        return str_number, False, True
    number = abs(number)
    lo = 0.01
    hi = 1000000000.0
    # If it's in the scientific notation range, apply the rules above, otherwise
    # just return it "as is"
    in_range = min(lo, hi) < number < max(lo, hi)
    if not in_range:
        # Break the number into a mantissa and exponent and make it a string
        s_number = str(np.format_float_scientific(number, exp_digits=2, unique=False, precision=9))

        # Convert string to a list, so we can get at the characters because of Python's immutable strings
        # Convert to a list (which would be indexed 0-14)
        sl = list(s_number)
        # Add the sign character at the beginning. This will make the list 15 digits after inserting
        # a ' ' or a '-' thus it will now be indexed 0-15
        if positive:
            sl.insert(0, ' ')
        else:
            sl.insert(0, '-')
        # Remove the e+EX or e-EX and replace the + or with a space if number is big or
        # with a - sign if the number is small. Put the EX 'digits' in the last two places
        for i in range(0, 13):
            if sl[i] == 'e':
                sign_loc = i + 1
                exp1_loc = i + 2
                exp2_loc = i + 3
                sl[i] = ''
                sl[sign_loc] = ' '
                sl[14] = sl[exp1_loc]
                sl[15] = sl[exp2_loc]
        # Remove the e and replace the + with a space if number is big or
        # with a - sign if the number is small.
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
        sci_note = False
        s_number = str(number)
    return s_number, positive, sci_note


def show_calc(display, disp_col, valid_number, off):
    #
    # Lot of fooling around here to get things to fit in the
    # display properly as per the 1972 HP-35 'standard'
    #
    if valid_number:
        number = float(display)
        led_display, positive, sci_note = hp35_scientific_notation(number)
        if not positive and not sci_note:
            led_display = '-' + led_display
        if not sci_note:
            led_display = led_display.rstrip("0")
            led_display = textwrap.shorten(led_display, width=15, placeholder='')
        led_display = led_display.ljust(15, ' ')
    #
    # When the calculator off, the display should be blank.
    #
    elif off:
        led_display = '               '
    #
    # Flash 0.0 on √ of negative number and other
    # illegal math operations.
    #
    elif display == 'wink':
        led_display = '0.0            '
    else:
        led_display = display.ljust(15, ' ')
    #
    # Double space characters to make them
    # look more like the original LED display
    #
    spaced_chars = ' '.join(led_display)
    print("┌--------------------------------------┐")
    if display != 'wink':
        vertical_1 = '|     '
        vertical_2 = '    |'
        print(vertical_1, end='')
        cprint(spaced_chars, disp_col, attrs=['bold'], end='')
        print(vertical_2)
    else:
        vertical = '|'
        text = '    0.                                '
        print(vertical, end='')
        cprint(text, disp_col, attrs=['blink', 'bold'], end='')
        print(vertical)
    print("|______________________________________|")
    print("|                                      |")
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
    print('xy', '    log', '    ln', '  ex', '  clr')
    print('rx', ' a<s,c,t>', '  sin', ' cos', ' tan')
    print('1x', '     rv', '    rd', '  sto', ' rcl')
    print('e(nter)', '       chs', ' eex', ' clx')
    print('-', '       7', '      8', '      9')
    print('+', '       4', '      5', '      6')
    print('x', '       1', '      2', '      3')
    print('/', '       0', '      .', '     pi')
    print()


def is_number(n):
    try:
        float(n)  # Type-casting the string to `float`.
        # If string is not a valid `float`,
        # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


def get_cmd(choice):
    legal_key = False
    a_number = False
    while not legal_key:
        choice = input('> ')
        choice = str(choice)
        if choice == 'pi':
            choice = '3.141592654    '
            a_number = True
            break
        a_number = is_number(choice)
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


def reverse_xy(stack):
    temp = stack["Y"]
    stack["Y"] = stack["X"]
    stack["X"] = temp
    return stack


def push_stack(stack):
    stack["T"] = stack["Z"]
    stack["Z"] = stack["Y"]
    stack["Y"] = stack["X"]
    return stack


def rotate_stack(stack):
    temp = stack["X"]
    stack["X"] = stack["Y"]
    stack["Y"] = stack["Z"]
    stack["Z"] = stack["T"]
    stack["T"] = temp
    return stack


def clear_stack(stack):
    stack["T"] = float(0.0)
    stack["Z"] = float(0.0)
    stack["Y"] = float(0.0)
    stack["X"] = float(0.0)
    return stack


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


def dump_zeros(stack):
    chars = str(stack["X"])
    chars = chars.rstrip("0")
    return chars


def get_exponent(stack, mem, disp_col):
    #
    # Some complex programming here because of the 1972 technical limitations of the HP-35 and
    # Python's immutable strings.
    #
    # First get the X register and make it scientific notation if it's not between 10⁻² and 10¹⁰
    # Precision of the HP-35 is 9 digits. Python's float might have 'noise' beyond that, so
    # round off to 9
    #
    temp = round(float(stack["X"]), 9)
    if temp == 0.0:
        temp = 1.0
    led_display, positive, sci_note = hp35_scientific_notation(temp)
    if not positive:
        led_display = '-' + led_display
    # If it's not scientific notation remove the trailing zeros and
    # pad it out to 15 'LED' display characters
    if not sci_note:
        led_display = led_display.rstrip("0")
        led_display = led_display.ljust(15, ' ')
        # Stick 00s in last two locations in preparation for the entering of the exponent. Temporarily
        # make it a list to do this.
    lst = list(led_display)
    lst[13] = '0'
    lst[14] = '0'
    led_display = ''.join(lst)
    while True:
        #
        # Don't display the entire calculator during the 'E EX' function
        spaced_chars = ' '.join(led_display)
        print("┌--------------------------------------┐")
        vertical_1 = '|     '
        vertical_2 = '    |'
        print(vertical_1, end='')
        cprint(spaced_chars, disp_col, attrs=['bold'], sep="", end='')
        print(vertical_2)
        print("|______________________________________|")
        print()
        print('> ')
        key = getkey()
        if key == keys.NEW_LINE:
            break
        if key != keys.MINUS:
            lst[13] = lst[14]
            lst[14] = key
        #
        # Use '-' in this situation only to change the sign of the exponent
        #
        else:
            tmp = str(lst[12])
            if tmp == ' ':
                lst[12] = '-'
            elif tmp == '-':
                lst[12] = ' '
        led_display = ''.join(lst)
    #
    # Before updating the display string, convert the mantissa and exponent to a
    # Python float and put it in the X register.
    #
    exponent = float(str(lst[12]) + str(lst[13]) + str(lst[14]))
    mult = 10.0 ** exponent
    mantissa = ''
    for i in range(0, 10):
        mantissa = mantissa + str(lst[i])
    mantissa = float(mantissa)
    result = float(mantissa * mult)
    stack["X"] = result
    action_chars = dump_zeros(stack)
    return action_chars, stack, mem


def add(stack):
    total = stack["X"] + stack["Y"]
    stack["X"] = round(total, 9)
    return


def subtract(stack):
    difference = stack["Y"] - stack["X"]
    stack["X"] = round(difference, 9)
    return


def multiply(stack):
    try:
        wink = False
        product = stack["Y"] * stack["X"]
        stack["X"] = round(product, 9)
    except OverflowError:
        stack["X"] = float(0.0)
        wink = True
    return wink


def divide(stack):
    try:
        wink = False
        quotient = stack["Y"] / stack["X"]
        stack["X"] = round(quotient, 9)
    except ZeroDivisionError:
        stack["X"] = float(0.0)
        wink = True
    return wink


def reciprocal(stack):
    try:
        wink = False
        number = stack["X"]
        quotient = 1.0 / number
        stack["X"] = round(quotient, 9)
    except ZeroDivisionError:
        stack["X"] = float(0.0)
        wink = True
    return wink


def square_root(stack):
    try:
        wink = False
        number = stack["X"]
        root = math.sqrt(number)
        stack["X"] = round(root, 9)
    except ValueError:
        stack["X"] = float(0.0)
        wink = True
    return wink


def log(stack):
    wink = False
    number = float(stack["X"])
    if number > 0.0:
        the_log = math.log10(number)
        stack["X"] = round(the_log, 9)
        return wink
    else:
        stack["X"] = float(0.0)
        wink = True
    return wink


def ln(stack):
    wink = False
    number = float(stack["X"])
    if number > 0.0:
        the_log = np.log(number)
        stack["X"] = round(the_log, 9)
        return wink
    else:
        stack["X"] = float(0.0)
        wink = True
    return wink


def sin(stack):
    number = float(stack["X"])
    sine = math.sin(math.radians(number))
    stack["X"] = round(sine, 9)
    return


def arcsin(stack):
    wink = False
    number = float(stack["X"])
    in_range = -1 <= number <= 1
    if in_range:
        temp = np.arcsin(number)
        asin = np.rad2deg(temp)
        stack["X"] = round(asin, 9)
    else:
        stack["X"] = float(0.0)
        wink = True
    return wink


def cos(stack):
    number = float(stack["X"])
    cosine = math.cos(math.radians(number))
    stack["X"] = round(cosine, 9)
    return


def arccos(stack):
    wink = False
    number = float(stack["X"])
    in_range = -1 <= number <= 1
    if in_range:
        temp = np.arccos(number)
        acos = np.rad2deg(temp)
        stack["X"] = round(acos, 9)
    else:
        stack["X"] = float(0.0)
        wink = True
    return wink


def tan(stack):
    number = float(stack["X"])
    if number / 90.0 == 1.0:
        tangent = float(9.99999999e99)
    elif number / 90.0 == 3.0:
        tangent = float(-9.99999999e99)
    else:
        tangent = math.tan(math.radians(number))
    stack["X"] = round(tangent, 9)
    return


def arctan(stack):
    number = float(stack["X"])
    temp = np.arctan(number)
    atan = np.rad2deg(temp)
    stack["X"] = round(atan, 9)
    return


def exp(stack):
    wink = False
    x = float(stack["X"])
    y = float(stack["Y"])
    if x > 0.0:
        try:
            x_to_y = math.pow(x, y)
            stack["X"] = round(x_to_y, 9)
            return wink
        except OverflowError:
            stack["X"] = float(0.0)
            wink = True
        return wink
    else:
        stack["X"] = float(0.0)
        wink = True
    return wink


def ex(stack):
    wink = False
    try:
        number = float(stack["X"])
        e_to_x = math.exp(number)
        stack["X"] = round(e_to_x, 9)
        return wink
    except OverflowError:
        stack["X"] = float(0.0)
        wink = True
    return wink


def process_action_keys(cmd, disp_col, stack, mem):
    #
    # First the memory/stack/clr, etc., keys
    #
    if cmd == 'off':
        action_chars = ''
        show_calc(action_chars, disp_col, False, True)
        print('HP-35 is powering down')
        time.sleep(0.3)  # Time delay for slower systems to allow the display to update before exit
        sys.exit(0)
    if cmd == 'on':
        print("Calculator is already on.")
        print()
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'clr':
        action_chars = "0.             "
        stack = clear_stack(stack)
        dump_zeros(stack)
        mem, stack = mem_func(mem, stack, cmd)
        return action_chars, stack, mem
    elif cmd == 'e':
        stack = push_stack(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'rd':
        stack = rotate_stack(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'rv':
        stack = reverse_xy(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'sto':
        mem, stack = mem_func(mem, stack, cmd)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'rcl':
        mem, stack = mem_func(mem, stack, cmd)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'clx':
        stack["X"] = float(0.0)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'chs':
        temp = float(stack["X"])
        stack["X"] = temp * -1.0
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'eex':
        action_chars, stack, mem = get_exponent(stack, mem, disp_col)
        return action_chars, stack, mem
    elif cmd == '+':
        add(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == '-':
        subtract(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'x':
        wink = multiply(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == '/':
        wink = divide(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == '1x':
        wink = reciprocal(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'rx':
        wink = square_root(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'log':
        wink = log(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'ln':
        wink = ln(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'sin':
        sin(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'as':
        wink = arcsin(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'cos':
        cos(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'ac':
        wink = arccos(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'tan':
        tan(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'at':
        arctan(stack)
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem
    elif cmd == 'xy':
        wink = exp(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    elif cmd == 'ex':
        wink = ex(stack)
        action_chars = dump_zeros(stack)
        if wink:
            return 'wink', stack, mem
        return action_chars, stack, mem
    else:
        #
        # This point should never be reached, but
        # it's here just in case the legality of
        # input commands check fails
        #
        print(cmd, 'not implemented')
        action_chars = dump_zeros(stack)
        return action_chars, stack, mem


def display_registers(mem, stack):
    print()
    print('M :', mem)
    print()
    for cmd, value in stack.items():
        print(cmd, ':', value)


def main():
    python_check()
    epi_text = "LED display colour codes: G=green,Y=yellow,R=red,B=blue,M=magenta,C=cyan. \nUse " \
               "'off' to turn off calculator and exit program.\n" \
               "Read 'HP-35.txt' for more details about this program"
    my_parser = argparse.ArgumentParser(prog="hp35", formatter_class=RawTextHelpFormatter)
    my_parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.1.0')
    my_parser.add_argument('-V', '--verbose',
                           help='stack (X,Y,Z,T registers) and mem are displayed, Default is False',
                           action='store_true',
                           default=False,
                           )
    my_parser.add_argument('-d', '--display',
                           help='LED display colour,default is white.',
                           action='store',
                           default='W',
                           choices=['W', 'G', 'Y', 'R', 'B', 'M', 'C'],
                           )
    my_parser.epilog = epi_text
    args = my_parser.parse_args()
    verbose = args.verbose
    colour = str(args.display)
    if colour == 'W':
        disp_col = 'white'
    if colour == 'G':
        disp_col = 'green'
    elif colour == 'Y':
        disp_col = 'yellow'
    elif colour == 'R':
        disp_col = 'red'
    elif colour == 'B':
        disp_col = 'blue'
    elif colour == 'M':
        disp_col = 'magenta'
    elif colour == 'C':
        disp_col = 'cyan'
    # Create operational stack as a Python dictionary
    stack = {"T": 0.0,
             "Z": 0.0,
             "Y": 0.0,
             "X": 0.0}
    # Clear everything on startup
    stack = clear_stack(stack)
    mem = float(0.0)
    try:
        chars = "0.             "
        a_number = True
        show_calc(chars, disp_col, a_number, False)
        if verbose:
            display_registers(mem, stack)
        cmd = ''
        while True:
            display_key_menu()
            cmd, a_number = get_cmd(cmd)
            print()
            if not a_number:
                cmd, stack, mem = process_action_keys(cmd, disp_col, stack, mem)
                if cmd != 'wink':
                    to_display = stack["X"]
                    show_calc(to_display, disp_col, True, False)
                else:
                    show_calc(cmd, disp_col, False, False)
                if verbose:
                    display_registers(mem, stack)
            else:
                lo = 0.01
                hi = 1000000000.0
                cmd = float(cmd)
                in_range = min(lo, hi) < cmd < max(lo, hi)
                if in_range:
                    stack["X"] = float(cmd)
                else:
                    stack["X"] = float(np.format_float_scientific(float(cmd), exp_digits=2, unique=False, precision=9))
                show_calc(cmd, disp_col, a_number, False)
                if verbose:
                    display_registers(mem, stack)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt by user")
        print()
        print()


if __name__ == "__main__":
    main()
