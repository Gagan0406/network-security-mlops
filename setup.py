'''
The setup.py file is an essential part fo packaging and distributing Python projects. it is used by setuptools
to define the configuration of project, such as its metadata, dependencies and more
'''
from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
   This function will return list of requirements 
    '''
    requirement_lst:List[str]=[]
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement != 'e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")
        return []
    return requirement_lst
setup(
    name="network-security-project",
    version="0.1.0",
    author="Gagan gupta",
    author_email="gagan04062005@gmail.com",
    description="A project for network security",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)