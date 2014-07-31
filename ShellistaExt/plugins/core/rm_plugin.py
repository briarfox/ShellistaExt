'''rm:
remove one or more files/directories
usage: rm [-r] file_or_dir [...]

options:
    -r    Flag to remove directories
'''
from .. tools.toolbox import bash,pprint
import os,shutil

alias = ['remove']

def main(self, line):
    """remove one or more files/directories"""
    args = bash(line)
    print args
    if args is None:
      return
    elif (len(args) < 1):
      print "rm: Usage: rm file_or_dir [...]"
    else:
      for filef in args:
        full_file = os.path.abspath(filef).rstrip('/')
        if not os.path.exists(filef):
          print "! Skipping: Not found -", pprint(filef)
          continue
        if (os.path.isdir(full_file)) and args[0]=='-r':
          try:
            shutil.rmtree(full_file, True)
            if (os.path.exists(full_file)):
              print "rm: %s: Unable to remove" % pprint(filef)
          except Exception:
            print "rm: %s: Unable to remove" % pprint(filef)
        elif args[0] != '.':
          try:
            os.remove(full_file)
          except Exception:
            print "rm: %s: Unable to remove" % pprint(filef)
