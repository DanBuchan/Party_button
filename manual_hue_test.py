import urllib.request
import ssl, json, pprint
import time

def put(url, content, context):
    """
    Do a HTTP PUT request with given content as payload.
    put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":true}')
    """
    req = urllib.request.Request(url=url,
        data=content.encode('UTF-8'), method='PUT')
    f = urllib.request.urlopen(req, context=context)
    print(f.status, f.reason, f.read())
    
def get_json(url, context):
    """Do a HTTP GET request and return response parsed as JSON.
    get_json(f'https://{ip}/api/{user}/lights')
    """
    # print(url)
    req = urllib.request.Request(url=url, method='GET')
    f = urllib.request.urlopen(req, context=context)
    #print(f.status, f.reason)
    return json.loads(f.read())

def set_initial_scene(ip, user, initial_lights, context):
    url=f'https://{ip}/api/{user}/scenes'

    scenes = get_json(f'https://{ip}/api/{user}/scenes', context)
    modify = False
    scene_id = None
    for id in scenes:
        if scenes[id]['name'] == 'initialscene':
            modify=True
            scene_id=id
        # req = urllib.request.Request(url=url+"/"+id, method='DELETE')
        # f = urllib.request.urlopen(req, context=context)
    
    payload = '{"name": "initialscene", "lights": ['
    for light_id in initial_lights:
        payload += f'"{light_id}", '
    payload = payload[:-2]+'], '
    payload += '"lightstates": {'
    lightstates = ''
    for light_id in initial_lights:
        bri=initial_lights[light_id]['state']['bri']
        hue=initial_lights[light_id]['state']['hue'] 
        sat=initial_lights[light_id]['state']['sat']
        lightstates += f'"{light_id}": {{"bri": {bri}, "sat": {sat}, "hue": {hue}}}, '
    payload += lightstates[:-2]+' } }'
    # print(payload)
    if modify:
        req = urllib.request.Request(url=url+"/"+scene_id,
        data=payload.encode('UTF-8'), method='PUT')
        f = urllib.request.urlopen(req, context=context)
        # print("MODIFY", f.status, f.reason, f.read())
    else:
        payload = '{"name":"initialscene", "recycle": false, "lights":["4"],"type":"LightScene"}'
        req = urllib.request.Request(url=url,
        data=payload.encode('UTF-8'), method='POST')
        f = urllib.request.urlopen(req, context=context)
        # print("CREATE", f.status, f.reason, f.read())
    
    scenes = get_json(f'https://{ip}/api/{user}/scenes', context)
    for id in scenes:
        if scenes[id]['name'] == 'initialscene':
            return(id)


def get_initial_colours(lights):
    initial_settings = {}
    # pprint.pprint(lights)
    try:
        for light in lights:
            initial_settings[light["name"]] = [light["state"]["hue"],
            light["state"]["sat"], light["state"]["bri"] ]
    except Exception as e:
        print("Unable to get initial light information:" + str(e))
    return(initial_settings)

def get_group_id(room_name, groups):
    for id in groups:
        print(id, room_name, groups[id]['name'])
        if room_name == groups[id]['name']:
            return id
    return None

def dip_lights(group_id, initial_scene_id, context):
    setting_data = '{"bri":30, "transitiontime": 1}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    time.sleep(0.2)
    setting_data = f'{{"scene":"{initial_scene_id}", "transitiontime": 1}}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    

user = 'GIRjjwwRjU7If6DYHwnzY2L6qxMOJnimt4Femjvd'
ip = '192.168.0.168'
name_stub = "PB spot"
room_name = "Radha kitchen"
context = ssl._create_unverified_context()

initial_light_state = get_json(f'https://{ip}/api/{user}/lights', context)
initial_scene_id = set_initial_scene(ip, user, initial_light_state, context)
groups = get_json(f'https://{ip}/api/{user}/groups', context)
group_id = get_group_id(room_name, groups)

pp = pprint.PrettyPrinter(indent=4)

start = time.time()
pb_lights = dip_lights(group_id, initial_scene_id, context)
end = time.time()
print(end-start)
