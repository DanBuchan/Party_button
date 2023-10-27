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
sudo apt-get install apache2
sudo apt-get install ffmpeg
sudo apt-get install apache2-dev
```
or OSX
``` bash
brew install httpd
```

2. collect static assets

``` bash
cd Party_button/pb_ui
python manage.py collectstatic
```

3. Copy httpd.conf
``` bash
cp Party_button/httpd.conf.pi /etc/httpd/conf
```
or OSX
``` bash
cp Party_button/httpd.conf.osx /opt/homebrew/etc/httpd/httpd.conf
```

4. Start apache
``` bash
sudo systemctl enable apache2.service
sudo systemctl start apache2.service
```
or OSX
``` bash
sudo /opt/homebrew/opt/httpd/bin/httpd -D FOREGROUND
```

5. Start GPIO listening service

``` bash
cp party_button.service /etc/systemd/system/
systemctl enable party_button.service
systemctl start party_button.service
```

## TODO

1. Ensure service works