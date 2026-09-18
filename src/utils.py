import os
import sys
import pandas as pd
import numpy as np
import joblib


from src.exception import CustomException
from src.logger import logging

def save_preprocessor_object(file_path, obj):
    """
    This function is responsible for saving the preprocessor object to a specified file path using joblib.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the preprocessor object to the specified file path
        joblib.dump(obj, file_path)
        logging.info(f"Preprocessor object saved at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)