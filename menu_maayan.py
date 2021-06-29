# -*- coding: utf-8 -*-
"""
    Python School Project - Handwriting English letter identifier.
    A Deep Learning Computer Program that gets a dataset consists of Handwriting Lowercase English Letters -
    The database is based on the EMNIST library: images of handwritten English letters a-z.
    The program is learning to identify the handwritten English letters, show the accuracy and loss it got during the train process,
    then do test to check the model and at the end predicts an image of a letter the user want or a random letter image from the dataset, or from new images.
    It does it using classification. Classifies the lowercase letters so that they are divided into lowercase categories in English.
    26 categories = 26 letters: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x , y, z.
    
    
@author: Maayan Eliya
"""


"""
this is the main python file that manages the program using tkinter
"""
    
import tk_inter


def main():
    
    """defult directories.
       these directoties are changed according to the user inputs.
    """
    model_path = r"C:/Users/maaya/OneDrive/שולחן העבודה/model/model_new" #a path to the last updated model
    labels_path = r"C:/Users/maaya/OneDrive/שולחן העבודה/labels/labels_new" #a path to the last updated labels
    data_set = r"C:/Users/maaya/OneDrive/שולחן העבודה/All images" #a path to the unsorted dataset that contains all the letters without labels
    sorted_data_path = r"C:/Users/maaya/OneDrive/שולחן העבודה/sorted_dataset" #a path to the sorted dataset that contains all the letters with the labels
    new_images_folder = r"C:/Users/maaya/OneDrive/שולחן העבודה/myHandWriting" #a path to a directory that contains new images of letters that hadn't tested - my handwriting
    #Use tk inter to manage the project - all the cases
    tkinter = tk_inter.TkInter(model_path,labels_path, data_set, sorted_data_path, new_images_folder) #Make an object of the tk_inter class
    tkinter = tkinter.menu_window() #Runs all actions on the object
        
	    
if __name__ == "__main__":
	main()
        