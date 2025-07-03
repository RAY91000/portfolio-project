FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    vsftpd \
    net-tools \
    sudo && \
    useradd -m ftpuser && \
    echo "ftpuser:ftppass" | chpasswd && \
    mkdir -p /home/ftpuser/ftp/files && \
    chown nobody:nogroup /home/ftpuser/ftp && \
    chmod a-w /home/ftpuser/ftp && \
    echo "FLAG{ftp_password_protected_flag}" > /home/ftpuser/ftp/files/flag.txt

COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 2121

CMD [ "sleep", "infinity" ]
