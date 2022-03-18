# Script to create MP4-Video data `create_videodata.py`

This script downloads video files from the 3d-Berlin API, which was created for the Bremerhaven University of Applied Sciences. It also creates the videos so that we can integrate them into our own API. 

Here is a link to the API from 3d-Berlin that we used to generate the videos:
https://www.3d-berlin.com/portfolio_page/university-bremerhaven-de_de

The structure of the file names consists of three necessary pieces of information, which are separated from each other by a "-" sign for the sake of clarity and always form a name that only occurs once for the recognition of the respective video. The first section contains the ID for the starting point of the route and the second the ID for the end point to be reached. The definition of these IDs are the same ID names as used by the 3D-Berlin API. This has the advantage thatwe can better understand in retrospect which request the corresponding video originally came from. In addition, it would be time-redundant to create a new ID numbering for this. The third section of the video name describes whether it is a video with an accessible path or an ordinary path. In this case, the designation "M0000" stands for the ordinary path and "M0001" for a path that takes accessibility into account. Thus, there are two different variants for each video.

Please note that the downloaded videos are all stored in the directory in which the script is executed. In addition, an internet connection is of course necessary to execute the script correctly.

## Example for console output
    =================== ROUTE_TO_ROOM: C006 ===================
    accessibily_mode: False
    GET-REQUEST --> https://cdnguide3dcom.blob.core.windows.net/videos/100011/544x306/L00P1133-L01P1056-M0000.mp4
    try to downloading video ..
    Request was successful! HTTP status code is: 200. 
    start to downloading video ..
    Video is saved as L00P1133-L01P1056-M0000.mp4
    Success!

    (...)

## Run by
```bash
╰─ python3 create_videodata.py
```

# Script to generate the meta information related to the videos `create_metadata.py`

This script creates a dataset in java object notation. The content of the data is information about the paths between rooms within the university of applied sciences bremerhaven.

Here is a link to the API from 3d-Berlin that we used to get all this meta information about the 3D-Navigation:
https://www.guide3d.mobi/?project=100011

    
**The following attributes are described in the data:**
    
    *  **Type of route**
        For each route description there are two different ways to reach the destination. In each case, we create a barrier-free route and an ordinary route or a route that can be reached quickly.
        
    *  **Video path** 
        This parameter represents the direct link to the corresponding data with the associated spatial information. In this way, we can determine the appropriate video with the correct route description as precisely as possible.
        
	*  **Location**
        The location is a short description in which house and which floor the room is located. Such a location description would be, for example, "House C ground floor". With this description Pepper can provide the user with additional information for verbal interaction.
        
    *  **Distance**
        The distance is the distance from the starting point of the directions to the destination. We use metres as the unit and round this up to whole metres for better comprehensibility.
        
    *  **Duration** 
        The duration is given in minutes. It describes the time needed from the starting point to the destination, based on the average walking speed.

It should be noted that the json file created is stored in the directory in which the script is executed. In addition, an internet connection is of course necessary to execute the script correctly.  

## Example for console output

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

## Run by
```bash
╰─ python3 create_metadata.py
```
