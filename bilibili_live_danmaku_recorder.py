#-*-code:utf-8-*-

import requests
import json
import time



def get_room_stat(room_id):
    # room_id: int
    url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
    r = requests.get(url, params={'room_id':room_id})
    data = json.loads(r.text)['data']

    description = data['description']
    live_status = data['live_status']
    tags = data['tags']
    title = data['title']

    room_stat = { 'description': description,
                  'live_status': live_status,
                  'tags'       : tags,
                  'title'      : title }

    return room_stat




def get_live_danmaku(room_id):
    url = 'http://api.live.bilibili.com/ajax/msg'
    r = requests.get(url, params={'roomid':room_id})
    data = json.loads(r.text)

    danmakus = []
    for _d in data['data']['room']:
        danmakus.append( { 'timeline' : _d['timeline'], 
                           'nickname' : _d['nickname'],
                           'text'     : _d['text']      } )
    return danmakus



def fetch_danmakus(room_id, retry=15):

    _last_danmakus = []
    _live_status = 0

    while True:

        try:
            room_stat = get_room_stat(room_id)
            # print(time.ctime(time.time()), 'live_status', room_stat['live_status'])

            if _live_status == 0:
                if room_stat['live_status'] == 1: # live start
                    # init a live record
                    _live_record = {}
                    _live_record['description'] = room_stat['description']
                    _live_record['title'] = room_stat['title']
                    _live_record['tags'] = room_stat['tags']
                    danmakus = []

                    _live_record['start_time'] = time.time()
                    start_time_local = time.localtime(_live_record['start_time'])
                    start_time_str = '%d%02d%02d_%02d%02d%02d'%( start_time_local[0], start_time_local[1], start_time_local[2],
                                                       start_time_local[3], start_time_local[4], start_time_local[5] )
                    print('Live started at ', start_time_str)
            
            if _live_status == 1:
                if room_stat['live_status'] == 0: # live end
                    _live_record['end_time'] = time.time()
                    end_time_local = time.localtime(_live_record['end_time'])
                    end_time_str = '%d%02d%02d_%02d%02d%02d'%( end_time_local[0], end_time_local[1], end_time_local[2],
                                                     end_time_local[3], end_time_local[4], end_time_local[5] )
                    print('Live ended at ', end_time_str)
                    _live_record['danmakus'] = danmakus
                    # save live record
                    with open('%d_%s.json'%(room_id, start_time_str), 'w') as f:
                        f.write( json.dumps(_live_record, ensure_ascii=False) )
            
            _live_status = room_stat['live_status']
        
        except:
            print('Fetch live room status fail')


        if _live_status == 1:
            try:
                _current_danmakus = get_live_danmaku(room_id)
            except:
                _current_danmakus = []
            for _d in _current_danmakus:
                if not _d in _last_danmakus:
                    print(_d['timeline'], _d['nickname'], _d['text'])
                    danmakus.append(_d)
            _last_danmakus = _current_danmakus


        time.sleep(retry)



if __name__ == '__main__':

    import sys

    id_77 = 21828604

    if len(sys.argv) == 1:
        print( 'ID of liveroom is needed, or Liveroom 21828604 would be recorded' )
        print( 'Room ID:', id_77 )
        print( 'Time for retry: %f s'%(75) )
        fetch_danmakus(id_77)
    elif len(sys.argv) == 2:
        room_id = int(sys.argv[1])
        print( 'Room ID:', room_id )
        print( 'Time for retry: %f s'%(75) )
        fetch_danmakus(room_id)
    elif len(sys.argv) == 3:
        room_id = int(sys.argv[1])
        retry = float(sys.argv[2])
        print( 'Room ID:', room_id )
        print( 'Time for retry: %f s'%(retry) )
        fetch_danmakus(room_id, retry)

    

   




