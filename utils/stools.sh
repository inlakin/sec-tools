#! /bin/bash

# Secu tools, bash scripting

if [ "$1" == "" -o "$2" == "" ]; then
    echo "Usage: ./stools.sh [options] [network]"
    echo "Examples"
    echo "    ./stools.sh --dns-lookup 192.168.0"
    echo "    ./stools.sh --dns-reverse-lookup 192.168.0"
    echo "    ./stools.sh --ping-sweep 192.168.0"
else
    echo ""
    if [ "$1" == "--dns-lookup" ]; then
        echo "=== DNS Lookup ==="
        echo ""
        for x in `seq 1 254`; do
            host $2.$x | grep "name pointer"
        done
    elif [ "$1" == "--dns-reverse-lookup" ]; then
        echo "=== DNS Reverse Lookup ==="
        echo ""
        for x in `seq 1 254`; do
            dig -x $2.$x 
        done
    elif [ "$1" == "--ping-sweep" ]; then
        echo "=== Ping Sweep ==="
        echo ""
        for x in `seq 1 254`; do
            ping -c 1 $2.$x | grep "64 b" | cut -d" " -f4 | sed 's/.$//'
        done
    else
        echo "[*] Unknown argument"
        echo ""
    fi
fi

