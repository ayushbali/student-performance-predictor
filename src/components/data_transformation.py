import sys
import os
from dataclasses import dataclass

import pandas as pd 
import numpy as np


# from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_preprocessor_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "data_preprocessor.pkl")  


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is responsible for data transformation and returns a preprocessor object that can be used to transform the data.
        Transformations: 
            1. For numerical columns: Impute missing values with median and scale the data using StandardScaler.
            2. For categorical columns: Impute missing values with the most frequent value, apply OneHotEncoding, and scale the data using StandardScaler.
            3. Combine both numerical and categorical transformations into a single preprocessor object using ColumnTransformer.
            4. Return the preprocessor
        """

        try:
            # Define the numerical and categorical columns
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Define the numerical and categorical pipelines for data transformation
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            # Combine both numerical and categorical pipelines into a single preprocessor object
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        This function is responsible for initiating the data transformation process. It reads the train and test datasets, applies the preprocessor object to transform the data, and saves the preprocessor object to a specified file path. It returns the transformed train and test arrays along with the file path of the saved preprocessor object.
        """
        try:
            # Read train and test datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Get preprocessor object
            preprocessor_obj = self.get_data_transformer_object()

            target_column = "math_score"

            # Split into X and y for train and test datasets

            # Train dataset
            X_train_df = train_df.drop(columns=[target_column], axis=1)
            y_train_df = train_df[target_column]

            # Test dataset
            X_test_df = test_df.drop(columns=[target_column], axis=1)
            y_test_df = test_df[target_column]

            # Now that we have feature and targets for both train and test datasets, we can apply the preprocessor on them to transform the data

            X_train_arr = preprocessor_obj.fit_transform(X_train_df)
            X_test_arr = preprocessor_obj.transform(X_test_df)

            # COmbine the transformed features with the target variable to create final train and test arrays
            train_arr = np.c_[X_train_arr, np.array(y_train_df)]
            test_arr = np.c_[X_test_arr, np.array(y_test_df)]

            logging.info("Data transformation is completed")
            logging.info("Saving the preprocessor object")

            # Save the preprocessor_obj.pkl to the specified file path
            save_preprocessor_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessor_obj
            )
            logging.info("Preprocessor object saved successfully")
            
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
