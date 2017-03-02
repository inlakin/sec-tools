# Simple Port Scanner - Python

### Options

```
./portscanner.py -h

    Usage:       ./portscanner.py -d [destination] -p [start-end]
    Options:
                 -s          Stealth scan : SYN Scan + randomized source ports
                 -m [ipsrc]  Masquerade IP source with [ipsrc]
    
    Example:
                 ./portscanner.py -d 192.168.0.2 -p 1-1024 
                 ./portscanner.py -d 192.168.0.2 -p 1-1024 -s
                 ./portscanner.py -d 192.168.0.2 -p 1-1024 -m 192.168.0.3
                 ./portscanner.py -d 192.168.0.2 -p 1-1024 -s -m 192.168.0.3
```

## Self notes

### Flags description

* URG = 0x20
* ACK = 0x10
* PSH = 0x08
* RST = 0x04
* SYN = 0x02
* FIN = 0x01


### Todo :
    * Fixing host discovery 
    * Removing warning about ipv6
    * Multi threading / Multi processing
    * XMAS Scan ()