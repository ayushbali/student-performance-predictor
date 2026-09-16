from tkinter import E
from typing import List
from setuptools import find_packages, setup
import os

EOF = '-e .'

def get_requirements(file_path: str)-> List[str]:
    '''
    This function will return the list of requirements mentioned in the requirements.txt file
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if EOF in requirements: 
            requirements.remove(EOF)

    return requirements

setup(
    name='student-performance-prediction',
    version='0.0.1',
    author='Ayush',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
) 