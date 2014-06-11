'''ssh:
Usage: 
    addhost save_name hostname user [password]
    connect save_name
    connect hostname user password
'''
from ssh import SSH

alias = []

def main(line):
    print line
    args = line.split()
    print ' '.join(args[1:])
    ssh = SSH()
    if len(args) == 0:
        print '''Usage: 
    addhost save_name hostname user [password]
    connect save_name
    connect hostname user password
    '''
        return
    if args[0] == 'addhost':
        ssh.addhost(line)
    elif args[0] == 'connect':
        ssh.connect(' '.join(args[1:]))
    else:
        print 'invalid commands'
        return
        
if __name__ == '__main__':
    main('connect rdr')
    
