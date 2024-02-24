# Manual

## Index

### Current Playlist

Shows the playlist that songs are randomly selected from

### Select Playlist

Use drop down and 'Select' button to set the Current Playlist

### Set Play Conditions

1. Playtime seconds - The number of seconds a track play for
2. Pause Length (seconds)- The party button goes dark then take half a second to initialise on pressing. This adds additional darkness time.
3. Play full override - Overrides "Playtime Seconds" and plays tracks in full
4. Play whole playlist - Overrides playing one random tune and plays the whole playlist in random order

Press "Update" to set these settings

### Invite Party Ghost

1. Exorism Complete/Party Haunted toggle - sets whether the party button should randomly trigger by turning on and off the switch debounce

### Scene Control

1. Lights On/Lights Only toggle - sets whether the disco lights are on with music or only the lights come on
2. Music On/Music Only toggle - sets whether the music comes on with the disco lights or only the music comes on

## Track Management

### Upload Track

1. Name - Provide a memorable name for the track you upload
2. Mp3 file - select an mp3 file, only mp3 is supported at this time
3. Minutes & seconds - set the time in the track that the track should play from when triggered

Press "Upload" to upload a track, may take some time as it has to measure the bpm of the track

### Track List

A table of details about each track

1. Min & Sec- set the time in the track that the track should play from when triggere
2. Solo toggle - set to green and the track will be the only one selected from the playlist when the button is pressed. Blue is unset.
3. Play Whole Track toggle - "Using Play Time Settings" plays for the set number of play time seconds, "Using Whole Track" plays the whole track regardless of currently valid seconds of play time
4. Override global playtime toggle - "Using global play time" uses the master play time. "Using Track's Playtime" uses the track specific play time listed in the next column
5. Track playtime (seconds) - Set a track specific amount of playtime. Press 'Update' to update
6. BPM (HUE bulb sync) - Shows the track BPM calculated when uploaded. Can be altered and saved with the 'Update' button
7. Remove - Delete a track from the system

## Playlist Management

### Add New Playlist

1. Name - Provide a name for your playlist

Click "Add" to add a playlist to the system

### Remove Playlist

1. Dropdown - use this to select a playlist to delete from the system

Click "Delete" to remove the selected playlist. This will not remove the tracks that are associated with the playlist

### Assign Tracks To Playlists

1. Playlist & Track - use the dropdowns to select a track and a playlist to associate the track with

Click "assign" to add a track to a playlist, tracks can appear in multiple playlists

### Playlists

A listing of each playlist and the tracks current associated with them. Use the "Remove" button to remove a track from a playlist. Track will not be deleted.

## Smart Bulbs

### Party Time Brightness

1. Brightness - The global brightness that all lights should change to when the party button is pressed. 0-100

Click "Updated" to save or update this value

### Light Config

A listing of all lights that the system was able to discover and their possible settings

1. Name - name of the smart bulb, should start with "Name Stub" from the bridge settings (see below)
2. Primary RGB - Colour the bulb should switch when the party button is pressed. Values as (0 - 254) RGB, background shows colour setting
3. Secondary RGB - Second colour to use for "Fade Between" and "Alternate" colour modes. Values as (0 - 254) RGB, background shows colour setting
4. Change Interval - Lights change in tempo. 1 change on every beat, 2 change every 2 beats, 3 change every third beat etc...
5. 'Update button' - Click to update the Primary RGB, Secondary RGB and Interval settings
6. Primary Only toggle - Light changes to Primary RGB colour on party button press
7. Fade Between toggle - Light changes to Primary RGB colour on party button press then fades to secondary RGB during play time. If playtime is greater than 30 seconds it will fade back and forth
8. Alternate toggle - Light will alternate between Primary RGB and Secondary RGB colours on each interval
9. Randomise toggle - Light will change to a random colour on each interval
10. & Inc. Bri. toggle - Light colour randomisatiomn will also randomise brightness
11. Randomise intervale toggle - Whether a light changes on a given "beat" is randomised
12. Brightness Override toggle - "Use Global Value" uses the brightness set in Party Time Brightness, "Use Light Value" uses the per light brightness value
13. Brightness Value - The per light brightness value the light should take if the brightness toggle is on, value 0-100
14. 'Update button' - Updates the per light brightness value
15. 'Off?' - Set whether a light should turn off during the party button

### Bridge Settings

1. ip - The IP address of your Philips Hue bridge on your home network
2. User id - A valid app user id issued by your bridge by following the HUE developer instructions (https://developers.meethue.com/develop/get-started-2/)
3. Name stub - The name prefix string assigned to each light you want to control (use hue app to set light names)
4. Room - The hue 'room' that the party button should look for names lights in

For the first time, click 'RESET LIGHTS' to attach to the bridge and get a list of matching lights to appear on the 'Light Config' list. On subsequent presses it will reset all light settings.

## Disco Lights

### Configure Disco Light

1. Name - Name of a light of set of lights 
2. Pin - Control pin on the raspberry pi which controls the light
3. Light on toggle - Toggles whether the disco light should come on when the party button is pressed

### Disco Light List

1. Light Name - Name of a light of set of lights 
2. Pin ID - Control pin on the raspberry pi which controls the light
3. On toggle - Toggles whether the disco light should come on when the party button is pressed
3. Update button - update the settings to new value
4. Remove - remove the disco light
5. Add double-click and long press functionality - Can have different actions while music is or isn't playing

## Current installation location

http://192.168.0.233/