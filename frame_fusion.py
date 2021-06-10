# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt
import numpy as np
video_capture = cv2.VideoCapture('run.mp4')
save_path_file ='run.jpg'
start=0.8#起始秒
fps=30
backgroundframe=0#int(0.05*fps) 背景帧不含想要检测的动态形象
frame0=int(start*fps)#600
step=2#步长 frames
length=11#帧数
gaussian_ksize=3
kopen=7#去噪
kclose=17#补空隙
background=[]
video_capture.set(1,backgroundframe); # Where frame_no is the frame you want
ret, img0 = video_capture.read() # Read the frame
background = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
#background = cv2.GaussianBlur(background, (gaussian_ksize, gaussian_ksize), 0)
# 对帧进行预处理，先转灰度图，再进行高斯滤波。
# 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化
#等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
i=0
for frame_no in range(frame0,frame0+step*length,step):
    i+=1
    video_capture.set(1,frame_no); # Where frame_no is the frame you want
    ret, img = video_capture.read() # Read the frame
    
    #if i==1:
        #cv2.imwrite('frame0.jpg',img)
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (gaussian_ksize,gaussian_ksize), 0)
       
        # 对于每个从背景之后读取的帧都会计算其与背景之间的差异，并得到一个差分图（different map）。
        # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，
        #从而对孔（hole）和缺陷（imperfection）进行归一化处理
        diff = cv2.absdiff(background, gray)
        mask = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[1] #第二个返回参数
        #0黑255白 <25 为0  二值化阈值处理
        kernel=np.ones((kopen,kopen),np.uint8)
        mask= cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)#侵蚀，再膨胀 去噪
        #https://www.jianshu.com/p/a8ee3674c061
        kernel=np.ones((kclose,kclose),np.uint8)
        mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)#膨胀，再侵蚀
        plt.imshow(mask,cmap="gray")
        plt.show()
        
        mask_inv = cv2.bitwise_not(mask)#蒙版01反转
        img=cv2.bitwise_and(img, img,mask=mask)#只有蒙版mask部分非0
        b=cv2.bitwise_and(img0, img0,mask=mask)#蒙版中的累积部分
        img0= cv2.bitwise_and(img0,img0,mask = mask_inv) #挖去背景中蒙版部分
        m=np.uint8(np.floor(img*0.5+b*0.5))#当前动作与累积历史动作叠加
        if i==length:#最后一帧
            img0 = cv2.add(img0,img)#蒙版处没有累积动作（只显示最后一帧）
            #img0=cv2.add(img0,m)#蒙版处有积累动作
        else:
            img0=cv2.add(img0,m)
        
cv2.imwrite(save_path_file,img0)

    