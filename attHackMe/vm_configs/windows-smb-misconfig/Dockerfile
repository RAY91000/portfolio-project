FROM debian:bullseye

RUN apt-get update && apt-get install -y samba && \
    mkdir -p /srv/smb/WorkShares/Ray.D /srv/smb/WorkShares/Raph.D && \
    echo "Voici des notes inutiles de Ray" > /srv/smb/WorkShares/Ray.D/worknotes.txt && \
    echo "FLAG{smb_misconfig_exposure}" > /srv/smb/WorkShares/Raph.D/flag.txt && \
    chmod -R 777 /srv/smb && \
    apt-get clean

COPY smb.conf /etc/samba/smb.conf

EXPOSE 445

CMD ["sh", "-c", "service smbd restart && tail -f /dev/null"]
