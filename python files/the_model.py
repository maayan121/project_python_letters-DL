"""
this file contains a class with a static method
this method declared the model layers
@author: Maayan Eliya
"""
# import the necessary package
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K
	

class Model():
    
    @staticmethod
    def build(width, height, depth, classes, finalAct="softmax"):
        """
        This function creates the Model.
        # Get the imaged dims
        :param width: int
        :param height: int
        :param depth: int
        # Get the number of the categories
        :param classes: int
        # Get the final activation function - by defual "softmax"
        :param finalAct: string
        :return: None
        """
        
        #It initialize the model with the input shape to be "channels last" ->  update the input shape and channels dimension
        model = Sequential()
        inputShape = (height, width, depth) #if the channels represent the color in the last place
        chanDim = -1 #if channel laste then chanDim=-1

        # if we are using "channels first", update the input shape and channels dimension
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width) #if the channels represent the color in the first place
            chanDim = 1 #if channel first then chanDim=1
	
        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape, activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape, activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.15))
	
        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))
	
        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(256, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))
	
        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(256, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(512, (3, 3), padding="same", activation="relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))
	
        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation(finalAct))
	

        # return the constructed network architecture
        return model

