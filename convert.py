#!/usr/bin/env python
#coding=utf-8
import MySQLdb
import subprocess
import os.path
import hashlib
def processFLV(path): #用ffmpeg解码
	tmp = os.path.basename(path)
	tmp = tmp.split('.')
	convt_file = tmp[0]
	path2 = '/var/video/convert/'+convt_file+'.flv'
	args = ['ffmpeg', '-i', path, '-ab', '64', '-ac', '2', '-ar', '22050',  '-r', '29.97', '-y', path2]
	print ' '.join(args)
	exit()
	p = subprocess.check_call(args)
	return path2
def check_type(path): #检查文件的视频属性 ,如果是ffmpeg不支持的格式要用mencoder来解码
	tmp = os.path.basename(path)
	tmp = tmp.sqlist('.')
	tmp_type = tmp[-1]
	type0=['flv']
	type1 = ['mpg','wmv','3gp','mov','mp4','asf','mkv']
	type2 = ['wmv9','rm','rmvb'] 
	if tmp_tpye in type0:# 如果上床的视频已经是flv格式,则不用再次转换
		return 0
	elif tmp_type in type1:
		return 1
	elif tmp_type in type2: #ffmpeg 所不支持的格式
		return 2
	else:                   # 不支持的格式
		return 3
def processAVI(path): #调用mencoder把视频转还为avi
	tmp = os.path.basename(path)
	tmp = tmp.split('.')
	convt_file = tmp[0]
	path2 = '/var/video/convert/'+convt_file+'.avi'
	args=['mencoder','oac','lavc','-lavcopts','acodec=mp3:abitrate=64','-ovc','xvid','-xvidencopts','bitrate=600','-of','avi','-o',path2]
	p = subprocess.check_call(args)
	return path2

conn=MySQLdb.connect(host="localhost",user="root",passwd="wukong",db="video")
cursor = conn.cursor()
sql= "select * from covert"
n= cursor.execute(sql)
for i in cursor.fetchall():
	path = i[1]
	path2 = processFLV(path)
	f = open(path2,'rb')
	h = hashlib.md5()
	h.update(f.read())
	hash_value = h. hexdigest()

	#更新带转换视频的信息状态
	sql2= "update  covert set state = " + "1" +" where id ="+str(i[0])
	#print sql2
	cursor.execute(sql2)

	#将转码后的视频传到相应的服务器
	args2 =['scp',path2,'root@192.168.0.106:/root/']
	p = subprocess.check_call(args2)


	#更新视频库信息，增加转还后视频路径信息
	sql2= "update video_h  set state = " + "1" +" where id ="+str(i[0])
	cursor.execute(sql2)
	sql2= "update video_h  set path2 = '"+ path2 +"' where id ="+str(i[0])
	print sql2
	cursor.execute(sql2)
	sql2= "update video_h  set hash_value = '"+ hash_value +"' where id ="+str(i[0])
	cursor.execute(sql2)


cursor.close()
conn.close()

