run:
	.venv/bin/python3 tic.py

status:
	systemctl --user status linky.service

test-serial:
	screen /dev/ttyUSB1 9600,cs7,parenb,-parodd,-cstopb
