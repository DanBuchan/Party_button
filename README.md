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

Will add methods for starting system as services under systemctl. 

REQUIRES 64BIT OS

1. Install requirements
``` bash
sudo apt-get install apache2
sudo apt-get install apache2-dev
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install midori
sudo apt-get install bpm-tools
sudo apt-get install libsox-fmt-mp3
ENABLE SSH
```
or OSX

``` bash
brew install httpd
```

2. Install requirements

On pi you could/should comment out mod-wsgi

``` bash
python -m venv pb_venv
source pb_venv/bin/activate
pip install -r requirements.txt
```

3. collect static assets

``` bash
cd Party_button/pb_ui
python manage.py collectstatic
```

4. Copy httpd.conf
``` bash
cp Party_button/000-default.conf.pi /etc/apache2/sites-available
```
or OSX
``` bash
cp Party_button/httpd.conf.osx /opt/homebrew/etc/httpd/httpd.conf
```

5. Start apache
``` bash
sudo systemctl enable apache2.service
sudo systemctl start apache2.service
```
or OSX
``` bash
sudo /opt/homebrew/opt/httpd/bin/httpd -D FOREGROUND
```

DON'T FORGET IN THE DJANGO APPLICATION THAT ALLOWED_HOSTS MUST REFLECT THE IP OF THE MACHINE

6. Start GPIO listening service

``` bash
sudo cp party_button.service /etc/systemd/system/
sudo systemctl enable party_button.service
sudo systemctl start party_button.service
```

## TODO

1. refactor django views to correctly use mixins and not have all those single function classes
2. Spotify integration (hmmmm)