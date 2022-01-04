
__version__ = "1.0"
__author__      = "Benjamin Thomas Schwertfeger"
__copyright__   = "Benjamin Thomas Schwertfeger"
__email__ = "development@b-schwertfeger.de"
__credits__ = ["Kristian Kellermann", "Jacob Menge"]
__status__ = "Production"

# ----- D E S C R I P T I O N ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

'''
    create_dummy_conversation_data.py
    ===================================

    This script is used to randomly generate data that is sent to a web application via API. 
    This data contains dummy information about conversations between humans and the university robot pepper. 
    
    ----- A R G U M E N T S -----    
    required arguments: None

    optional arguments:
        -h, --help            show help message and exit
        -n                    number of datasets to generate and send | default: 1000
        -p, --prod            send to https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/collector instead to http://127.0.0.1:3000/docker-hbv-kms-http/collector | default: False

    ----- E X A M P L E -----
    ╰─ python3 create_dummy_conversation_data.py --prod -n 250
    2022-01-04 09:51:25 create_dummy_conversation_data,line: 137     INFO | Sending 250 dummy datasets to https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/collector
    100%|████████████████████████████████████████████████████████████████████████████████████████| 250/250 [00:33<00:00,  7.49it/s]
    2022-01-04 09:51:59 create_dummy_conversation_data,line: 139     INFO | Done!
        
    ----- N O T E S -----
    Values in the region DEFINITIONS can be customized.
    
    BASE URL: https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/collector
    Parameters sent to API:
        - distance
        - age
        - gender
        - basic_emotion
        - pleasure_state
        - excitement_state
        - smile_state
        - dialog_time

    ----- A U T H O R S H I P - A N D - C O N T R I B U T I O N ----- 
    @Date: 2022, January 4.
    @Author: Benjamin Thomas Schwertfeger
    @Email: development@b-schwertfeger.de
    @Contributors: Kristian Kellermann, Jacob Menge
    @Links: https://github.com/ProjectPepperHSB/Backend-Services
'''

# ----- I M P O R T S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

import sys, traceback 
import requests
import numpy as np
import logging
from tqdm import tqdm
import argparse

# ----- S E T U P ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- Argument - Parser -----
parser = argparse.ArgumentParser(description="Create dummy data to send to API")
parser.add_argument(
    "-n", type=int, dest="nr_of_entries_to_generate", default=1000,  
    help="number of datasets to generate and send | default: 1000"
)
parser.add_argument(
    "-p", "--prod", dest="production", default=False, action="store_true", 
    help="send to https://informatik.hs-bremerhaven.de instead to localhost | default: False"
)
args = parser.parse_args()

# ----- Logger -----
formatter = logging.Formatter(
    fmt="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
) 
log = logging.getLogger()
log.setLevel(logging.INFO)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logging.getLogger().addHandler(screen_handler)

# ----- D E F I N I T I O N S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- dont change this ----- 
SUBJECT = "save_pepper_data" 
BASE_URL = "https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/collector" if vars(args)["production"] else "http://127.0.0.1:3000/docker-hbv-kms-http/collector"
NR_OF_ENTRIES_TO_GENERATE = vars(args)["nr_of_entries_to_generate"]

# ----- following can be customized ----- 
basic_emotions = ["bad", "good", "excited", "bored"]
pleasure_states = ["bad", "medium", "good", "pefect"]
excitement_states = ["excited", "not excited"]
smile_state = ["false", "medium", "true"]

# ----- F U N C T I O N S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def get_random_conversation_data():
    '''Return randomized conversation data as type dict.'''
    dialog_times = np.random.normal(3, 3, 1000) 
    return {
        "distance": np.round(np.random.random() * 2, 4),
        "age": np.random.choice(range(3, 80, 1)),
        "gender": np.random.choice(["male", "female"]) if np.random.random() > 0.0001 else "other",
        "basic_emotion": np.random.choice(basic_emotions),
        "pleasure_state": np.random.choice(pleasure_states),
        "excitement_state": np.random.choice(excitement_states),
        "smile_state": np.random.choice(smile_state),
        "dialog_time": np.round(np.random.choice(dialog_times[dialog_times > 1]), 2)
    }

def do_request(query_string: str):
    '''Send get request to API.

        ----- Keyword arguments -----
        query_string: str | Query string to send
        
        ----- Example -----
        do_request(query_string="&gender=male")    
    
    '''

    try:
        response = requests.get(f"{BASE_URL}?subject={SUBJECT}&{query_string}")
        if response.status_code != 200:
            raise ConnectionError
    except Exception as e:
        log.error(f"{e}, {traceback.format_exc()}") # <- will not show up bc of tqdm is clearing screen
        log.warning("Exiting now!")
        exit()

def submit_data(data: dict):
    '''Create query string and trigger request function.

        ----- Keyword arguments -----
        data: dict | Dictionary containing key value pairs to be sent 
        
        ----- Example -----
        submit_data(data={ "gender": "male", "age": 18 })    
    
    '''

    do_request("&".join([f"{key}={data[key]}" for key in data]))

# ----- M A I N ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def main():
    '''Main function'''

    log.info(f"Sending {NR_OF_ENTRIES_TO_GENERATE} dummy datasets to {BASE_URL}")
    [submit_data(get_random_conversation_data()) for _ in tqdm(range(NR_OF_ENTRIES_TO_GENERATE))]
    log.info("Done!")
   

if __name__ == "__main__":
    '''Function to mark standalone script'''
    main()   

# ----- E O F ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----