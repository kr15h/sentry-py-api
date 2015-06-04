#sentry-py-api
Python serial API for the Sentry Remote Power Manager. Use ./restapi.py to launch the server and access it by http://localhost:8080/a1/on and http://localhost:8080/a1/off

Before launching, make sure that the web.py module is installed. Install it with python-setuptools: sudo easy_install web.py

Use the following guide to figure out your serial port device name: [Using Minicom](https://help.ubuntu.com/community/Minicom)

## Launching on Boot
This has been tried on a Raspberry Pi 1 model B+ running Raspbian. You have to add the following line before the `exit 0` line in `/etc/rc.local`:
```
su - pi -c /home/pi/startup.sh &
```

Contents of `startup.sh`:
```
#!/bin/sh
sudo /home/pi/sentry-py-api/restapi.py
```

License: [MIT](LICENSE)
