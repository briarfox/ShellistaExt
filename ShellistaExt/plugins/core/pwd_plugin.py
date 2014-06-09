'''pwd:
returns the working directory name
'''
from .. tools.toolbox import pprint
def main(line):
    """return working directory name"""
    print pprint(os.getcwd())
