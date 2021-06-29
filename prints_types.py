"""
this python file contains the function that prints messages for the user in colors.
@author: Maayan Eliya
"""
# import the necessary package
from colorama import init, Fore, Style
	    
def printError(message):
    """
    This function print the message in red color - represent Error.
    :param massage: string #A message to desplay for the user
    :return: None
    """
    init(convert=True)
    print(Fore.RED + message) 
    Style.RESET_ALL
	    
def printInput(message):
    """
    This function print the message in green color - represent the options.
    :param massage: string #A message to desplay for the user
    :return: None
    """
    init(convert=True)
    print(Fore.GREEN + message) 
    Style.RESET_ALL
	        
def printProcess(message):
    """
    This function print the message in blue color - represent the process.
    :param massage: string #A message to desplay for the user
    :return: None
    """
    init(convert=True)
    print(Fore.BLUE + message) 
    Style.RESET_ALL

