#/bin/bash

SYSTEMD_USER=~/.config/systemd/user
mkdir -p $SYSTEMD_USER

SERVICE=linky.service

cat << EOF > $SYSTEMD_USER/$SERVICE
[Unit]
Description=Linky 

[Install]
WantedBy=default.target

[Service]
ExecStart=/home/guillaume/linky/.venv/bin/python3 /home/guillaume/linky/tic.py
WatchdogSec=3600
Restart=always


EOF

systemctl --user daemon-reload
systemctl --user enable $SERVICE
systemctl --user restart $SERVICE

# To keep service while user is not logged in
#sudo loginctl enable-linger guillaume 

systemctl --user status $SERVICE
