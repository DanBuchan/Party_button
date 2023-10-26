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

## TODO

1. write services
2. switch from pygame to pydub
3. better handle full length of mp3
4. fast fade at end
5. probably should fast fade in the track and then turn off mains and turn on discos
