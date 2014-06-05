'''pwd:
returns the working directory name
'''
from tools.tools import pprint
def main(line):
    """return working directory name"""
    print pprint(os.getcwd())
