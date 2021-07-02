"""
this python file handle the test section
@author: Maayan Eliya
"""
# import the necessary package
import prints_types


class TestModel():
    
    def __init__(self, testX, testY, model):
        """
        Create the TestModel class object.
        :param testX: array
        :param testY: array
        :param plot_dir: string
        :param model: file
        :return: None
        """
        self.__testX = testX #the inputs for the test - what it should check
        self.__testY = testY #the expected outcomes/labels (the target) to the test inputs
        self.__model = model #the model itself
        self.__test() #do the testing process
        
    
    def __test(self):
        """
        This function responsible for testing the model.
        it evaluate the model on the test data using `evaluate` - check the trained model.
        :param: None
        :return: None
        """
        prints_types.printProcess('\n# Evaluate on test data')
        results = self.__model.evaluate(self.__testX, self.__testY, batch_size=32) #the results of the testing
        print('test loss ' + str(results[0])  + ' , test acc ' + str(results[1])) #print the results
