"""
this python file handle the train section
@author: Maayan Eliya
"""
# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from the_model import Model
import matplotlib.pyplot as plt
import numpy as np
import pickle
import prints_types


class TrainModel():
    
    def __init__(self, model_path, labels_path, plot_dir, trainX, trainY, valX, valY, lb):
        """
        Create the TrainModel class object.
        :param model_path: string
        :param labels_path: string
        :param plot_dir: string
        :param trainX: array
        :param trainY: array
        :param valX: array
        :param valY: array
        :param lb: array
        :return: None
        """
        self.__model_path = model_path #the directory the user chose to save the trained model
        self.__labels_path = labels_path #the directory the user chose to save the images labels
        self.__plot_dir = plot_dir #the directory to the folder that the user chose to save the graph images
        self.__trainX = trainX #the inputs for the train - what it should learn
        self.__trainY = trainY #the expected outcomes/labels (the target) to the train inputs
        self.__valX = valX #the inputs for the validation - what it should check
        self.__valY = valY #the expected outcomes/labels (the target) to the validaion inputs
        self.__model = None #the model itself
        self.__lb = lb #the label binzrizer
        self.__EPOCHS = 15 #number of epochs
        self.__INIT_LR = 1e-3 #learning rate
        self.__BS = 32 #batch size
        self.__IMAGE_DIMS = (28, 28, 1) #image dimensions
        

    def handle_train(self):
        """
        this function manage the TrainModel class - train section
        return the train model path and the images labels path
        :param: None
        :return: self.__model
        :rtype: file
        """
        history = self.__train() #do the training process
        self.__save_model() #save the model in the path the user chose
        self.__graph1(history, self.__plot_dir+ r"\plot1.png") #graph that shows the Training Loss and Accuracy
        self.__graph2(history, self.__plot_dir +r"\plot2.png") #graph that shows the Validation Loss and Accuracy
        self.__graph3(history, self.__plot_dir +r"\plot3.png") #graph that shows the Training and Validation togheter
        return (self.__model) #return the trained model 
    
    
    def __train(self):
        """
        This function responsible for training the model.
        The model learn from the train dataset to identify the Handwriting English Lowercase Letters.
        :param: None
        :return: H #the history
        :rtype: History object
        """
        # construct the image generator for data augmentation - it allow to augment the images in real-time while the model is still training
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
            height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
            fill_mode="nearest")
        
        # initialize the model
        prints_types.printProcess("[INFO] Compiling model...")
        self.__model = Model.build(width=self.__IMAGE_DIMS[1], height=self.__IMAGE_DIMS[0],
        depth= self.__IMAGE_DIMS[2], classes=len(self.__lb.classes_)) #Make an object of the Model class
        
        # train the network
        opt = Adam(lr=self.__INIT_LR, decay=self.__INIT_LR / self.__EPOCHS) #the optimizer to the model - Adam
        
        self.__model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"]) #configures the model for the training
        
        self.__model.summary() #Prints a string summary of the network.
        prints_types.printProcess("[INFO] Training network...")
        
        #Fit model on training data
        H = self.__model.fit(
        aug.flow(self.__trainX, self.__trainY, batch_size=self.__BS),
        validation_data=(self.__valX, self.__valY),
        steps_per_epoch=len(self.__trainX) // self.__BS,
        epochs=self.__EPOCHS, verbose=1)
        return H #return the training process
          
        
    def __save_model(self):
        """
        This function responsible for saving the trained model and the label binarizer on the directories the user chose.
        :param: None
        :return: None
        """
        prints_types.printProcess("[INFO] Serializing network...")
        self.__model.save(self.__model_path) #save the model
        prints_types.printProcess("[INFO] Serializing label binarizer...")
        f = open(self.__labels_path, "wb")
        f.write(pickle.dumps(self.__lb)) # save the label binarizer
        f.close()


    def __graph1(self,H, plot_path):
        """
        This function creates a graph that represents the Training Loss and Accuracy,
        and save an images that contains the graph on the path the user chose.
        :param H: History object
        :param plot_path: string
        :return: None
        """
        plt.style.use("ggplot")
        plt.figure()
        N = self.__EPOCHS
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss") #plot the training loss
        plt.plot(np.arange(0, N), H.history["accuracy"], label="train_accuracy") #plot the training accuracy
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig(plot_path) #save the praph to file on the path that the user chose to save the results
        plt.show() #show the graph on the screen
        plt.close()


    def __graph2(self,H, plot_path):
        """
        This function creates a graph that represents the Validation Loss and Accuracy,
        and save an images that contains the graph on the path the user chose.
        :param H: History object
        :param plot_path: string
        :return: None
        """
        plt.style.use("ggplot")
        plt.figure()
        N = self.__EPOCHS
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss") #plot the validation loss
        plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_accuracy") #plot the validation accuracy
        plt.title("Validation Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig(plot_path) #save the praph to file on the path that the user chose to save the results
        plt.show()
        plt.close()


    def __graph3(self, history, plot_path):
        """
        This function creates a graph that represents the Training and Validation Loss and Accuracy,
        and save an images that contains the graph on the path the user chose.
        :param H: History object
        :param plot_path: string
        :return: None
        """
	    # plot loss
        plt.subplot(211)
        plt.title('Model Loss')
        plt.plot(history.history['loss'], color='green', label='train') #plot the training loss
        plt.plot(history.history['val_loss'], color='orange', label='validation') #plot the validation loss
        plt.xlabel("Epoch #")
        plt.ylabel("Loss")
        plt.legend(loc="upper right")
	    # plot accuracy
        plt.subplot(212)
        plt.title('Model Accuracy')
        plt.plot(history.history['accuracy'], color='green', label='train') #plot the training accuracy
        plt.plot(history.history['val_accuracy'], color='orange', label='validation') #plot the validation accuracy
        plt.xlabel("Epoch #")
        plt.ylabel("Accuracy")
        plt.legend(loc="upper right")
        plt.savefig(plot_path) #save the praph to file on the path that the user chose to save the results
        plt.show() #show the graph on the screen
        plt.close()

