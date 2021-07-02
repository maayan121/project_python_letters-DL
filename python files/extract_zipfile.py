"""
this python file responsible for Extracting a zip file to an ordinary file
@author: Maayan Eliya
"""
# import the necessary package
from zipfile import ZipFile
import check_directory
import prints_types
import os
    
def extract_Zip(zip_path): 
    """
    This function checks if a file is a zip file - if so the in extracts the images from the zip file.
    It returns an ordinary file - unzipped file
    :param: None
    :return: None
    """
    path = zip_path #the path to the file
    ls = zip_path.split(".") #a list of substrings from the path that split by '.'
    split = os.path.split(ls[0]) #split the path
    filename = split[-1] #the name of the file
    
    #Checks if the file/folder is a zip file by its ending - the file type
    if ls[len(ls)-1] == "zip": #if it is a zip file
        prints_types.printProcess("[INFO] Got a zip file...")
        path = check_directory.Directory.get_New_Dir("Enter a path of an unexisted directory to extract the file to it: ") #the path to the directory the user chose to download the images to it
        
        #Extract the folder to the new location that the user chose
        with ZipFile(zip_path, 'r') as zipObj:
            prints_types.printProcess("[INFO] Extracting the images from the zip file...")
            zipObj.extractall(path) #Extract all the contents of the zip file to a different directory
        
        path = os.path.join(path, filename) #the path to the unzipped folder itself (with the images inside)
        prints_types.printProcess("[INFO] Finished extracting process...")

    else: #if it is not a zip file
        prints_types.printProcess("[INFO] Got ordinary file...")
    return path