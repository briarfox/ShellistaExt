#!/usr/bin/python

import paramiko
#from ssh import SSHSession
import cmd,sys,getpass,os
from ConfigParser import SafeConfigParser

package_directory = os.path.dirname(os.path.abspath(__file__))

class SSH:
    """ Simple shell to run a command on the host """

    prompt = 'ssh> '

    def __init__(self):
       # cmd.Cmd.__init__(self)
        self.config = SafeConfigParser()
        self.config.read(os.path.join(package_directory,'hosts.ini'))
        self.host = []
        self.cwd = ''


    def addhost(self, line):
        """add_host 
        Add the host to the host list"""
        args = line.split()
        #check that there is a correct number of args
        if len(args) < 3 or len(args)>4:
            return
        
        self.config.add_section(args[0])
        self.config.set(args[0],'host',args[1])
        self.config.set(args[0],'user',args[2])
        if len(args) == 4:
            self.config.set(args[0],'password',args[3])
        else:
            self.config.set(args[0],'password','')
        with open('hosts.ini', 'w') as fp:
            self.config.write(fp)


    def connect(self, list):
        """Connect to all hosts in the hosts list"""
        
        args = list.split()

        
        if len(args) == 1:
            for section in self.config.sections():
                if section == args[0]:
                    self.host = [self.config.get(section,'host'),self.config.get(section,'user')]
                    if self.config.get(section,'password') == '':
                        passwd = getpass.getpass('Password: ')
                        self.host.append(passwd)
                    else:
                        self.host.append(self.config.get(section,'password'))
        else:
            self.host = [args[0],args[1],args[2]]
        
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
            self.client.connect(self.host[0], 
                    username=self.host[1], 
                    password=self.host[2])
            _,err = self.runCommand('ls')
            self.sign = '&' if err else ';'
            self.console()
        except Exception,e:
            print 'Error connecting to server %s' % self.host[0]
        
        
    def runCommand(self,command):
        #print self.client.exec_command(command)
        stdin, stdout, stderr = self.client.exec_command(command)
        stdin.close()
        str = ''
        err = ''
    
        for line in stdout.read().splitlines():
            str += line + '\n' 
        for line in stderr.read().splitlines():
            err += line + '\n'
        if err == '':
            err = False
        return str,err 
    
    def setPath(self,path):
        if path == "..":
            self.cwd = os.path.dirname(self.cwd)
        elif self.cwd == '':
            self.cwd = path
        else:
            self.cwd = os.path.join(self.cwd, path)
        print self.cwd
        

    def console(self):
        """run 
        Execute this command on all hosts in the list"""
        
        while True:
            command = raw_input('command>')
            args = command.split()
            print args
            if args[0] == 'quit':
                print 'leaving console'
                self.client.close()
                break
                print 'didnt break'
                
            if args[0]=='cd':
                self.setPath(args[1])
            else:
                
                com = 'cd '+ self.cwd + ' '+ self.sign + ' ' +command
                str,err =  self.runCommand(com)
                print str
                if err: print err
        self.client.close()
        
                
                
        
          

if __name__ == '__main__':
    ssh = SSH()
    #ssh.connect()
    
    #ssh.console()

