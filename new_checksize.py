#!/usr/bin/python3
#-*- coding : utf-8 -*-
#version : 0.0.2
#create:2019-11-10
#describe:
'''
此脚本用于核对下载ont数据的大小，主要功能为，获取obs数据的文件的文件名和文件大小，整理好对应的格式，写在obs.txt中，通过合同
编号获取本地的文件名称和大小，然后保存到 local.txt 文件中，最后对两个文件进行排序对比，输出不同的文件。
'''

import subprocess
import re
import os
USER_PATH = "/home/liuy/DataCheckScript/record"
try:
    os.system("rm -rf local.txt obs.txt")
except Exception as e:
    raise e

project_name = input("请输入合同编号： ")
# root_path = input("请输入项目所在服务器上的路径： ")
class CheckFiles:

    def __init__(self):
        self.project = project_name
        # self.RootPath = root_path
        # self.RawPath = root_path + project_name

    def open_file(self,file,objs=None,methd="r"):
        if methd =="r":
            #获取OBS的路径
            with open(file,methd) as f:
                cell_path_list = f.readlines()
                return cell_path_list
        elif methd =="a+":
            with open(file,methd) as f1:
                for k,y in objs.items():
                    f1.write(k + "\t"+y +"\n")

    def get_obspath(self,cell_path_list):
         for cell_path in cell_path_list:
            self.filesize = {}
            self.path_list = []
            self.fileSize_list = []
            self.cell_path = cell_path.replace("\n","")
            self.myutils()
            self.filesize = dict(zip(self.path_list,self.fileSize_list))
            self.open_file("{}/{}_obs.txt".format(USER_PATH,self.project),objs=self.filesize,methd="a+")


    def myutils(self):
        res = subprocess.Popen("obsutil ls -limit -1 -bf=raw {}".format(self.cell_path),shell=True,stdout=subprocess.PIPE)
        obj_byte_list = res.stdout.readlines()
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
                    self.path_list.append(obs_path)
            elif re.findall('\s[0-9]+B',obj_byte.decode("utf8")):
                self.fileSize_list.append(re.findall('\s[0-9]+B',obj_byte.decode("utf8"))[0])
            else:
                pass

    def get_localpath(self):
        local_dic = {}
        dir_item=os.walk("/home/liuy/software/{}".format(self.project))
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
                local_dic[local_path] = " "+str(file_size)+"B"
        return local_dic

    @staticmethod
    def diffile():
        print("-------------------------------------------")
        os.system("cat %s/%s_obs.txt %s/%s_local.txt | sort | uniq -c | sort -n -k 1  | awk '{if($1==1)print $2,$3}'"%(USER_PATH,project_name,USER_PATH, project_name))
        print("--------------------------------------------")






obj = CheckFiles()
cell_path_list = obj.open_file("Obslist.txt")
obj.get_obspath(cell_path_list)
local_dic = obj.get_localpath()
obj.open_file("{}/{}_local.txt".format(USER_PATH,project_name),objs=local_dic,methd="a+")
CheckFiles.diffile()
