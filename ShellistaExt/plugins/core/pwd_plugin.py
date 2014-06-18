'''pwd:
returns the working directory name
'''
from .. tools.toolbox import pprint
import os

def main(line):
    """return working directory name"""
    print pprint(os.getcwd())
