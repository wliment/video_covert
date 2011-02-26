#!/usr/bin/python
#coding=utf-8
import subprocess
import sys,os

class video_process:
	def __init__(self):
		self.tempv_path = '/var/video/tempv/'  #原始视频存储目录
		self.covert_path = '/var/video/convert/' #转换后视频存储目录
		self.mid_dir = '/var/video/mid_data/'

	def __mkv_extract_audio(self,path): #mvk 提取音频轨道数据
		args =[]
		args.append('mkvextract')
		args.append('tracks')
		args.append(path)
		path2 = self.mid_dir + 'temp.aac'
		args.append('2:'+ path2 )  #mkv 音频轨道默认为2
		return_code = subprocess.check_call(args)
		if return_code !=0:
			return return_code
		return path2
	def __yamdi(self,path):   #往flv写入关键桢
		args = []
		args.append('yamdi')
		args.append('-i')
		args.append(path)
		args.append('-o')
		path2 = path+'.new'
		args.append(path2)
		return_code = subprocess.check_call(args)
		if return_code != 0:
			return return_code
		os.remove(path)
		os.rename(path2,path)
		return return_code
		
	def __mkv_to_avi(self,path):
		path2= self.__mkv_extract_audio(path) 
		if path2 == 0:
			return path2
		args = []
		args.append('mencoder')
		args.append(path)
		args.append('-oac')
		args.append('mp3lame')
		args.append('-audiofile')
		args.append(path2)
		args.append('-ovc')
		args.append('xvid')
		args.append('-xvidencopts')
		args.append('fixed_quant=2')
		args.append('-slang')
		args.append('chi')
		args.append('-subcp')
		args.append('utf8')
		args.append('-subfont-text-scale')
		args.append('3')
		args.append('-font')
		args.append('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
		args.append('-o')
		#filename = self.get_basename()
		path2 = self.mid_dir +self.filename + '.avi'
		args.append(path2 ) 				 # avi视频数据在视频当前目录,等转换为flv文件后删除
		#print args
		return_code = subprocess.check_call(args)
		if return_code != 0:
			return return_code
		return path2
	def __rmvb_to_avi(self,path):
		args = []
		args.append('mencoder')
		args.append(path)
		args.append('-oac')
		args.append('pcm')
		args.append('-ovc')
		args.append('xvid')
		args.append('-xvidencopts')
		args.append('fixed_quant=2')
		args.append('-o')
		path2 = self.mid_dir + self.filename + '.avi'
		args.append(path2)
		print args
		return_code = subprocess.check_call(args)
		if return_code != 0:
			return return_code
		return path2

	def __avi_to_flv(self,path):
		args = []
		args.append('ffmpeg')
		args.append('-i')
		args.append(path)
		args.append('-acodec')
		args.append('libfaac')
		args.append('-ac')
		args.append('1')
		args.append('-ar')
		args.append('44100')
		args.append('-ab')
		args.append('64')
		args.append('-f')
		args.append('flv')
		args.append('-threads')
		args.append('0')
		args.append('-r')
		args.append('24')
		args.append('-vcodec')
		args.append('libx264')
		args.append('-vpre')
		args.append('hq')
		args.append('-crf')
		args.append('20')
		args.append('-y')
		path2 = self.covert_path + self.filename + '.flv'
		print path2
		args.append(path2)
	#	print args
		return_code = subprocess.check_call(args)
		if return_code != 0:
			return return_code
		return path2

	def get_basename(self,video_path):  #除去扩展名的文件名
		tmp = os.path.basename(video_path)	
		self.filename = ''.join(tmp.split('.')[:-1])
		return self.filename

	def check_type(self,path): #检查文件的格式
		tmp = os.path.basename(path)
		tmp1 = tmp.split('.')
		tmp_type = tmp1[-1]
		return tmp_type

	def __mkv_process(self,video_path):
		path = self.__mkv_to_avi(video_path)
		path2 = self.__avi_to_flv(path)
		return path2
	def __rmvb_process(self,video_path):
		path = self.__rmvb_to_avi(video_path)
		path2 = self.__avi_to_flv(path)
		return path2

	def covert(self,video_path):
		self.filename = self.get_basename(video_path)
		video_chose = {"mkv": self.__mkv_process,"rmvb":self.__rmvb_process,"avi":self.__avi_to_flv,"mpeg":self.__avi_to_flv}
		video_type = self.check_type(str(video_path))
		print video_type
		process = video_chose[video_type]
		path2 = process(video_path)   #开始转码
		return_code = self.__yamdi(path2)
		if return_code !=0:
			return return_code
		if video_type in['mkv','rmvb']:
			os.remove( self.mid_dir + self.filename + '.avi' ) #删除中间的avi文件
		return path2
