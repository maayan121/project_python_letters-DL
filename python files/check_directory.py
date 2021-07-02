"""
this python file handle the input section - checks if it's okey
@author: Maayan Eliya
"""
# import the necessary package
import os
import prints_types


class Directory():
    
    @staticmethod
    def is_Exsists(message):
        """
        This function request an exsisting directory from the user.
        It returns the path only if cheak_exsists_dir() function returns true.
        This function keeps request a directory path until it will be an existed path - valid according to the cheak function.
        :param massage: string #A message to desplay for the user
        :return: path
        :rtype: string
        """
        prints_types.printInput(message)
        path = input("Enter: ")
        while not Directory.__check_Exsists_Dir(path): #if the directory is not existed it request a new path
            prints_types.printInput(message)
            path = input("Enter: ")
        return path


    @staticmethod
    def __check_Exsists_Dir(path):
        """
        This function checks if the current directory exsists.
        Returns true if the path is valid (exist), otherwise returns false .
        :param path: string #A path that the user gave
        :return: True/False
        :rtype: boolian
        """
        if not os.path.exists(path): #id the directory is not existed
            prints_types.printError("Error - no such file or directory")
            return False
        return True
    
    
    @staticmethod
    def get_New_Dir(message):
        """
        This function request a new directory from the user.
        It returns the path only if cheak_new_dir() function return true.
        This function keeps request a directory until it will be not existed path - valid according to the cheak function.
        :param massage: string #A message to desplay for the user
        :return: path
        :rtype: string
        """
        path = ""
        while not Directory.__check_New_Dir(path): #if the directory is existed then it request a new path
            prints_types.printInput(message)
            path = input("Enter: ")
        return path 
   
    
    @staticmethod
    def __check_New_Dir(path):
        """
        This function checks if the current directory is not exsists.
        Returns true if the path is valid (new directory - not exist), otherwise returns false .
        :param path: string #A path that the user gave
        :return: True/False
        :rtype: boolian
        """
        #cheak that the path is not already exists
        if(os.path.exists(path)): #if the path is already exists
            prints_types.printError("Error - this directory is already exsists")
            return False
        #if the path is not exists
        try: #try to make a folder in the current path
             #if its succeed the path is valid
            os.mkdir(path) #Create a directory 
            os.rmdir(path) #Remove a directory
            return True
         
        except: #the path is not vaild and the function return false
            if(path != ""):
                prints_types.printError("Error - directory is not valid")            
                return False
