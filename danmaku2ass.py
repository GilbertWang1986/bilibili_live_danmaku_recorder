import json
import time
import math


def time_convert(t):
    # s (second, float) to hour:miniute:second
    _h = math.floor(t/3600)
    res = t - _h*3600
    _m = math.floor(res/60)
    res = res - _m*60
    _s = res
    return '%d:%02d:%.2f'%(_h, _m, _s)



def danmaku2ass(fin, fout=None, delay=None):
    if fout == None:
        fout = '%s.ass'%(fin)
    if delay == None:
        delay = 75

    live_record = json.loads( open(fin).read() )
    start_time = live_record['start_time']
    end_time = live_record['end_time']
    danmakus = live_record['danmakus']

    with open( fout, 'w' ) as f:
        # [Script Info] section
        f.write( '[Script Info]\n' )
        f.write( 'ScriptType: v4.00+\n' )
        f.write( 'Collisions: Normal\n' )
        f.write( 'PlayResX: 384\n' )
        f.write( 'PlayResY: 288\n' )
        f.write( 'Timer: 100.0000\n' )
        f.write( '\n' )

        # [V4+ Styles] section
        f.write( '[V4+ Styles]\n' )
        f.write( 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n' )
        f.write( 'Style: Default,方正黑体_GBK,20,&H00ffffff,&Hf0000000,&H00000000,&H32000000,0,0,0,0,100.00,100.00,0.00,0.00,1,2.00,1.00,2,5,5,2,134\n' )
        f.write( '\n' )

        # [Events] section
        f.write( '[Events]\n' )
        f.write( 'Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n' )

        for _d in danmakus:
            nickname = _d['nickname']
            text = _d['text']
            timeline = time.mktime( time.strptime(_d['timeline'], '%Y-%m-%d %X') )
            timeline -= delay # delay
            
            # ignore the danmakus posted 60 s efore the live
            if timeline - start_time < -60:
                continue

            start = timeline - start_time 
            if start <=0:
                start = 0
            end = start + 20

            f.write('Dialogue: 0,')
            f.write(time_convert(start)+',')
            f.write(time_convert(end)+',')
            f.write('Default,NTP,0000,0000,0000,,')
            f.write( '%s(%s)'%(text, nickname) )
            f.write('\n')




if __name__ == '__main__':
    import os
    import sys

    if len(sys.argv) == 1:
        print( 'Name of danmaku file is needed' )
    
    elif len(sys.argv) == 2:
        fin = sys.argv[1]
        print('Input: ', fin)
        print('Output: ', '%s.ass'%(fin))
        print('delay: %f s'%(75))
        danmaku2ass(fin)

    elif len(sys.argv) == 3:
        fin = sys.argv[1]
        fout = sys.argv[2]
        print('Input: ', fin)
        print('Output: ', fout)
        print('delay: %f s'%(75))
        danmaku2ass(fin, fout)

    elif len(sys.argv) == 4:
        fin = sys.argv[1]
        fout = sys.argv[2]
        delay = float(sys.argv[3])
        print('Input: ', fin)
        print('Output: ', fout)
        print('delay: %f s'%(delay))
        danmaku2ass(fin, fout, delay)

    else:
        print('Too much argument values')



