"""
this python file handle the classify section
@author: Maayan Eliya
"""
# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import os
from PIL import Image
import PIL.ImageOps
from matplotlib import image
from imutils import paths
import prints_types

IMAGE_SIZE = (28,28)


class ImagePredictor():
    
    def __init__(self, model_path, labels_path, image_path, sign, sorted_data_path):
        """
        Create the ImagePredictor class object.
        :param model_path: string
        :param labels_path: string
        :param image_path: string
        :param sign: boolian
        :param sorted_data_path: string
        :return: None
        """
        self.__model_path = model_path #a path to the trained model
        self.__labels_path = labels_path #a path to the updated labels
        self.__image_path = image_path #a path to an image that should be checked
        self.__sign = sign #True if in the image the letter is black and the background is white,
                           #or False if it the letter is white and the background is black(like in the dataset).
        self.__sorted_data_path = sorted_data_path #a path to the sorted dataset that contains all the letters with the labels
        self.__model = None #the model itself
        self.__lb = None #the label binzrizer
        
        
    def handle_classify(self): 
        """
        this function manage the ImagePredictor (classify) class
        :param: None
        :return: None
        """
        self.__load_Model() #loads the trained model
        image_arr = self.__load_Image() #load the image as array
        self.__predict_Image(image_arr) #predict the image


    def __load_Model(self):
        """
        This function loads the trained model and the label binarizer
        :param: None
        :return: None
        """
        prints_types.printProcess("[INFO] Loading network...")
        self.__model = load_model(self.__model_path) #loads the trained model
        self.__lb = pickle.loads(open(self.__labels_path, "rb").read()) #load the label binzrizer
    
    
    def __load_Image(self):
        """
        this function load the image that should be checked - as an array
        :param: None
        :return: image_arr
        :rtype: numpy array
        it returns the image as a numpy array (after fitting the image - normalization (pixels scale), #colors, #dims,  )
        """
        # pre-process the image for classification
        image_arr = Image.open (self.__image_path)
        if self.__sign == True: #if it is a new image - black letter and white background
            image_arr = PIL.ImageOps.invert(image_arr) #make the letter white and the background black
            image_arr.save(self.__image_path) #save the inverted image
        else:
            image_arr = Image.open (self.__image_path) #if the sign is false then the image is shown on the screen - if it's true then it was already shown
            image_arr.show() #show the image on the screen
        image_arr = image_arr.convert('L') #make the image to be on grayscale
        image_arr.save(self.__image_path) #save the grayscaled image
        image_arr = image_arr.resize((IMAGE_SIZE)) #change the image's size to be (28,28)
        image_arr.save(self.__image_path) #save the image with the new size
        image_arr = image.imread(self.__image_path) #load the image
        image_arr = image_arr.astype("float") / 255.0 #normalization
        image_arr = img_to_array(image_arr) #convert the image to a numpy array
        image_arr = np.expand_dims(image_arr, axis=0) #expand the shape of the array
        return image_arr
   

    def __predict_Image(self,image_arr):
        """
        This function predicts the letter of the image that the user pass.
        It prints "correct" if the input image label is fit to the prediction label,
        else we will print "incorrect".
        It plots the image on the screen
        :param image_arr: numpy array
        :return: None
        """
        # classify the input image
        prints_types.printProcess("[INFO] Classifying image...")
        Predict = self.__model.predict(image_arr)[0] #output predictions for the input image
        idx = np.argmax(Predict) #the index of the max prediction value
        label = self.__lb.classes_[idx] #the label of the prediction
        #check if it predicted correctly
        split_pimg = os.path.split(self.__image_path) #split the path of image that should be predicted to head and tail
        filename = split_pimg[-1] #the name of image that should be predicted (the tail)
        imagePaths = sorted(list(paths.list_images(self.__sorted_data_path))) #list of all the images paths
        flag = False
        for imagePath in imagePaths:
           split = os.path.split(imagePath) #split the path of the image that is currently checked to head and tail
           imgname = split[-1] #the name of the image that is currently checked (the tail)
           if filename == imgname: # if the name of the image that should be predicted equals to the name of the image that is currently checked
               flag = True #it found the image. this is an image from the dataset
               split = os.path.split(split[0])
               imglabel = split[-1] #the actuall label of the image
               if label == imglabel: #if the label that it predicted equals to the actuall label of the image
                   correct = "correct"
               else: 
                    correct = "incorrect"
               break
        if flag == False: #if it is a new image
            #check if it predicted correctly
            imglabel = filename.split(".") 
            imglabel = imglabel[0] #imglabel = the new label of the image (the letter)
            if imglabel == label: #if the label that it predicted equals to the actuall label of the image
                correct = "correct"
            else:
                correct = "incorrect"
        # print the results
        result = "the letter it predicted: {}, prediction: {:.2f}%,  \nthe real label of the image letter: {} \n({})".format(label, Predict[idx] * 100, imglabel, correct)
        prints_types.printProcess("[INFO] {}".format(result)) 
