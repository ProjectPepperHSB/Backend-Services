import json
import requests

# open needData.json
with open('needData.json') as file:
    data = json.load(file)

new_data_struc = {}

# startpoint id
startpoint = "L00P1133"

# Project id | Bremerhaven project id: 100011
project = "100011"


# generate request for video metadata
def get_request(mode: str, project: str, startpoint: str, endpoint: str):
    """
    :param mode: mode for disabled access | disabled access mode True:  M0001 | disabled access mode False:  M0000
    :param project: the project used by 3Dberlin
    :param startpoint:
    :param endpoint:
    :return:
    """
    url = f'https://services.guide3d.com/route/cors/index.php?project={project}&start={startpoint}&end={endpoint}&mode={mode}&redirect=duration&format=none'
    return requests.get(url, allow_redirects=True)


if __name__ == '__main__':

    # print(json.dumps(data, indent=4))
    count = 0

    # iterate over used json data
    for d in data["data"]["list"]:
        count += 1
        endpoint = d["point"]
        video_name = f'{startpoint}-{endpoint}-'
        video_path = f'video/{video_name}'

        # define request for video metadata
        r_M0000 = get_request(mode="M0000", project=project, startpoint=startpoint, endpoint=endpoint)
        r_M0001 = get_request(mode="M0001", project=project, startpoint=startpoint, endpoint=endpoint)

        # print data
        print(f'dis: {r_M0000.json()["distance"]}')
        print(f'time: {r_M0000.json()["duration"]}')
        print(f'dis: {r_M0001.json()["distance"]}')
        print(f'time: {r_M0001.json()["duration"]}')

        # add new data to dictonary
        new_data_struc.update(
            {f'{d["name"]}': {'M0000': {'video_path': f'{video_path}M0000.mp4',
                                        'location': f'{d["location"]}',
                                        'distance': f'{r_M0000.json()["distance"]}',
                                        'time': f'{r_M0000.json()["duration"]}'},
                              'M0001': {'video_path': f'{video_path}M0001.mp4',
                                        'location': f'{d["location"]}',
                                        'distance': f'{r_M0001.json()["distance"]}',
                                        'time': f'{r_M0001.json()["duration"]}'}}})

        print(new_data_struc)
        print(count)

        # write data into json
        with open('route_data.json', 'w') as fp:
            json.dump(new_data_struc, fp)
