#!/usr/bin/env python3
import pyfiglet
banner = pyfiglet.figlet_format("PORT DISCOVER")
print(banner)

#python3 port_discover.py input.txt output.txt

def help():
    print('command : python3 port_discover.py input.txt output.txt')
    print('        - input.txt  : Name of input file that contains list of domains(one on each line)')
    print('        - output.txt : Output file name')    
    print('-h help : to be used for help menu')

def create_domain_list(fname):
    dlist = []
    try:
        with open(fname) as f:
            while True:
                e = f.readline().strip()
                if e == '': break
                dlist.append(e)
    except:
        print('Input File does not exist!!')
        return False            
    return dlist

def discover(target):
    import socket
    try:
        target = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        return None
    live_ports = []
    socket.setdefaulttimeout(1)
    for port in range(1,100):	
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        try:
            result = s.connect((target,port))
            if result == None:
                live_ports.append(port)
            s.close()
        except socket.timeout:pass
    return live_ports

import sys,socket
if len(sys.argv) != 3:
    help()
    sys.exit(0)

targets = create_domain_list(sys.argv[1])
if targets == False:sys.exit(0)
#sys.argv[2] output.txt

from multiprocessing import Pool

try:
    pool = Pool()
    result = pool.map(discover, targets)
    #print(result)
    txt = ''
    for i in range(len(result)):
        txt += '----------------------------------------------------------------\n'
        txt += 'domain : '+targets[i]+' | ip : ' + socket.gethostbyname(targets[i])
        txt += '\n----------------------------------------------------------------\n'
        txt += '{:8} status'.format('port')  + '\n' 
        for j in result[i]:
            txt += '{:8} Open\n'.format(str(j))
        txt += '\n\n\n'
    if sys.argv[2][0] == '-':
        name = sys.argv[2][1:]
    elif sys.argv[2][0] == '--':
        name = sys.argv[2][2:]
    else:
        name = sys.argv[2]
    
    with open('Output/'+name,'w') as f:
        f.write(txt)
    print('Output is saved in /Output/{}.'.format(name))
except KeyboardInterrupt:
		print("\n Exitting Program !!!!")
		sys.exit()


















