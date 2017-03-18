# Pynetcat : Python Netcat

In progress.

## Usage 
    
    ./pynetcat.py -d 192.168.0.1 -p 999
    ./pynetcat.py -d 192.168.0.1 -p 999 -l -c
    ./pynetcat.py -d 192.168.0.1 -p 999 -l -e="cat /etc/passwd"


## Options

    -l      listen
    -e      execute [command] upon receiving a connection
    -c      initialize a bind shell


A bind shell allows the transmission of a shell from the victim machine to the attack machine. More specifically, it instructs the target to open a command shell on a local port and then listen on this specific port for incoming connection. Upon receiving connection, the attacker's machine will be prompted with the shell.
However, the effectiveness of this attack is unlikely to succeed due to common firewall configuration which are blocking traffic on random port. 

