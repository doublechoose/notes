# 使用FFmpeg 批量MP4视频分离成mp3
import os
import subprocess

current = os.getcwd()

dirs = os.listdir(current)

for i in dirs:
        
        if i.split('.')[1] == "mp4":
                os.rename(i,"temp.mp4")
                getmp3 = 'ffmpeg -i temp.mp4 -f mp3 -vn temp.mp3'
                returnget = subprocess.call(getmp3,shell = True)
                # returncut = subprocess.call(cutmp3,shell = True)
                # os.remove('temp.mp3')
                os.rename('temp.mp3',i.split('.')[0] + '.mp3')
                os.rename('temp.mp4',i)
                print(returnget)