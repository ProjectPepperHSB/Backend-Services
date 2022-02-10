
__version__ = '0.4.1'
__author__      = 'Benjamin Thomas Schwertfeger'
__copyright__   = 'Benjamin Thomas Schwertfeger'
__email__ = 'development@b-schwertfeger.de'
__credits__ = ['Kristian Kellermann', 'Jacob Menge']
__status__ = 'Prototype'

# ----- D E S C R I P T I O N ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

'''
    get_timetable_data.py
    ===================================

    This script is used to download custom timetable information to csv from the website of the University of Bremerhaven.
       
    
    ----- A R G U M E N T S -----    
    usage: get_timetable_data.py [-h] [-c COURSE] [-s SEMESTER] [-cw CW]

    required arguments:
        -cw CW, --cw CW                   Calendar week | e.g.: 42 | default: 42

    optional arguments:
        -h, --help                        show this help message and exit
        -c COURSE, --course COURSE        Course | e.g.: Wirtschaftsinformatik | default: None
        -s SEMESTER, --semester SEMESTER  Semester | e.g.: 7
        

    ----- E X A M P L E -----
    ╰─ python3 get_timetable_data.py -cw 42
    100%|██████████████████████████████████████████████████████████████████████████████████| 11/11 [00:25<00:00,  2.29s/it]
        
    ----- A U T H O R S H I P - A N D - C O N T R I B U T I O N ----- 
    @Date: 2022, January 4.
    @Author: Benjamin Thomas Schwertfeger
    @Email: development@b-schwertfeger.de
    @Contributors: Kristian Kellermann, Jacob Menge
    @Links: https://github.com/ProjectPepperHSB/Backend-Services
'''

# ----- I M P O R T S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

import requests
from bs4 import BeautifulSoup
import pandas as pd
from argparse import ArgumentParser
import json, csv
from tqdm import tqdm

# ------ S E T U P ----- ----- ----- ------ ------ ----- ------ ----- ----- ------

parser = ArgumentParser()
parser.add_argument('-cw', '--cw', dest='cw', help='Calendar week | e.g.: 42', required=True)
parser.add_argument('-c', '--course', dest='course', default=None, help='Course | e.g.: Wirtschaftsinformatik | default: None')
parser.add_argument('-s', '--semester', dest='semester', help='Semester | e.g.: 7')
args = parser.parse_args()

courses = {
    'Wirtschaftsinformatik': 'WI',
    'Informatik': 'INF',
    'Betriebswirtschaftslehre': 'BWL',
    'Crouse Tourism Management': 'CTM',
    'Digitalisierung, Innovation und Informationsmanagement': 'DIIM',
    'Erasmus': 'Erasmus',
    'Digitale Medien Produktion': 'DMP',
    'Gründung, Innovation, Führung': 'GIF',
    'Integrated Safety and Security Management': 'ISSM',
    'Logistics Engineering and Management': 'LEM',
    'Transportwesen und Logistik': 'TWL',
}

# ------ ----- ----- ----- ------ ------ ----- ------ ----- ----- ------

def get_course_id(name: str) -> int:
    '''Return the course id scraped from the university website
        ----- Keyword arguments -----
        name: str | Course name 
        
        ----- Example -----
        get_course_id(name='WI')   
    
    '''

    url = 'https://www4.hs-bremerhaven.de/fb2/ws2122.php?action=showfb&fb=%23SPLUS938DBF'
    res = requests.get(url).content
    selection = BeautifulSoup(res, 'html.parser').find('select', attrs={ 'name': 'identifier' })

    courseId = None
    for row in selection.find_all('option'):
        if row.get_text() == name:
            courseId = row.get('value')

    return courseId

def specific() -> None:
    '''Get a specific timetable from the university website to save to csv.'''
    course = courses[args.coourse] + '_B' + args.semester
    courseId = get_course_id(course)
    url = f'https://www4.hs-bremerhaven.de/fb2/ws2122.php?action=showplan&weeks={args.cw}&fb=%23SPLUS938DBF&idtype=&listtype=Text-Listen&template=Set&objectclass=Studenten-Sets&identifier={courseId}&days=1;2;3;4;5&tabstart=41'
    response = requests.post(url)
    html = response.content

    table = BeautifulSoup(html, 'html.parser'.find('table', attrs={ 'class': 'spreadsheet' }))
    data, headings = [], None
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headings = [td.get_text() for td in row.find_all('td')]
        else:
            values = [td.get_text() for td in row.find_all('td')]
            data.append(values)

    data_ = {}
    for i, headline in enumerate(headings):
        data_[headline] = [x[i] for x in data]

    df = pd.DataFrame.from_dict(data_)
    df.to_csv(f'{course}_{args.cw}.csv', index=False, sep=';')
    # df.to_csv(f'/var/www/html/hbv-kms/timetablesfb2/{course}_{args.cw}.csv', index=False, sep=';')
    #json.dumps(json.loads(df.to_json(orient='index')))

# ----- M A I N ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def main() -> None:
    '''Iterate over all courses, get the ids and scrap the page content for every course in each semester to save to csv.'''

    for course in tqdm(courses):
        for sem in range(1, 7, 1):
            course_ = courses[course] + '_B' + str(sem)
            courseId = get_course_id(course_)
            if not courseId:
                continue

            url = f'https://www4.hs-bremerhaven.de/fb2/ws2122.php?action=showplan&weeks={args.cw}&fb=%23SPLUS938DBF&idtype=&listtype=Text-Listen&template=Set&objectclass=Studenten-Sets&identifier={courseId}&days=1;2;3;4;5&tabstart=41'
            response = requests.post(url)
            html = response.content

            table = BeautifulSoup(html, 'html.parser').find('table', attrs={ 'class': 'spreadsheet' })
            if not table:
              continue
            data, headings = [], None

            for i, row in enumerate(table.find_all('tr')):
                if i == 0:
                    headings = [td.get_text() for td in row.find_all('td')]
                else:
                    values = [td.get_text() for td in row.find_all('td')]
                    data.append(values)

            data_ = {}
            for i, headline in enumerate(headings):
                data_[headline] = [x[i] for x in data]

            if data:
                df = pd.DataFrame.from_dict(data_)
                df.to_csv(f'{course_}_{args.cw}.csv', index=False, sep=';')
                # df.to_csv(f'/var/www/html/docker-hbv-kms-web/timetablesfb2/{course_}_{args.cw}.csv', index=False, sep=';')

# ------ ----- ----- ----- ------ ------ ----- ------ ----- ----- ------

if __name__ == '__main__':
    main()

# ----- E O F ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----