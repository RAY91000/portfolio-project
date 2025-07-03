#!/bin/bash
# vm_configs/windows-auth-challenge1/server.sh

while true; do
    echo "Waiting for connection on port 2121..."
    nc -lvkp 2121 -c '
    echo -n "Enter password: "
    read password
    if [ "$password" = "hunter2" ]; then
        cat /flag.txt
    else
        echo "Access denied"
    fi
    '
done
