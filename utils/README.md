# Bash scripting : sec tools


### DNS Lookup

Perform a DNS lookup on a network

``` 
./stools.sh --dns-lookup 192.168.0
```
will scan the following host 192.168.0.[1-254]

### DNS Reverse Lookup

Perform a DNS reverse lookup on a network

```
.stools.sh --dns-reverse-lookup 192.168.0
```
will scan the following host 192.168.0.[1-254]

### Ping sweep

Check the alive hosts on a given network

```
./stools.sh --ping-sweep 192.168.0
```
will scan the following host 192.168.0.[1-254]



In order to output the results in a file for further use, use the `>` redirection

```
./stools.sh --ping-sweep 192.168. > ping.txt
```
