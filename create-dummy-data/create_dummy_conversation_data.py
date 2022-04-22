
__version__ = '1.0.0'
__author__ = 'Benjamin Thomas Schwertfeger'
__copyright__ = 'Benjamin Thomas Schwertfeger'
__status__ = 'Production'
__github__ = 'https://github.com/ProjectPepperHSB/Backend-Services.git'

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
        -p, --prod            send to https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/api/v1 instead to http://127.0.0.1:3000/docker-hbv-kms-http/api/v1 | default: False

    ----- E X A M P L E -----
    ╰─ python3 create_dummy_conversation_data.py --prod -n 250
    2022-01-04 09:51:25 create_dummy_conversation_data,line: 137     INFO | Sending 250 dummy datasets to https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/api/v1
    100%|████████████████████████████████████████████████████████████████████████████████████████| 250/250 [00:33<00:00,  7.49it/s]
    2022-01-04 09:51:59 create_dummy_conversation_data,line: 139     INFO | Done!

    ----- N O T E S -----
    Values in the region DEFINITIONS can be customized.

    BASE URL: https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/collector

    ----- A U T H O R S H I P - A N D - C O N T R I B U T I O N -----
    @date: 2022, January 4.
    @author: Benjamin Thomas Schwertfeger
    @email: development@b-schwertfeger.de
    @github: https://github.com/ProjectPepperHSB/Backend-Services
'''

# ----- I M P O R T S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

import sys, traceback
import logging
import argparse

from joblib import Parallel, delayed
from tqdm import tqdm

import requests
import numpy as np
import random
import string
import json

import uuid

# ----- S E T U P ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- Argument - Parser -----
parser = argparse.ArgumentParser(description='Create dummy data to send to API')
parser.add_argument(
    '-n', type=int, dest='nr_of_entries_to_generate', default=1000,
    help='number of conversations with datasets to generate and send to backend | default: 1000'
)
parser.add_argument(
    '-p', '--prod', dest='production', default=False, action='store_true',
    help='send to https://informatik.hs-bremerhaven.de instead to localhost | default: False'
)
args = parser.parse_args()

# ----- Logger -----
formatter = logging.Formatter(
    fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger()
log.setLevel(logging.INFO)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logging.getLogger().addHandler(screen_handler)

# ----- D E F I N I T I O N S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- dont change this -----

BASE_URL = 'https://informatik.hs-bremerhaven.de/docker-hbv-kms-http/api/v1' if vars(args)['production'] else 'http://localhost:3000/docker-hbv-kms-http/api/v1'
NR_OF_ENTRIES_TO_GENERATE = vars(args)['nr_of_entries_to_generate']

# ----- following can be customized -----
basic_emotions = ['bad', 'good', 'excited', 'bored']
pleasure_states = ['bad', 'medium', 'good', 'perfect']
excitement_states = ['excited', 'not excited']
smile_states = ['false', 'medium', 'true']

use_cases = ['RouteFinder', 'TimeTable', 'Mensa', 'SmallTalk', 'About HS', 'About HBV']

human_body_types = ['fat', 'sporty', 'normal', 'skinny']
colors = ['blonde', 'black', 'no hair', 'white', 'red', 'orange', 'green', 'blue', 'brown']

# ----- F U N C T I O N S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def get_random_data() -> dict:
    '''Return randomized emotion, conversation, use-case and not understand phrase data as type dict.'''
    identifier = uuid.uuid4().hex
    
    dialog_times = np.random.normal(3, 3, 1000)
    dialog_time = np.round(np.random.choice(dialog_times[dialog_times > 1]), 2)
    
    emotion_data = [{ 
        'identifier': identifier,
        'distance': np.round(np.random.random() * 2, 4),
        'age': np.random.choice(range(3, 80, 1)),
        'gender': np.random.choice(['male', 'female']) if np.random.random() > 0.0001 else 'other',
        'basic_emotion': np.random.choice(basic_emotions),
        'pleasure_state': np.random.choice(pleasure_states),
        'excitement_state': np.random.choice(excitement_states),
        'smile_state': np.random.choice(smile_states),
        'dialog_time': dialog_time
    }]
    
    nr_of_use_cases = np.random.choice(np.arange(0, len(use_cases)))
    use_case_data = [{
            'identifier': identifier,
            'use_case': np.random.choice(use_cases)
        } for _ in range(nr_of_use_cases)
    ]

    nr_of_not_understand_phrases = np.random.choice(np.arange(5)) if dialog_time < 6 else np.random.choice(np.arange(10))
    did_not_understand_data = [{
            'identifier': identifier,
            'phrase': ''.join(random.choices(f'{string.ascii_lowercase}{string.digits}', k = np.random.choice(range(5, 20, 1))))    
        } for _ in range(nr_of_not_understand_phrases)
    ]

    conversation_data = [{
        'identifier': identifier,
        'data': { 
            'attributes': {
                'hair': np.random.choice(colors),
                'eyes': np.random.choice(colors),
                'body': np.random.choice(human_body_types)
            }
        }
    }]

    return {
        'saveEmotionData': emotion_data,
        'saveUseCaseData': use_case_data,
        'saveNotUnderstandPhrases': did_not_understand_data,
        'saveAttributeData': conversation_data
    }

def do_request(method: str,  endpoint: str, query_string='', data={}) -> None:
    '''Send get request to API.

        ----- Keyword arguments -----
        query_string: str | Query string to send

        ----- Example -----
        do_request(method='GET', endpoint='saveEmotionData', query_string='&gender=male')
    '''

    try:
        if method == 'GET':
            response = requests.get(f'{BASE_URL}/{endpoint}?{query_string}')
        elif method == 'POST':
            response = requests.post(f'{BASE_URL}/{endpoint}', data = data)

        if response.status_code != 200:
            log.warn(response)
            raise ConnectionError
    except Exception as e:
        log.error(f'{e}, {traceback.format_exc()}')
        log.warning('Exiting now!')
        exit()

def submit_datasets(datasets: dict) -> None:
    '''Create query string and trigger request function.

        ----- Keyword arguments -----
        data: dict | Dictionary containing key value pairs to be sent

    '''
    for endpoint in datasets:
        if endpoint == 'saveAttributeData':
            [
                do_request(
                    method = 'POST',
                    endpoint = endpoint,
                    data = {
                        'identifier': dataset['identifier'],
                        'data': json.dumps(dataset['data'])
                    }
                ) for dataset in datasets[endpoint]
            ]
        else: 
            [
                do_request(
                    method = 'GET',
                    endpoint = endpoint,
                    query_string = '&'.join([f'{key}={dataset[key]}' for key in dataset])
                ) for dataset in datasets[endpoint]
            ]

# ----- M A I N ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def main() -> None:
    '''Main function'''

    log.info(f'Sending {NR_OF_ENTRIES_TO_GENERATE} dummy datasets to {BASE_URL}')
    Parallel(n_jobs=6)(delayed(submit_datasets)(get_random_data()) for _ in tqdm(range(NR_OF_ENTRIES_TO_GENERATE)))
    log.info('Done!')


if __name__ == '__main__':
    '''Function to mark standalone script'''
    main()



# ----- E O F ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----