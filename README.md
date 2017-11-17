# iot-raspberry
This project includes:

  - Raspberry Pi GPIO sensors
  - AWS IoT synchronization
  - Django webserver


Get Started:
  
How to use?

1) Start listening to orders and reporting sensor's status to control center on Raspberry Pi:
	run: python3 start_rpi.py

2) Start control center on server side:
	run: python3 start_control.py
	
3) Start Django webserver for UI control:
	switch to dcha/webserver directory, then
	run: python3 manage.py runserver 0:8001

