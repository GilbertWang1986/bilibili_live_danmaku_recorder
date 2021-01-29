# bilibili_live_danmaku_recorder
Record danmaku during bilibili live in json format and convert it to substitles file in ass format

## Requests:
* 1. Python3
* 2. Library: requests

## bilibili_live_danmaku_recorder.py 
bilibili_live_danmaku_recorder.py is used to recorde danmaku during Bilibili lives in a json file.
Usage: python bilibili_live_danmaku_recorder.py  room_id  [time for retry (default: 15)]


## danmaku2ass.py 
danmaku2ass.py is used to convert the damaku json file to ass substitles file.
Usage: python danmaku2ass.py json_file_name  [ass_file_name (default:json_file_name+'.ass')]  [delay (default: 75)]
delay is used to synchronize substitles with vedio

The argument values in [] can be omitted.
