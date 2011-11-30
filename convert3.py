#!/usr/bin/env python
#coding=utf-8
import subprocess
import os.path
import os
import shutil 
import video_process
import time
	

video = video_process.video_process()
ISOTIMEFORMAT='%Y-%m-%d %X'
ftp_temp ="/var/video/tempv/"
ftp_source = "/var/video/source_video/"
def main():
	while True:
    a = os.listdir("/var/video/tempv/")#a为文件总数
		if len(a)==0:      #如果记录数为零则休眠60S
			print "无转换队列,sleep 60S侯继续"
			time.sleep(60)
			continue
		for i in a:
			path = i
			info = get_info(path)
			flv_path = video.covert(path)
			#flv_hash_value = hashfile(flv_path)
      shutil.move(ftp_temp + path,ftp_source +path)

def get_info(path):#获得文件的属性，文件名 扩展名,转换开始时间，结束时间
	info = {}
	info["filename"]= video.get_basename(path)
	info['type'] =  video.check_type(path)
	info['start_time_str']= time.strftime( ISOTIMEFORMAT, time.localtime(time.time())) #转换开始时间,字符串格式
	info['start_time_int'] = time.time()
	return info
if __name__ == '__main__':
	main()

