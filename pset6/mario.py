from cs50 import *

# getting the user input, and seeing if it is a number
heigth = get_int("Heigth: ")
while heigth <= 0 or heigth > 8:
    heigth = get_int("Heigth: ")


space = heigth - 1

for i in range(heigth):
    # here is the first part of the comment
    print(" " * space, end="")
    print("#" * (heigth - space), end="")

    # here the secon part of mario
    print("  ", end="")
    print("#" * (heigth - space))
    space -= 1
