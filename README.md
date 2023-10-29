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
sudo apt-get install libapache2-mod-wsgi-py3
ENABLE SSH
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
cp Party_button/000-deafult.conf.pi /etc/apache2/available-sites
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

DON'T FORGET IN THE DJANGO APPLICATION THAT ALLOWED_HOSTS MUST REFLECT THE IP OF THE MACHINE

5. Start GPIO listening service

``` bash
sudo cp party_button.service /etc/systemd/system/
sudo systemctl enable party_button.service
sudo systemctl start party_button.service
```

## TODO

1. "Play All" added to model not done by frontend/gpio player
2. Add playlist assignment and safe deleting of playlist and associations 
3. Have frontend/gpio obey play full playlist and obey playlist selection
4. Spotify integration
5. Colour bulb 
    - Philips HUE (£70-90) - https://github.com/Q42/hue-libs#python
    - Sylvania smart+ integration (can't find UK, maybe same as OSRAM smart) - pywemo pywemo
    - LIFX (£45-60) - lifxlan package, https://github.com/mclarkk/lifxlan
    - FLUX WIFI - https://github.com/Danielhiversen/flux_led
    - lepro pack of 4 (£29)
