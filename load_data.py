"""
this python file responsible for loading the data - handle the data before train and test
@author: Maayan Eliya
"""
# import the necessary packages
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from imutils import paths
import numpy as np
import random
import os
from PIL import Image
from matplotlib import image
import prints_types

IMAGE_SIZE = (28,28)


class LoadData():
    
    def __init__(self, dataset_path):
        """
        Create the HandleData class object.
        :param dataset_path: string
        :return: None
        """
        self.__dataset_path = dataset_path #the sorted dataset directory
        self.__trainX = None #the inputs for the train - what it should learn
        self.__trainY = None #the expected outcomes/labels (the target) to the train inputs
        self.__testX = None #the inputs for the test - what it should check
        self.__testY = None #the expected outcomes/labels (the target) to the test inputs
        self.__valX = None #the inputs for the validation - what it should check
        self.__valY = None #the expected outcomes/labels (the target) to the validaion inputs
        self.__lb = LabelBinarizer() #binarize the labels (an easy tool for classification)
        self.__data = [] #list of all the images as arrays
        self.__labels = [] #labels list of all the images
        

    def handle_dataset(self):
        """
        this function manage the HandleData class
        :param: None
        :return self.__trainX: array
        :return self.__trainY: array
        :return self.__testX: array
        :return self.__testY: array
        :return self.__valX: array
        :return self.__valY: array
        :return self.__lb: array
        """
        self.__loading_Images() #loads all the images
        self.__scale_Pixels() #scales the images pixels to range [0, 1]
        self.__divide_data() #devides the dataset into train, validation, test
        return (self.__trainX, self.__trainY, self.__testX, self.__testY, self.__valX, self.__valY, self.__lb)


    def __loading_Images(self):
        """
        This function loads all the images from the current directory - the sorted dataset
        :param: None
        :return: None
        """
        #makes a list of the images paths and randomly shuffle them
        prints_types.printProcess("[INFO] Loading images...")
        imagePaths = sorted(list(paths.list_images(self.__dataset_path))) #makes a sorted list that contains the images paths
        random.seed(42)
        random.shuffle(imagePaths) #shuffle the list randomly
        
        # loops over the dataset images and makes an array
        for imagePath in imagePaths:
            #loads the image as gray scale, converts it to numpy array and stores it in the data list, add add its label to the array
            image_arr = Image.open (imagePath)
            image_arr = image_arr.convert('L') #make the image to be on grayscale
            image_arr.save(imagePath) #save the grayscaled image
            image_arr = image_arr.resize((IMAGE_SIZE)) #change the image's size to be (28,28)
            image_arr.save(imagePath) #save the image with the new size
            image_arr = image.imread(imagePath) #read the image into an array
            
            image_arr = img_to_array(image_arr) #convert the image to a numpy array
            self.__data.append(image_arr) #add the image array into the data list
            
            #extract the class label from the image path and update the labels list
            label = imagePath.split(os.path.sep)[-2] #the image's label
            self.__labels.append(label) #add the image's label imto the labels array
       
 
    def __scale_Pixels(self):    
        """ 
        This function scales the images pixels to range [0, 1] from range [0, 255].
        The data list stores all the images by arrays, so convert this list -> we convert all the images pixels range
        :return: None
        """
        self.__data = np.array(self.__data, dtype="float") / 255.0 #normalization of the data array
        self.__labels = np.array(self.__labels) #the labels binary file
        prints_types.printProcess("[INFO] data matrix: {:.2f}MB".format(self.__data.nbytes / (1024 * 1000.0))) #the data size
    
    
    def __divide_data(self):
        """ 
        This function devides the dataset into train (70%), validation (10%), test (20%)
        :return: None
        """
        #Linear transformation - Fit the label binarizer and transform the multi-class labels to binary labels.
        self.__labels = self.__lb.fit_transform(self.__labels)
    
        #Divides the data into train, test, validation using train_test_split:
        #remaining 20% of the data for testing. Using 70% for training and 10% for validation.
        #x's are the features we are using as input for the model. Y's are the expected outcomes/labels (the target).
        (self.__trainX, self.__testX, self.__trainY, self.__testY) = train_test_split(self.__data, self.__labels, test_size=0.2, random_state=42) #split to 80% train, 20% test
        (self.__trainX, self.__valX, self.__trainY, self.__valY) = train_test_split(self.__trainX, self.__trainY, test_size=0.125, random_state=1) #split to 70% train, 10% validation (0.125 x 0.8 = 0.1)
    
    