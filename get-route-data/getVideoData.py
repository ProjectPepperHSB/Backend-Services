import requests


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

    # check mode
    if accessibily_mode:
        mode = "M0001"

    video_name = f'{startpoint}-{endpoint}-{mode}.mp4'
    define_req = f'{url}/{format}/{startpoint}-{endpoint}-{mode}.mp4'
    print(f'Download Videodata ..')
    print(f'GET-REQUEST --> {define_req}')
    r = requests.get(define_req, allow_redirects=True)
    print(r.status_code)
    open(f'{directory}/{video_name}', 'wb').write(r.content)
    print(f'saved as {video_name}')


if __name__ == '__main__':

    # request to get meta information for videos
    rq = requests.get(
        'https://services.guide3d.com/menu/cors/index.php?project=100011&language=de&set=set_01&force-display=false')
    videos = rq.json()
    directory = "videos"

    # Project id | Bremerhaven project id: 100011
    project = "100011"
    # main domain
    url = f'https://cdnguide3dcom.blob.core.windows.net/videos/{project}'
    # the image format in pixels. the API supports only 544x306 in most cases.
    video_format = '544x306'

    startpoint = "L00P1133"

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