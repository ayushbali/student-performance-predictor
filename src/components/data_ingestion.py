import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation, DataTransformationConfig


@dataclass
class DataIngestionConfig:
    # DataIngestionCongig class will have the *path* where the data will be stored after we fetch it from the source. We will store the data in artifacts folder.

    # Path to store the raw data
    raw_data_path: str = os.path.join('artifacts', 'data.csv')
    # Path to store the train data
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    # Path to store the test data
    test_data_path: str = os.path.join('artifacts', 'test.csv')

class DataIngestion:
    # DataIngestion class will have the method to fetch the data from the source and store it in the artifacts folder. It will also split the data into train and test data.
    def __init__(self):
        '''
        Class constructor for DataIngestion class. It will initialize the DataIngestionConfig class (which has the path where the data will be stored after we fetch it from the source) and is stored in the ingestion_config variable.

        Methods: 
            constructor: This method will initialize the DataIngestionConfig class and is stored in the ingestion_config variable.
            
            initiate_data_ingestion: This method will fetch the data from the source and store it in the artifacts folder. It will also split the data into training and testing set and store it in the artifacts folder.
            returns: 
                train_data_path: str: Path to the training data.
                test_data_path: str: Path to the testing data.
            
        '''
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        '''
        This function will fetch the data from the source and store it in the artifacts folder. It will also split the data into training and testing set and store it in the artifacts folder.
        Returns:
            train_data_path: str: Path to the training data.
            test_data_path: str: Path to the testing data.
        '''
        logging.info('Entered Data Ingestion Component')

        try:
            '''
                Workflow: 
                1. Read the dataset as DataFrame.
                2. Create the directory where we will store the raw data.
                3. Save the raw data in the directory.
                4. Split the raw data into train and test set.
                5. Save the train and test set in the directory.
            '''

            # Reading the raw dataset as DataFrame.
            df = pd.read_csv('notebooks/data/stud.csv') 
            logging.info('Read the raw dataset as dataframe')

            # Now we have read the data we have to create the directory where we will store the raw data. We will use os.makedirs() to create the directory. We will use os.path.dirname() to get the directory name from the path. We will use exist_ok=True to avoid any error if the directory already exists.
            logging.info('Creating raw data directory')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('Saved raw data')

            logging.info('Initiating train test split')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Ingestion of the data is completed')

            return(self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    train_path, test_path= data_ingestion.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_path, test_path)