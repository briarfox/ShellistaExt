import os
import cmd
import shlex
import importlib

# Credits
#
# The python code here was written by pudquick@github and modified by briarfox@github
#
# License
#
# This code is released under a standard MIT license.
#
#	Permission is hereby granted, free of charge, to any person
#	obtaining a copy of this software and associated documentation files
#	(the "Software"), to deal in the Software without restriction,
#	including without limitation the rights to use, copy, modify, merge,
#	publish, distribute, sublicense, and/or sell copies of the Software,
#	and to permit persons to whom the Software is furnished to do so,
#	subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be
#	included in all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#	BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#	ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
 
# You can skip over reading this class, if you like.
# It's an implementation of mine of the bash parser in pure python
# This has advantages over shlex, glob, and shlex->glob in that it expects
# the strings to represent files from the start.


 
class Shellista(cmd.Cmd):
  
  def __init__(self):
    self.did_quit = False
    self.cmdList = ['quit','exit','logoff','logout',]
    #self._bash = BetterParser()
    #self._bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')
    for file in os.listdir(os.path.join(os.curdir,'plugins')):
      (path, extension) = os.path.splitext(file)
    
    
      if extension == '.py' and path != '__init__'and '_plugin' in path:
        try:
          lib = importlib.import_module('plugins.'+path)
          name = 'do_'+path.lower().replace('_plugin','')
          if self.addCmdList(path.lower()):
            setattr(Shellista, name, self._CmdGenerator(lib.main))
      
          try:
            for a in lib.alias:
              #pass
              if self.addCmdList(a):
                parent = path.lower().replace('_plugin','')
                setattr(Shellista,'do_' + a.lower(),self._aliasGenerator(getattr(self,name)))
                setattr(Shellista,'help_'+a.lower(),self._HelpGenerator('Alias for: %s. Please use help on %s for usage.' % (parent,parent)))
              
          except (ImportError, AttributeError) as desc:
            pass
            
              
              
          if lib.__doc__:
            setattr(Shellista, 'help_' + path.lower().replace('_plugin',''), self._HelpGenerator(lib.__doc__))
        except (ImportError, AttributeError) as desc:
          print(desc)
 
    cmd.Cmd.__init__(self)
    os.chdir(os.path.expanduser('~/Documents'))
    self.getPrompt()

  def bash(self, argstr):
    try:
      #print self._bash.parse('. ' + argstr)[1:]
      return self._bash.parse('. ' + argstr)[1:]
    except SyntaxError, e:
      print "Syntax Error: %s" % e
      return None
 
  def _CmdGenerator(self,function):
    def CmdProxy(self, line):
      #args = [name]
      #args.extend(shlex.split(line))
      function(line)
      self.getPrompt()
 
    return CmdProxy
 
  def _HelpGenerator(self, help):
    def HelpProxy(self):
      print(help)
 
    return HelpProxy
    
  def _aliasGenerator(self,func):
  
    def aliasProxy(self,line):
      
      func(line)
    return aliasProxy
    
  def do_quit(self,line):
    self.did_quit = True
  def do_exit(self,line):
    self.did_quit = True
  def do_logout(self,line):
    self.did_quit = True
  def do_logoff(self,line):
    self.did_quit = True
  def postcmd(self,stop,line):
    return self.did_quit
    
  def addCmdList(self,name):
    if name in self.cmdList:
      print 'Conflict: Command %s already in use.' % name
      return False
    else:
      self.cmdList.append(name)
      return True
    
      
      
      
      
  
    
  def getPrompt(self):
    prompt = os.path.relpath(os.getcwd(),os.path.expanduser('~'))
    if prompt == '.':
      self.prompt = '</>:'
    else:
      self.prompt = '<'+prompt + '>:'

  def emptyline(self):
      pass


               
shell = Shellista()
shell.cmdloop()

