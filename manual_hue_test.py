import urllib.request
import ssl, json, pprint
import time

context = ssl._create_unverified_context()

def put(url, content):
    """
    Do a HTTP PUT request with given content as payload.
    put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":true}')
    """
    req = urllib.request.Request(url=url,
        data=content.encode('UTF-8'), method='PUT')
    f = urllib.request.urlopen(req, context=context)
    print(f.status, f.reason)
    
def get_json(url):
    """Do a HTTP GET request and return response parsed as JSON.
    get_json(f'https://{ip}/api/{user}/lights')
    """
    # print(url)
    req = urllib.request.Request(url=url, method='GET')
    f = urllib.request.urlopen(req, context=context)
    #print(f.status, f.reason)
    return json.loads(f.read())


def get_sorted_light_list(lights, name_stub):
    light_list = [None] * len(lights)
    light_ids = []
    try:
        for light_id in lights:
            if name_stub in lights[light_id]['name']:
                light_ids.append(light_id)
                bits = lights[light_id]['name'].split()
                light_list[int(bits[-1])-1] = lights[light_id]
    except Exception as e:
        print("Couldn't get live light list: "+str(e))
    return light_list, light_ids

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

def dip_lights(group_id, lights_ids):
    setting_data = '{"bri":30, "transitiontime": 1}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data)
    time.sleep(0.2)
    setting_data = '{"bri":254, "transitiontime": 1}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data)
    

user = 'GIRjjwwRjU7If6DYHwnzY2L6qxMOJnimt4Femjvd'
ip = '192.168.0.168'
name_stub = "PB spot"
room_name = "Radha kitchen"

lights = get_json(f'https://{ip}/api/{user}/lights')
groups = get_json(f'https://{ip}/api/{user}/groups')
group_id = get_group_id(room_name, groups)

pp = pprint.PrettyPrinter(indent=4)   

start = time.time()
pb_lights, light_ids = get_sorted_light_list(lights, name_stub)
end = time.time()
print(end-start)
pp.pprint(pb_lights)

start = time.time()
pb_lights = get_initial_colours(pb_lights)
end = time.time()
print(end-start)

start = time.time()
# pb_lights = dip_lights(group_id, light_ids)
end = time.time()
print(end-start)
