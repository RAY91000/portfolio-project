#!/bin/bash

# Démarrer le serveur VNC (en arrière-plan)
vncserver :1 -geometry 1280x720 -depth 24 -localhost no

# Redémarrer si déjà en cours
if [ $? -ne 0 ]; then
    rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1
    vncserver :1 -geometry 1280x720 -depth 24 -localhost no
fi

# Lancer SSH en mode foreground (pour que le conteneur ne meure pas)
exec /usr/sbin/sshd -D
