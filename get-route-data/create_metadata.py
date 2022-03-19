__version__ = '1.5.0'
__author__ = 'Jacob Benjamin Menge'
__copyright__ = '© Hochschule Bremerhaven'
__status__ = 'Production'
__github__ = 'https://github.com/ProjectPepperHSB/Backend-Services.git'

# =============================================== D E S C R I P T I O N ================================================

'''
    create_metadata.py
    ===================================
    This script creates a dataset in java object notation. The content of the data is information about the paths 
    between rooms within the university of applied sciences bremerhaven.
    
    The following attributes are described in the data:
    
    - Type of route
        For each route description there are two different ways to reach the destination. In each case, we create a 
        barrier-free route and an ordinary route or a route that can be reached quickly.
        
    - Video path 
        This parameter represents the direct link to the corresponding data with the associated spatial information. 
        In this way, we can determine the appropriate video with the correct route description as precisely as possible.
        
    - Location
        The location is a short description in which house and which floor the room is located. Such a location 
        description would be, for example, "House C ground floor". With this description Pepper can provide the user 
        with additional information for verbal interaction.
        
    - Distance
        The distance is the distance from the starting point of the directions to the destination. We use metres as the 
        unit and round this up to whole metres for better comprehensibility.
        
    - Duration 
    The duration is given in minutes. It describes the time needed from the starting point to the destination, based on 
    the average walking speed.
    
    
    ----- E X A M P L E -----
        
    Start the fetch of new data .. 
    Request was Success!
    HTTP status code is: 200. 
    Request was Success!
    HTTP status code is: 200. 
    Room: C006
    Location: Haus C - Untergeschoss
    Distance "M0000": 239, Distance "M0001": 402
    Distance "M0000": 3, Distance "M0001": 8
    Status of created JSON data: {
        "C006": {
            "M0000": {
                "video_path": "L00P1133-L01P1056-M0000.mp4",
                "location": "Haus C - Untergeschoss",
                "distance": "239",
                "time": "3"
            },
            "M0001": {
                "video_path": "L00P1133-L01P1056-M0001.mp4",
                "location": "Haus C - Untergeschoss",
                "distance": "402",
                "time": "8"
            }
        }
    }
    Number of generated Data 1
    (...)
    create route_data
    Creating the JSON file was successful!
    
    ----- N O T E S -----
    
    It should be noted that the json file created is stored in the directory in which the script is executed. 
    In addition, an internet connection is of course necessary to execute the script correctly.
    
    ----- A U T H O R S H I P - A N D - C O N T R I B U T I O N -----
    @date: 2022, January 23.
    @author: Jacob Benjamin Menge
    @email: mengejacob@gmail.com
    @github: https://github.com/ProjectPepperHSB/Backend-Services
'''

# ================================================ I M P O R T S =======================================================

import json
import requests
import math
import re
import PySimpleGUI as fr

# ================================================== S E T U P =========================================================

# request to get meta information for videos from 3d-Berlin API
data = requests.get(
    'https://services.guide3d.com/menu/cors/index.php?project=100011&language=de&set=set_01&force-display=false').json()

# temp struct to fill data into it
new_json_struc = {}

# startpoint id
startpoint = 'L00P1133'

# Project id | Bremerhaven project id: 100011
project = '100011'

# directory for the json file
directory = ""

json_name = ""

# ==================================================== G U I ===========================================================

# set colors for the windows
fr.theme('Dark')

# make a short text window to describe the skript in GUI
textwindow = [
    [fr.T(
        "This script creates a dataset in java object notation. The content of the data is information about the paths"
        " between rooms within the university\nof applied sciences bremerhaven. please note that you do not specify the"
        " file extension <.json>.")]
]

# initialize progressbar
progressbar = [
    [fr.ProgressBar(500, orientation='h', size=(75, 20), key='progressbar')]
]

# initialize the windows to show the output (printouts)
outputwin = [
    [fr.Output(size=(60, 30))],
]

# Define GUI Layout Window
layout = [
    [fr.Frame('Info about this program', layout=textwindow, size=(837, 70))],
    [fr.T("")],
    [fr.Text("Choose a filename: "), fr.Input(key="-IN3-", size=76, change_submits=True), fr.Button("Submit ")],
    [fr.Text("Choose a folder:     "), fr.Input(key="-IN2-", size=76, change_submits=True), fr.FolderBrowse(key="-IN-"),
     fr.Button("Submit")],
    [fr.Frame('Progress', layout=progressbar)],
    [fr.Frame('Output', layout=outputwin), fr.MLine(key='-ML1-' + fr.WRITE_ONLY_KEY, size=(50, 31))],
    [fr.Submit('Start'), fr.Cancel()]
]

# set some windows setting for the Frame
window = fr.Window('Downloading Metadata for 3D-Navigation                                                             '
                   '                                          © Hochschule Bremerhaven', layout)
progress_bar = window['progressbar']


# ============================================== F U N C T I O N S =====================================================

# generate request for video metadata
def get_request(mode: str, project: str, startpoint: str, endpoint: str):
    """
    :param mode: mode for disabled access | disabled access mode True:  M0001 | disabled access mode False:  M0000
    :param project: the project used by 3Dberlin
    :param startpoint: start point from where the route should begin
    :param endpoint: the end point at which the route ends (the point to which the user wants to go)
    :return: returns defined request as an object
    """

    # define request to get the data
    url = f'https://services.guide3d.com/route/cors/index.php?project=' \
          f'{project}&start={startpoint}&end={endpoint}' \
          f'&mode={mode}&redirect=duration&format=none'

    # start request
    r = requests.get(url, allow_redirects=True)

    # check that the HTTP status code 200 indicates OK, which means that the request was successful.
    if r.status_code == 200:
        print('Request was Success!')
        print(f'HTTP status code is: {r.status_code}. ')
    else:
        print('something went wrong!')
        print(f'HTTP status code is: {r.status_code}')
    return r


# rounding up the floating point numbers
def round_up_numbers(num: int):
    return math.ceil(num)


# Convert seconds into minutes
def sec_to_min(num: int):
    return (num / 60)


# Filter out the incorrectly formatted string characters
def filter_char_location(string):
    string = str(string)
    characters = "[']"
    for x in range(len(characters)):
        string = string.replace(characters[x], "")
    replace = "-"
    string.replace(replace, "im")
    return string


# Filtering out the incorrectly formatted strings for the room names
def filter_char_wrong_Roum(string):
    string = str(string)
    string = re.sub("T ", "T", string)
    return string


# write data into json
def write_json_down(json_data, directory, json_name):
    print(f'create {json_name} in {directory}')
    with open(f'{directory}/{json_name}.json', 'w') as outfile:
        json.dump(json_data, outfile)
    print('Finish! Creating the JSON file was successful!')


# =================================================== M A I N ==========================================================

if __name__ == '__main__':

    count = 0

    # start GUI Windows
    while True:
        event, values = window.read(timeout=10)

        if event == "Submit":
            directory = values["-IN-"]
            print(f'"{directory}" is set as target directory')

        if event == "Submit ":
            json_name = values["-IN3-"]
            print(f'"{json_name}" is set as name')

        # close window if cancel event (button is triggered)
        if event == 'Cancel' or event is None:
            break

        # start button activated
        elif event == 'Start':

            # iterate over used json data
            for d in data['data']['list']:
                print('Start the fetch of new data .. ')
                count += 1
                endpoint = d["point"]
                video_name = f'{startpoint}-{endpoint}-'
                video_path = f'{video_name}'

                # send request for normal path
                r_M0 = get_request(mode='M0000',
                                   project=project,
                                   startpoint=startpoint,
                                   endpoint=endpoint)

                # send request for Accessible path
                r_M1 = get_request(mode='M0001',
                                   project=project,
                                   startpoint=startpoint,
                                   endpoint=endpoint)

                # Initialise var for the room name and filter the wrong chars out of the string to avoid errors later on
                room_name = filter_char_wrong_Roum(string=d['name'])
                print(f'Room: {room_name}')

                # Initialise a variable for the location and filter the wrong characters from the string
                location = filter_char_location(string=d['location'])
                print(f'Location: {location}')

                # Initialise var for the distance and round up the floating point number to make it easier to call up.
                distance_M0 = round_up_numbers(num=r_M0.json()['distance'])
                distance_M1 = round_up_numbers(num=r_M1.json()['distance'])
                print(f'Distance "M0000": {distance_M0},'
                      f' Distance "M0001": {distance_M1}')

                # Initialise var for duration and divide by 60 to get minutes, then round up the number of minutes to
                # get a better result.
                duration_M0 = round_up_numbers(num=sec_to_min(r_M0.json()['duration']))
                duration_M1 = round_up_numbers(num=sec_to_min(r_M1.json()['duration']))
                print(f'Duration "M0000": {duration_M0},'
                      f' Duration "M0001": {duration_M1}')

                # define the json structure to add to the whole json
                tmp_json_struc = {f'{room_name}': {'M0000': {'video_path': f'{video_path}M0000.mp4',
                                                             'location': f'{location}',
                                                             'distance': f'{distance_M0}',
                                                             'time': f'{duration_M0}'},
                                                   'M0001': {'video_path': f'{video_path}M0001.mp4',
                                                             'location': f'{location}',
                                                             'distance': f'{distance_M1}',
                                                             'time': f'{duration_M1}'}}}

                # add new data to dictonary and define the json data structure
                new_json_struc.update(tmp_json_struc)
                progress_bar.UpdateBar(current_count=count + 1)

                # print(f'Status of created JSON data: {json.dumps(tmp_json_struc, indent=4)}')
                print(f'Number of generated Data {count}')
                print(f'Adding Data was successful!')
                print('=================================================')
                window['-ML1-' + fr.WRITE_ONLY_KEY].print(json.dumps(obj=tmp_json_struc,
                                                                     indent=4))

            # save generated json data
            write_json_down(json_data=new_json_struc,
                            directory=directory,
                            json_name=json_name)

    # close window
    window.close()
