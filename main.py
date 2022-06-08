#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import cv2 as cv
import numpy as np
import os
import random

# 创建文件
def Create_folder(filename):
    filename = filename.strip()
    filename = filename.rstrip("\\")
    isExists = os.path.exists(filename)

    if not isExists:
        os.makedirs(filename)
        print(filename+"创建成功")
        return  True
    else:
        print(filename+"已存在")
        return False

print('请输入保存文件夹名称，保存目录位于上一级')
save_path_name = input()
# 获取当前目录下所有图片列表并处理
print('--------------获取当前图片列表--------------')
file_nums = 0
save_path = os.path.join('../'+save_path_name+'/')
Create_folder('../'+save_path_name)
file_all = os.walk(r'.')

try:
        for path,dir,filelist in file_all:
                for filename in filelist:
                        if filename.endswith('jpg') or filename.endswith('png'):
                                pending_image = os.path.join(path, filename)
                                print(pending_image)
                                image = cv.imdecode(np.fromfile(pending_image,dtype=np.uint8),cv.IMREAD_GRAYSCALE)
                                binary = cv.adaptiveThreshold(image,255,
                                        cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,25,15)
                                se = cv.getStructuringElement(cv.MORPH_RECT,(1,1))
                                se = cv.morphologyEx(se, cv.MORPH_CLOSE, (2,2))
                                mask = cv.dilate(binary,se)
                                # cv.imshow("image",image)
                                
                                mask1 = cv.bitwise_not(mask)
                                binary =cv.bitwise_and(image,mask)
                                result = cv.add(binary,mask1)
                                # cv.imshow("reslut",result)
                                save_file_name = save_path+str(random.randint(0,100))+'-'+filename
                                cv.imencode('.jpg', result)[1].tofile(save_file_name)
                                # cv.waitKey(0)
                                # cv.destroyAllWindows()
                                file_nums = file_nums + 1 

except:
        print(pending_image+'图片错误，请检查！')

print('——-------------处理结果--------------')
print('共处理了'+str(file_nums)+'图片')
print('保存目录'+save_path)
input()
