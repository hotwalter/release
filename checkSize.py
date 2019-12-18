#!/usr/bin/python3
#-*- coding : utf-8 -*-

import subprocess
import re
import os



#获取OBs 文件大小 并写入到obs.txt 文件中
with open("ont.txt","r") as f:
    cell_sample_list = f.readlines()
    for cell_sample in cell_sample_list:
        filesize = {}
        raw_list = []
        size_list = []
        cell_sample = cell_sample.replace("\n","")
        res = subprocess.Popen("obsutil ls -limit -1 -bf=raw {}".format(cell_sample),shell=True,stdout=subprocess.PIPE)
        obj_byte_list  = res.stdout.readlines()
        for obj_byte in obj_byte_list:
            if b'obs://' in obj_byte :
                if re.findall('^obs.+\\/$',obj_byte.decode()):
                    pass
                else:
                    #取最后三层目录
                    obs_abs_path = obj_byte.decode().replace("\n","")
                    obs_path = obs_abs_path.split("/")[-1:-4:-1]
                    obs_path.reverse()
                    obs_path = "/".join(obs_path)
                    raw_list.append(obs_path)
            elif re.findall('\s[0-9]+B',obj_byte.decode("utf8")):
                 size_list.append(re.findall('\s[0-9]+B',obj_byte.decode("utf8"))[0])
        with open("obs.text",'a+') as f1:
            i= 0
            while True:
                filesize[raw_list[i]] = size_list[i]
                i+=1
                if i == len(raw_list):
                    break
            for k,y in filesize.items():
                f1.write(k + "\t"+y +"\n")

#获取本地的文件大小 并写入到local.txt 文件中

project_name = input("请输入合同编号：  ")
#返回值为一个生成器对象
dir_item=os.walk(project_name)

local_dic = {}
for maindir,subdir,files in dir_item:
    #遍历所有的文件
    for file in files:
        #获取文件的路径
        abs_path = os.path.join(maindir,file)
        #只需要最后三层得目录
        local_path = abs_path.split("/")[-1:-4:-1]
        local_path.reverse()
        local_path = "/".join(local_path)
        #获取文件的大小
        file_size = os.path.getsize(abs_path)
        local_dic[local_path] = file_size

with open("local.txt","a+") as f2:
    for k,v in local_dic.items():
        f2.write(k + "\t " +str(v) +"B\n")