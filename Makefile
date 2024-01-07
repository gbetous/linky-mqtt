run:
	python2 linky.py
setup:
	sudo pip2 install -r requirements.txt
	./setup.sh

status:
	systemctl --user status linky.service
