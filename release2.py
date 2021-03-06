#!/usr/bin/env/python3
# _*_ coding : utf-8 _*_
#version: 0.0.2
import logging
import os
project_name = input("请输入合同编号：  ")
delivery_method = input("请选择需要释放的方式：1.硬盘释放；2.OBS 释放 ：  ")
release_type = input("请选择需要释放的类型： 1.原始数据; 2.fastq 数据：  ")

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename="log/ont.log",filemode='a+')



class ReleaseData(object):

    def instancechek(self):
        with open('ont.txt','r') as files :
            cell_sample_list = files.readlines()
            for cell_sample in cell_sample_list:
                try:
                    cell_list = cell_sample.split('\t')
                    sample_name = cell_list[0].strip()
                    cell_path = cell_list[1].strip()
                    library_id = cell_path.split("-")[3]
                    cell_name = cell_path.split("/")[7]
                    chip_name = cell_name.split("-")[3]
                    cell_path_list = cell_path.split("/")
                except Exception as e:
                    cell_list = cell_sample.split(' ')
                    sample_name = cell_list[0].strip()
                    cell_path = cell_list[1].strip()
                    library_id = cell_path.split("-")[3]
                    cell_name = cell_path.split("/")[7]
                    chip_name = cell_name.split("-")[3]
                    cell_path_list = cell_path.split("/")
                #print(cell_path)
                barcode = self.isbarcode(cell_path,chip_name)
                head = self.release_method(delivery_method)
                target_path,new_path = self.release_rawdata(release_type, project_name, sample_name, library_id, cell_name, chip_name,cell_path,head,barcode)
                #print(target_path,new_path)
                self.path = target_path
                self.release(target_path,new_path)

    def isbarcode(self,cell_path,ship_name):
        if "NB" in cell_path:
            barcode_id = cell_path.strip().split("/")[-2]
            return barcode_id
        else:
            new_path = cell_path+ship_name+"/"
            return new_path

    def release_method(self,delivery_method):
        #硬盘释放
        if delivery_method == "1":
            head = "/home/liuy/software/"
        #OBS释放
        elif delivery_method == "2":
            head = "obs://nextomics6/FTP/"
        return head


    def release_rawdata(self,release_type, project_name, sample_name, library_id, cell_name, chip_name, cell_path,head,barcode):
        #释放原始数据
        if release_type == "1":
            if "NB" in cell_path:
                body = "{}/raw_data/genome/Nanopore/{}/{}/".format(project_name,sample_name,cell_name)

            else:
                body = "{}/raw_data/genome/Nanopore/{}/".format(project_name,sample_name)
            new_path = cell_path
            target_path = head + body
        #释放fastq
        elif release_type == "2":
            if  "NB" in cell_path:
                new_path = cell_path + "qc_report/"
                body = "{}/raw_data/genome/Nanopore/{}/{}/{}/".format(project_name,sample_name,cell_name,barcode)
                target_path = head+body
            else:
                new_path = cell_path+chip_name+"/qc_report/"

            #print(cell_path)
                body = "{}/raw_data/genome/Nanopore/{}/{}/{}/".format(project_name,sample_name,cell_name,chip_name)
                target_path = head+body
        return target_path,new_path

    def release(self,target_path,new_path):

        #print(new_path)
        status=os.system("obsutil cp -r -f -u -vlength -vmd5 {} {}".format(new_path,target_path))
        logging.info("obsutil cp -r -f -u {} {} successful".format(new_path,target_path))
        if status == 0:
            print("OK")
        else:
            print("warning")
            os.system("obsutil cp -r -f -u -vlength -vmd5 {} {}".format(new_path,target_path))

    def putfile(self):
        import datetime
        now_time = datetime.date.today()
        #times = time.strftime("%Y%m&d")
        if delivery_method == "1":
            #硬盘释放
            os.system("tree -h %s >%s/directory_description.txt"%(project_name,project_name))
            os.system("tree -h %s > tree_record/%s_%s-tree.txt && obsutil cp -r -f tree_record/%s_%s-tree.txt obs://backup-nextomics-wh/Record/%s/%s/"%(project_name,now_time,project_name,now_time,project_name,project_name,now_time))
            os.system("cp -r -f Nanopore_Data_documentation.doc {}/".format(project_name))
        else:
            os.system("obsutil cp -r -f Nanopore_Data_documentation.doc obs://nextomics6/FTP/{}/".format(project_name))
            os.system("tree -h /nextomics6/FTP/%s > tree_record/%s_%s-tree.txt && obsutil\
             cp -r -f tree_record/%s_%s-tree.txt obs://nextomics6/FTP/%s/&& \
             obsutil cp -r -f tree_record/%s_%s-tree.txt \
             obs://backup-nextomics-wh/Record/%s/%s/"%(project_name,now_time,project_name,now_time,project_name,project_name,now_time,project_name,project_name,now_time))

    def create_share(self):
        import subprocess
        res = subprocess.Popen("obsutil create-share obs://nextomics6/FTP/{}/ -ac=112233 -vp=2w".format(project_name),shell=True,stdout=subprocess.PIPE)
        s = res.stdout.readlines()
        for x in s:
            print(x.decode("utf-8"))

        print("图形化界面下载说明文档：https://www.nextomics.cn/obs_browser_read_me/")
        print("linux命令行下载说明文档：https://www.nextomics.cn/obsutil-download-link/")
        print("15日后链接失效，请及时下载，若超期未下载，需要支付二次释放费用")
        print("本次释放路径：obs://nextomics6/FTP/{}/".format(project_name))


if __name__ == "__main__":
    obj=ReleaseData()
    obj.instancechek()
    obj.putfile()
    if delivery_method == "2":
        obj.create_share()
