#!/bin/bash

# Supprimer les fichiers VNC bloquants
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1 /root/.vnc/*.pid

# Lancer VNC et SSH
vncserver :1 -geometry 1280x720 -depth 24
/usr/sbin/sshd -D
