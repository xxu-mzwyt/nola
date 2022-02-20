import os
from model_selection import model_selection 
from analyze import analyze

title = r"""
                   _        
                  | |       
     _ __    ___  | |  __ _ 
    | '_ \  / _ \ | | / _` |
    | | | || (_) || || (_| |
    |_| |_| \___/ |_| \__,_|
==========================================================     
"""

carId = -1


def main_interface():

    global carId

    while True:
        os.system('cls')
        print(title)
        print("   CHOOSE AN OPTION TO CONTINUE\n")
        print("   1) Search for your car model")
        if carId < 0:
            print("   2) -------------------------")
        else:
            print("   2) Fuel efficient directions")
        print("   3) Help\n")
        opt = input("   > ")

        if carId < 0:
            valid = ["1", "3"]
        else:
            valid = ["1", "2", "3"]

        if opt not in valid:
            print("   Invalid input. Please try again.")
            continue

        else:
            if opt == "1":
                carId = model_selection()
                continue
            elif opt == "2":
                st = input("   Please input your origin:\n   > ")
                de = input("   Please input your destination:\n   > ")
                analyze(st, de, str(carId))
                continue
            else:
                print("   See https://github.com/xxu-mzwyt/nola.")


if __name__ == '__main__':
    main_interface()