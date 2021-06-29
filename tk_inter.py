"""
this is the file that contacts the user and manages the program according to the user choices
@author: Maayan Eliya
"""
# import the necessary packages
import os
import extract_zipfile
import train_model
import test_model
import classify
import load_data
import check_directory
import prints_types
import check_input
import random   
import keras
import tkinter as tk
import requests
import shutil
from pathlib import Path
from PIL import Image


class TkInter():
    
    def __init__(self,model_path,labels_path, data_set, sorted_data_path, new_images_folder):
        """
        Create the TkInter class object.
        :param model_path: string
        :param labels_path: string
        :param data_set: string (path)
        :param sorted_data_path: string
        :param new_images_folder: string (path)
        :return: None
        """
        self.__model_path = model_path #a path to the last updated model
        self.__labels_path = labels_path #a path to the last updated labels
        self.__data_set = data_set #a path to the unsorted dataset that contains all the letters without labels
        self.__sorted_data_path = sorted_data_path #a path to the sorted dataset that contains all the letters with the labels
        self.__new_images_folder = new_images_folder #a path to a directory that contains new images of letters that hadn't tested - my handwriting
        self.__plot_dir = None #the directory that will include the plots from the train and validation
        self.__model = None #the model itself
        self.__trainX = None #the inputs for the train - what it should learn
        self.__trainY = None #the expected outcomes/labels (the target) to the train inputs
        self.__testX = None #the inputs for the test - what it should check
        self.__testY = None #the expected outcomes/labels (the target) to the test inputs
        self.__valX = None #the inputs for the validation - what it should check
        self.__valY = None #the expected outcomes/labels (the target) to the validaion inputs
        self.__lb = None #the labels
        
        
    def menu_window(self):
        """
        this function makes the first window - the menu window.
        :param: None
        :return: None
        """
        #make screens with messages and buttons to contact the user using Tkinter
        root = tk.Tk() #the root for the main window
        root.geometry("340x300") #define the window's size
        root.title("The Menu")
        frame1 = tk.Frame(master=root, width=340, height=20, bg="Light blue")
        frame1.pack(fill=tk.X)
        msg = tk.Message( root, width=310, bg="Light pink", text = "Hello! \nYou are going to start run the project - identify English letters. \n\nSoon when you start you will see some windows one after one, please do what they say. \nFirst, you will load the data. \nThen, you will train the model. \nAfter that you will test it. \nAt the end you will choose the option you want. \n\nIn order to start please press on the button down here.  ")  
        msg.pack()
        tk.Button(root, bg = "green", text='Click here to start', command=self.__data_window).pack() #button to start - opens the data window
        root.protocol("WM_DELETE_WINDOW", root.iconify) #make the top right close button (X) minimize (iconify) the window/form
        #create a menu bar with an Exit command
        menubar = tk.Menu(root)
        menubar.add_cascade(label = 'Exit', command = root.destroy)
        root.config(menu=menubar)
        root.mainloop()
	    
        
    def __data_window(self):
        """
        this function create a new window to load the data
        :param: None
        :return: None
        """
        newWindow = tk.Toplevel() #the root for the new window
        newWindow.geometry("200x100") #define the window's size
        newWindow.title("Load the data")
        #a button to load the data and to create a new window for the train
        data = tk.Button(newWindow, bg = "Yellow", text = "Click here to load the Data", command = self.__combine_funcs (self.__case_Data, self.__train_window))
        data.pack()
        newWindow.protocol("WM_DELETE_WINDOW", newWindow.iconify) #make the top right close button (X) minimize (iconify) the window/form
        #create a menu bar with an Exit command
        menubar = tk.Menu(newWindow)
        menubar.add_cascade(label = 'Exit', command = newWindow.destroy)
        newWindow.config(menu=menubar)
        
    
    def __train_window(self):
        """
        this function create a new window to train the model
        :param: None
        :return: None
        """
        newWindow = tk.Toplevel() #the root for the new window
        newWindow.geometry("340x150") #define the window's size
        newWindow.title("Train the model")
        msg = tk.Message(newWindow, width=310, bg="Light green", text = "choose the option you want and then click on start")  
        msg.pack()
        options = {"Train the Model" : '1', 
    		"Use the last updated model" : '2'} #the two options
        var=tk.StringVar(newWindow) #value holder for strings variables.
        var.set(None)
        for (txt, val) in options.items(): #a loop to create 2 Radiobuttons instaed of creating each button separately
        	tk.Radiobutton(newWindow, bg = "Light yellow", text=txt, variable=var, value=val).pack() #create 2 Radiobuttons for the 2 options
        tk.Button(newWindow, text='Start', command=lambda: self.__start_train(var.get())).pack() #the start button
        newWindow.protocol("WM_DELETE_WINDOW", newWindow.iconify) #make the top right close button (X) minimize (iconify) the window/form
        #create a menu bar with an Exit command
        menubar = tk.Menu(newWindow)
        menubar.add_cascade(label = 'Exit', command = newWindow.destroy)
        newWindow.config(menu=menubar)        
        
        
      
    def __start_train(self,choice):
        """
        This function responsible for start the option to the train that the user chose.
        2 options:
            1) Train the Model
    		2) Use the last updated model
        :param choice: int (1/2)
        :param dataset: string (path) - unsorted dataset or new images dataset
        :return: None
    	"""
        if choice=='1': #the user chose to predict a specific image
            self.__combine_funcs (self.__case_Train(), self.__test_window()) #a button to train the model and to create a new window for the test -> calls the self.__case_Train() function
        elif choice=='2': #the user chose o predict random images
            self.__combine_funcs (self.__case_lastmodel(), self.__test_window()) #a button to use the last model the model and to create a new window for the test -> calls the self.__case_lastmodel() function
  
    
        
    def __test_window(self):
        """
        this function create a new window to test the model
        :param: None
        :return: None
        """
        newWindow = tk.Toplevel() #the root for the new window
        newWindow.geometry("200x100") #define the window's size
        newWindow.title("Test the model")
        #a button to test the model and to create a new window for the predict options       
        test = tk.Button(newWindow,  bg = "Orange", text = "Click here to test the Model", command = self.__combine_funcs (self.__case_Test, self.__options_window))
        test.pack()
        newWindow.protocol("WM_DELETE_WINDOW", newWindow.iconify) #make the top right close button (X) minimize (iconify) the window/form
        #create a menu bar with an Exit command
        menubar = tk.Menu(newWindow)
        menubar.add_cascade(label = 'Exit', command = newWindow.destroy)
        newWindow.config(menu=menubar)


    def __options_window(self):
        """
        this function create a new window to show options for predicting
        :param: None
        :return: None
        """
        newWindow = tk.Toplevel() #the root for the new window
        newWindow.geometry("340x150") #define the window's size
        newWindow.title("Predict options")
        msg = tk.Message(newWindow, width=310, bg="Light pink", text = "choose the option you want and then click on start")  
        msg.pack()
        options = {"Predict a specific image" : '1', 
    		"Predict random images" : '2'} #the two options
        var=tk.StringVar(newWindow) #value holder for strings variables.
        var.set(None)
        for (txt, val) in options.items(): #a loop to create 2 Radiobuttons instaed of creating each button separately
        	tk.Radiobutton(newWindow, bg = "Light yellow", text=txt, variable=var, value=val).pack() #create 2 Radiobuttons for the 2 options
        tk.Button(newWindow, text='Start', command=lambda: self.__start_options(var.get())).pack() #the start button
        newWindow.protocol("WM_DELETE_WINDOW", newWindow.iconify) #make the top right close button (X) minimize (iconify) the window/form
        #create a menu bar with an Exit command
        menubar = tk.Menu(newWindow)
        menubar.add_cascade(label = 'Exit', command = newWindow.destroy)
        newWindow.config(menu=menubar)
        
        
    def __start_options(self,choice):
        """
        This function responsible for start the option to predict that the user chose.
        2 options:
            1) Predict a specific image
    		2) Predict random images
        :param choice: int (1/2)
        :param dataset: string (path) - unsorted dataset or new images dataset
        :return: None
    	"""
        if choice=='1': #the user chose to predict a specific image
            self.__case_Specific_image() #calls the self.__case_Specific_image() function
        elif choice=='2': #the user chose o predict random images
            self.__case_Random() #calls the self.__case_Random() function
  
        
    def __combine_funcs(self, *funcs):
        """
        this function allows me to use a single button to call 2 functions insted of only 1 (make a combined function)
        :param: the functions
        :return: the combined function
        """
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    	
    def __case_Data(self):
        """
        This function loads the dataset - the sorted and unsorted and updated the paths (self.data_set,self.sorted_data_path).
        It also divides it to train, test, validation using handle_data class and updates these class variables.
        :param: None
        :return: None
        2 options:
            1) Using datasets that are already downloaded to the computers.
            2) Download the datasets from my Github user (zip folders).
        for each dataset checks if it a zip folder or not:
            zip -> if the folder is a zip folder then extract it to a new path and set the self.data_set/self.sorted_data_path to the unzipped folder.
            not zip -> if it is not a zip folder (but an an ordniry folder) it keeps it that way.
        
        """
        prints_types.printInput("Please enter 1 to download the datasets from Github, or 2 to use datasets that you have already downloaded to your computer: ")
        num = input ("Enter: ")
        num = check_input.check_1or2(num)
        if (num == 1): #if the user wanted to download the datasets from Github
            prints_types.printProcess("[INFO] Downloading the All_images file - the unsorted dataset from GitHub...")
            r = requests.get('https://raw.github.com/maayan121/project_python_letters-DL/main/All%20images.zip') #get the unsorted dataset from Github
            filename = "All images.zip"
            all_img_path = self.__download_file(filename, r) #the path to the zip file that was downloaded from Github
            self.__data_set = extract_zipfile.extract_Zip(all_img_path) # return the folder path to the unzipped unsorted dataset after extracting it     
            prints_types.printProcess("[INFO] Downloading the Sorted dataset file from GitHub...")
            r = requests.get('https://raw.github.com/maayan121/project_python_letters-DL/main/sorted_dataset.zip') #get the sorted dataset from Github
            filename = "sorted_dataset.zip"
            sorted_img_path = self.__download_file(filename, r) #the path to the zip file that was downloaded from Github
            self.__sorted_data_path = extract_zipfile.extract_Zip(sorted_img_path) # return the folder path to the unzipped sorted dataset after extracting it    
        
        else: #if the user has already downloaded the datasets
            prints_types.printProcess("[INFO] Downloading the datasets from your computer...")
            self.__data_set = extract_zipfile.extract_Zip(self.__data_set) # return the folder path to the unzipped unsorted dataset after extract it (if it was a zip file at first)    
            self.__sorted_data_path = extract_zipfile.extract_Zip(self.__sorted_data_path) # return the folder path to the unzipped sorted dataset after extract it (if it was a zip file at first)
	    
        #load data for the project - divides it to train, test, validation using handle_data class and updates these class variables
        data = load_data.LoadData(self.__sorted_data_path) #make an object of the handle_data class
        (self.__trainX, self.__trainY, self.__testX, self.__testY, self.__valX, self.__valY, self.__lb) = data.handle_dataset() #runs all the handle_data class' actions on the object
            

    def __download_file(self, filename, r):
        """
        This function downloads the dataset - the sorted and unsorted from Github.
        :param filename: string
        :param r: requests.Response (a GET requast)
        :return: img_dir #the path to the zip folder (where the user wanted to put it)
        :rtype: string (path)
        """
        with open(filename, "wb") as file:
            file.write(r.content)
            img_path = os.path.join(Path().absolute(), filename) #the path to the images dataset that was downloaded from Github
        prints_types.printInput("Please enter 1 if you want to choose a path to download the zip file to, or 2 to download the zip file to the directory where the project is located: ")
        num = input ("Enter: ")
        num = check_input.check_1or2(num)
        if (num == 1): #if the user wanted to choose a path
            prints_types.printInput("Enter a path of an unexisted directory to put the zip dataset directory in it. \nPlease don't choose a name that include . (point): ") #the directory that the user chose to download the images to it
            img_dir = input ("Enter: ")
            os.mkdir(img_dir) #make the directory
            prints_types.printProcess("[INFO] Downloading the dataset to the path you chose...")
            shutil.move(img_path,img_dir) #move the zip folder to the path the user chose
            img_dir = os.path.join(img_dir, filename) #the path to the zip folder itself
        else:
            img_dir = img_path
        return img_dir


    def __case_Train(self):
        """
        This function responsible for training the model. #if the user chose to do the train process
        Doing the train process: inputs from the user: self.model_path, self.labels_path, self.plot_dir.
        Uses the sorted data set, does the training with train_model class:
        This function calls to the handle_train() fanction that locaited in train_model.py file
        Then save the updated model in self.model.
  	    the model path -> contains the trained model
        labels path - contains the labels for each images (for the prediction)
        the plot path -> contains the graphes from train and validation
        :param: None
        :return: None
        """
        self.__model_path = check_directory.Directory.get_New_Dir("Enter the full path (with the name) to output model (unexisted folder): ")
        self.__labels_path = check_directory.Directory.get_New_Dir("Enter the full path (with the name) to output label binarizer (unexisted folder): ")
        while self.__model_path == self.__labels_path: #check that the paths are not the same
            prints_types.printError("Error - file will be override")
            self.__labels_path = check_directory.Directory.get_New_Dir("Enter the full path (with the name) to output label binarizer: ") #if it is the same then input again
        self.__plot_dir = check_directory.Directory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ")
        while self.__model_path == self.__plot_dir or self.__labels_path == self.__plot_dir: #check that the paths are not the same
            prints_types.printError("Error - file will be override")
            self.__plot_dir = check_directory.Directory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ") #if it is the same then input again
        os.mkdir(self.__plot_dir) #make the plot directory
           
        train_obj = train_model.TrainModel(self.__model_path,self.__labels_path, self.__plot_dir, self.__trainX, self.__trainY, self.__valX, self.__valY, self.__lb) #Make  an object of the train_model class
        self.__model = train_obj.handle_train() #Runs all actions on the object - do the train process
        prints_types.printProcess("[INFO] Using trained model")


    def __case_lastmodel(self):
        """
        This function responsible for Using the last updated model from the defult directories.
        #if the user chose to use the last updated model
        :param: None
        :return: None
        """
        self.__model = keras.models.load_model(self.__model_path) #load the last model
        prints_types.printProcess("[INFO] Using trained model")


    def __case_Test(self):
        """
        This function responsible for testing the model.
        Uses the updated model and test it.
        This function uses TestModel() class that locaited in test_model.py file and runs the function there.
        :param: None
        :return: None
        """
        test_model.TestModel(self.__testX, self.__testY, self.__model)
    	
    
    def __case_Specific_image(self):
        """
        This function responsible for predicting a specific image that the user choose.
        Uses the updated model and labels.
        this function call to the handle_classify() fanction that locaited in classify.py file.
        :param: None
        :return: None
        """
        image_path = check_directory.Directory.is_Exsists("Enter the image path, note that the image must be type JPEG/JPG (not PNG): ") #the path to the image that the user wanted to check
        prints_types.printInput("please enter 1 if in the image the letter is black and the background is white \nor 2 if it the letter is white and the background is black (an image from the dataset): ")
        sign = input ("Enter: ")
        sign = check_input.check_1or2(sign)
        if sign == 1:
            image1 = Image.open (image_path)
            image1.show() #show the image on the screen
            predict_obj = classify.ImagePredictor(self.__model_path, self.__labels_path, image_path, True, self.__sorted_data_path) #Make an object of the classify class 
        else:
            predict_obj = classify.ImagePredictor(self.__model_path, self.__labels_path, image_path, False, self.__sorted_data_path) #Make an object of the classify class 
        predict_obj.handle_classify() #Runs all actions on the object
    	
     
    def __case_Random(self):
        """
        This function responsible for predicting random images.
        Uses the updated model and labels.
        2 ways:
            1) Random images from the unsorted dataset.
            2) Random images from the directory that contains new unlearned images - my handwriting.
        this function call to __checkPredict fanction.
        :param: None
        :return: None
        """        
        prints_types.printProcess("[INFO] Learned images...")
        prints_types.printInput("how many random images from the unsorted dataset do you want to check? ")
        num = input ("Enter the number: ") #the nymber of images the user want to check
        num = check_input.check_int(num)        
        self.__checkPredict(num, self.__data_set, False) #calls the function that responsible for predicting the random images
        prints_types.printProcess("[INFO] New images...")
        prints_types.printInput("how many random images from the new images do you want to check? ")
        num = input ("Enter the number: ") #the nymber of images the user want to check
        num = check_input.check_int(num)      
        self.__checkPredict(num, self.__new_images_folder, True) #calls the function that responsible for predicting the random images
	    
	   
    def __checkPredict(self, num, dataset, sign):
        """
        This function responsible for predicting random images.
        Uses the updated model and labels.    	    
        this function predict [num] random images from the folder
        this function call to the handle_classify() fanction that locaited in classify.py file.
        :param num: int
        :param dataset: string (path) - unsorted dataset or new images dataset
        :param sign: boolian #true if the image is a new one or false if it from the dataset
        :return: None
    	"""
        list_of_images = os.listdir(dataset) #make a list of the images in the dataset
        for i in range(num): #loop that checks [num] images
            image_name = random.choice(list_of_images) #choose an image randomlly
            image_path = os.path.join(dataset, image_name) #the path to the image
            if sign == True:
                image1 = Image.open (image_path)
                image1.show() #show the image on the screen
                prints_types.printInput("please enter 1 if in the image the letter is black and the background is white \nor 2 if it the letter is white and the background is black: ")
                sign = input ("Enter: ")
                sign = check_input.check_1or2(sign)
                if sign == 2:
                    sign = False
            predict = classify.ImagePredictor(self.__model_path, self.__labels_path, image_path, sign, self.__sorted_data_path) #Make an object of the classify class 
            predict.handle_classify() #Runs all actions on the object
            list_of_images.remove(image_name) #remove the checked image from the list so it want check it again
	        


