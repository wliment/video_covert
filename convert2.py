#!/usr/bin/env python
#coding=utf-8
import MySQLdb
import subprocess
import os.path
import hashlib
import video_process
import time
import gtalk
	

video = video_process.video_process()
ISOTIMEFORMAT='%Y-%m-%d %X'
def main():
	gtalk_message = gtalk.gtalk()
	conn=MySQLdb.connect(host="localhost",user="root",passwd="wukong",db="video")
	cursor = conn.cursor()
	while True:
		sql= "select * from covert"
		n= cursor.execute(sql)
		if n==0:      #如果记录数为零则休眠60S
			print "无转换队列,sleep 60S侯继续"
			time.sleep(60)
			continue
		for i in cursor.fetchall():
			path = i[1]
			info = get_info(path)
			flv_path = video.covert(path)
			flv_hash_value = hashfile(flv_path)

			#更新带转换视频的信息状态
			sql2= "update  covert set state = " + "1" +" where id ="+str(i[0])
			#print sql2
			cursor.execute(sql2)

			#将转码后的视频传到相应的服务器
			#args2 =['scp',path2,'wiment@127.0.0.1:/var/video/convert']
			#p = subprocess.check_call(args2)


			#更新视频库信息，增加转还后视频路径信息
			sql2= "update video_h  set state = " + "1" +" where id ="+str(i[0])
			cursor.execute(sql2)
			sql2= "update video_h  set flv_path = '"+ flv_path +"' where id ="+str(i[0])
			print sql2
			cursor.execute(sql2)
			sql2= "update video_h  set flv_hash_value = '"+ flv_hash_value +"' where id ="+str(i[0])
			cursor.execute(sql2)
			info['stop_time_str'] = time.strftime( ISOTIMEFORMAT, time.localtime(time.time()))
			use_time = time.time() - info['start_time_int']  #获取转换所用时间
			message = info["filename"] + " 转换完成\n文件类型: "+ info['type'] +'\n' \
					+ "转换开始时间: "+ info['start_time_str'] +'\n'\
					+ "转换结束时间: "+ info['stop_time_str'] + '\n' \
					+ "转换用时: " + str(int(use_time)) + '秒'
			#gtalk_message.send_to_gtalk( message )
			sql2 = "delete from covert where id ="+str(i[0]) #删除转换表中的数据
			cursor.execute(sql2)




	cursor.close()
	conn.close()

def hashfile(path): #获取文件的hash值
	f = open(path,'rb')
	h = hashlib.md5()
	h.update(f.read())
	hash_value = h.hexdigest()
	return hash_value
def get_info(path):#获得文件的属性，文件名 扩展名,转换开始时间，结束时间
	info = {}
	info["filename"]= video.get_basename(path)
	info['type'] =  video.check_type(path)
	info['start_time_str']= time.strftime( ISOTIMEFORMAT, time.localtime(time.time())) #转换开始时间,字符串格式
	info['start_time_int'] = time.time()
	return info
if __name__ == '__main__':
	main()

