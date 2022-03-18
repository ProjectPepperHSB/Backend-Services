__version__ = '1.2.3'
__author__ = 'Jacob Benjamin Menge'
__copyright__ = 'Jacob Benjamin Menge'
__status__ = 'Production'
__github__ = 'https://github.com/ProjectPepperHSB/Backend-Services.git'

# =============================================== D E S C R I P T I O N ================================================

'''
    create_videodata.py
    ===================================

    This script downloads video files from the 3d-Berlin API, which was created for the Bremerhaven University of 
    Applied Sciences. It also creates the videos so that we can integrate them into our own API. The structure of the 
    file names consists of three necessary pieces of information, which are separated from each other by a "-" sign for 
    the sake of clarity and always form a name that only occurs once for the recognition of the respective video. The 
    first section contains the ID for the starting point of the route and the second the ID for the end point to be 
    reached. The definition of these IDs are the same ID names as used by the 3D-Berlin API. This has the advantage that
    we can better understand in retrospect which request the corresponding video originally came from. In addition, it 
    would be time-redundant to create a new ID numbering for this. The third section of the video name describes 
    whether it is a video with an accessible path or an ordinary path. In this case, the designation "M0000" stands for
    the ordinary path and "M0001" for a path that takes accessibility into account. Thus, there are two different 
    variants for each video.
    
    ----- E X A M P L E -----
    
    =================== ROUTE_TO_ROOM: C006 ===================
    accessibily_mode: False
    GET-REQUEST --> https://cdnguide3dcom.blob.core.windows.net/videos/100011/544x306/L00P1133-L01P1056-M0000.mp4
    try to downloading video ..
    Request was successful! HTTP status code is: 200. 
    start to downloading video ..
    Video is saved as L00P1133-L01P1056-M0000.mp4
    Success!
    (...)
    
    ----- N O T E S -----
    
    Please note that the downloaded videos are all stored in the directory in which the script is executed. In addition,
    an internet connection is of course necessary to execute the script correctly.
    
    ----- A U T H O R S H I P - A N D - C O N T R I B U T I O N -----
    @date: 2022, January 4.
    @author: Jacob Benjamin Menge
    @email: mengejacob@gmail.com
    @github: https://github.com/ProjectPepperHSB/Backend-Services
'''

# ================================================ I M P O R T S =======================================================

import requests

# ================================================== S E T U P =========================================================

# request to get meta information for videos
rq = requests.get(
    'https://services.guide3d.com/menu/cors/index.php?project=100011&language=de&set=set_01&force-display=false')
videos = rq.json()
directory = "videos"

# Project id | Bremerhaven project id: 100011
project = "100011"

# main domain to 3d-Berlin API
url = f'https://cdnguide3dcom.blob.core.windows.net/videos/{project}'

# the image format in pixels. the API supports only 544x306 in most cases.
video_format = '544x306'
startpoint = "L00P1133"


# ============================================== F U N C T I O N S =====================================================

def get_video(url: str, startpoint: str, endpoint: str, accessibily_mode: bool, format: str):
    """
    :param url: Download link to video (.mp4)
    :param startpoint: start point from where the route should begin
    :param endpoint: the end point at which the route ends (the point to which the user wants to go)
    :param accessibily_mode: determines whether the accessibility mode should be enabled or disabled. Depending on which
     mode is selected, a sensible path is chosen. For efficiency reasons, a string is used instead of a boolean.
     M0000 = normal path| M0001 = Accessible path.
    :param format:the image format in pixels. the API supports only 544x306 in most cases.
    """

    mode = "M0000"

    # check mode for accessibily to change the type of the request
    if accessibily_mode:
        mode = "M0001"

    # definition of the video name, which later serves as a unique ID
    video_name = f'{startpoint}-{endpoint}-{mode}.mp4'

    # definition of the request to get the right video
    define_req = f'{url}/{format}/{startpoint}-{endpoint}-{mode}.mp4'

    print(f'GET-REQUEST --> {define_req}')
    print(f'try to downloading video ..')
    r = requests.get(define_req, allow_redirects=True)

    # check that the HTTP status code 200 indicates OK, which means that the request was successful.
    if r.status_code == 200:
        print(f'Request was successful! HTTP status code is: {r.status_code}. ')
        write_video(directory, video_name, r)
    else:
        print('\x1b[6;30;41m' + 'something went wrong!' + '\x1b[0m')
        print(f'HTTP status code is: {r.status_code}')


def write_video(directory, video_name, request_object):
    """
    :param directory: direct path under which the video is to be saved
    :param video_name: name of the MP4 file to be saved
    :param request_object: the request object received from the request
    """

    print("start to downloading video ..")
    open(f'{directory}/{video_name}', 'wb').write(request_object.content)
    print(f'Video is saved as {video_name}')
    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')


# =================================================== M A I N ==========================================================

if __name__ == '__main__':

    for video in range(len(videos['data']['list'])):
        endpoint = videos['data']['list'][video]['point']
        room = videos['data']['list'][video]['name']
        print(f'=================== ROUTE_TO_ROOM: {room} ===================')
        print("accessibily_mode: False")
        get_video(url=url,
                  startpoint=startpoint,
                  endpoint=endpoint,
                  accessibily_mode=False,
                  format=video_format)

        print("accessibily_mode: True")
        get_video(url=url,
                  startpoint=startpoint,
                  endpoint=endpoint,
                  accessibily_mode=True,
                  format=video_format)
