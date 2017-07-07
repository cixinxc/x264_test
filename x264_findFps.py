# -*- coding:utf-8 -*-
# function     找到不同分辨率和不同bitrate下，PSNR=40时的FPS值
# create time  2017/07/07
# creator      崔鑫鑫

from subprocess import Popen, PIPE
import re, sys, string
import matplotlib.pyplot as plt
import os

#
os.chdir('c:/MinGW/msys/1.0/home/x264/')
# 正则表达式规则
re_real_bitrate = re.compile('kb/s:([\d.]+)')
re_psnr = re.compile('x264 \[info\]: PSNR Mean Y:([\d.]+)')
re_frameNum = re.compile('encoded ([\d.]+)')
# re_psnr_eachFrame = re.compile('x264 \[debug\]: frame=[\s]{0,3}([\d]+).*Y:([\d.]+)')
# 参数设置
minStepL = 1     # fps调节最小步长
maxStepL = 100   # FPS调节最大步长
IterStepL = 2    # FPS调节速率
maxIterNum = 40  # 最大迭代次数
maxPSNR = 40.15  # 最大可接受PSNR
inputBitrate = [100, 300, 500, 750, 1000, 1500, 2000, 4000]     # 需要的bitrate
inputBitrate = [100, 300]     # 需要的bitrate
bitrate = 500  # 循环变量
keyint = 15  # 由输入文件决定
fps = 33  # 循环变量
inputRes = '640x480'  # 由输入文件清晰度决定
name = "out"
inputFilePath = 'd:/yuvOut/'
inputFileName = 'out%s.yuv' % inputRes
outFilePath = 'd:/yuvOut/'
outFileName = '%s_%d_%d_.264' % (inputFileName, bitrate, fps)
# 日志文件
logFile = r'D:/WorkSpace/PYTHON/x264_test/x264_test_%s.log' % inputFileName
if logFile:
    lf = open(logFile, 'a+')
# 迭代查找各视频在不同bitrate下编码时，PSNR=40的FPS
currentPSRN = 0
iterNum = 0
for bitrate in inputBitrate:
    while (currentPSRN < 40 or currentPSRN >= maxPSNR) and iterNum <= maxIterNum:
        # 拼接CMD命令
        command_param = (r'x264 --preset faster --bitrate %d --keyint %d --bframes 0 --fps %d -o %s%s %s%s '
                         r'--input-res %s '
                         r'--psnr' % (bitrate, keyint, fps, outFilePath, outFileName, inputFilePath, inputFileName,
                                      inputRes)).split(' ')
        out, err = Popen(list(command_param), stderr=PIPE).communicate()
        err = err.decode('GBK')
        real_bitrate = re_real_bitrate.findall(err)
        psnr = re_psnr.findall(err)
        frameNum = re_frameNum.findall(err)
        # 记录本次日志
        print('\t inputRes:%s\t bitrate:%s\t fps:%s' % (inputRes, bitrate, fps), file=lf)
        print('\t\t PSNR:%s\t frameNum:%s\t realBitrate:%s' % (psnr[0], frameNum[0], real_bitrate[0]), file=lf)
        lf.flush()

        currentPSRN = float(psnr[0])
        iterNum += iterNum
