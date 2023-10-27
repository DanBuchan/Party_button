# Installation instructions

## Dev mode
1. `workon` you party button venv
2. install requirements

``` bash
pip install -r requirements.txt
```

3. Initialise django
``` bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
4. Head to `127.0.0.1:8000/admin` and add a PlayTime record
5. Head to `127.0.0.1` and add some example tracks

### Install ffmpeg

``` bash
brew install ffmpeg
```
or

``` bash
sudo apt-get install ffpmeg
```

From here `play_random.py` will interact with the db to play tracks. `gpio.test.py` will recieve switch signals, control relays and play tracks


## Production mode

Will add methods for starting system as services under systemctl

1. Install apache
``` bash
sudo apt-get httpd
```
or OSX
``` bash
brew install httpd
```

2. Copy httpd.conf

``` bash
cp httpd.conf.pi /etc/httpd/conf
```
or OSX
``` bash
cp httpd.conf.osx /opt/homebrew/etc/httpd/httpd.conf
```

3. Start apache
``` bash
sudo systemctl enable httpd.service
sudo systemctl start httpd.service
```
or OSX
``` bash
sudo /opt/homebrew/opt/httpd/bin/httpd -D FOREGROUND
```

4. Start GPIO listening service

TBC


## TODO

1. write services, gpio service should send STDOUT to /dev/null