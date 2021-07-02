"""
this python file responsible for checking an input - if it valid according to the instructions.
@author: Maayan Eliya
"""
# import the necessary package
import prints_types


def check_1or2(num):
    """
    This function checks if the input is 1 or 2. If not it asks for another input.
    :param num: string
    :return: num #a valid input
    :rtype: int (1/2)
    """
    while True:
        if num == '1' or num == '2':
            num = int(num)
            return num
            break
        else:
            prints_types.printError("[Error] This is not a valid input.")
            prints_types.printInput("Please enter 1 or 2 according to what it said before: ")
            num = input ("Enter: ")
            continue        
 
def check_int(num):
    """
    This function checks if the input is an integer number. If not it asks for another input.
    :param num: string
    :return: num #a valid input
    :rtype: int
    """
    while True:
        if num.isnumeric() == True:
            num = int(num)
            return num
            break
        else:
            prints_types.printError("[Error] This is not a valid input.")
            prints_types.printInput("Please enter an integer number: ")
            num = input ("Enter: ")
            continue        
        