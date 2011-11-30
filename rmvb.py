#!/usr/bin/python
# encoding=UTF-8
import subprocess
import sys
import gmail
import gg
import os.path

def rmvb_to_avi(path):
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
	args.append('sample.avi')
	print args
	return_code = subprocess.check_call(args)
	if return_code != 0:
		return return_code
	path2 = './'+ 'sample.avi'
	return path2
def avi_to_flv(path):
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
	args.append('sample.flv')
	print args
	return_code = subprocess.check_call(args)
	if return_code != 0:
		return return_code
	path2 = './'+ 'sample.flv'
	return path2
def main():
	if len(sys.argv) < 2:  
		print u'error hahaha!\n'
	send_name=os.path.basename(sys.argv[1])
	gtalk=gg.gtalk()
	gm=gmail.gmail()
	gtalk.send_to_gtalk(send_name+"  正在转换中")
	path = rmvb_to_avi(sys.argv[1])
	path2 = avi_to_flv(path)
	gtalk.send_to_gtalk(send_name+"  转换完成")
	gm.send_to_gmail(send_name + "转换完成",send_name + "转换完成")
	#path2 = avi_to_flv(sys.argv[1])
	
if __name__ == '__main__':
	main()
