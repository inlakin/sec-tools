# Pynetcat : Python Netcat

In progress.

## Usage 
    
    ./pynetcat.py -d 192.168.0.1 -p 999
    ./pynetcat.py -d 192.168.0.1 -p 999 -l -c
    ./pynetcat.py -d 192.168.0.1 -p 999 -l -u=c:\target.exe
    ./pynetcat.py -d 192.168.0.1 -p 999 -l -e="cat /etc/passwd"


## Options

    -l      listen
    -e      execute [file] upon receiving a connection
    -b      initialize a bind shell
    -r      initialize a reverse shell
    -u      upload a file upon receiving a connection

