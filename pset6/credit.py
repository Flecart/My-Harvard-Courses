from re import search
from cs50 import *


def main():

    number = get_string("Number: ")

    if verify(number) == False:
        print("INVALID")
        return

    check_and_print(number)

    return

# verifying the credit card with lhn algoritm


def verify(string):

    if not string.isdigit():
        return False

    check = 0

    # easier to work with the reversed string
    string = string[::-1]

    # first part, getting from second digit
    for i in range(1, len(string), 2):

        intero = 2 * int(string[i])
        if intero >= 10:
            intero = intero % 10 + (intero - intero % 10) / 10
        check += intero

    # ending the algoritm by last sums
    for i in range(0, len(string), 2):
        check += int(string[i])

    # check after this was a float, i reverse the number so i can
    # check =
    # its its nice i return
    if check % 10 == 0:
        return True

    return False

# printing the result


def check_and_print(number):

    # begins with amex strings and long 15 digits
    if search("(^37)|(^34)$", number) and len(number) == 15:
        print("AMEX")
        return

    # dont move this down or there is some strange bug i didnt understand
    # like the regex down, search("(^51)|(^52)|(^53)|(^54)|(^55)|$", number)
    # it matches 4111111111111111 for some unknown reason
    if number[0] == "4" and (len(number) == 13 or len(number) == 16):
        print("VISA")
        return

    if search("(^51)|(^52)|(^53)|(^54)|(^55)|$", number) and len(number) == 16:
        print("MASTERCARD")
        return

    print("INVALID")
    return


main()
