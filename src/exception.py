from os import error
import re
import sys

from src.logger import logging

def error_message(error, error_detail:sys):
    '''
    This function is used to get the error message and the line number where the error occurred.
    '''
    _, _, tb = error_detail.exc_info() # returns a tuple of three values: (type, value, traceback)
    error_message = f'Error occurred in script: {tb.tb_frame.f_code.co_filename} at line number: {tb.tb_lineno}\nError message: {str(error)}'

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message