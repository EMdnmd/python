'''
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2020/12/17 9:31
Tool ：PyCharm
'''
import  os
from datetime import datetime
from random import randint


class fileUoload():
    def __init__(self,file,exts=["png",'jpg',"jpeg","text"],size=1024*1024,is_randomnane=False):
            '''
            :param file: 上传文件对象
            :param exts: 文件格式
            :param size:文件大小，
            :param is_randomnane:是否随机生成文件名 默认为否
            '''

            self.file=file
            self.exts=exts
            self.size=size
            self.is_randomnane=is_randomnane

    # 文件上传
    def file_judge(self,dest):
            '''

              :param dest:文件上传目标
              :return:
            '''
            # 判断文件格式是否正确
            if  not self._check_type() :
                return  -1
            # 判断文件大小
            if not  self._checj_type():
                return -2
            # 判断文件是否需要随机名
            if self.is_randomnane:
                    self.file_name=self._ren_time()
            else:
                 self.file_name=self.file.name
            #     上传文件
            path=os.path.join(dest,self.file_name)
            self._write_file(path)
            return (True,self.file_name)


    # 判断文件后缀
    def  _check_type(self):
        print(self.file.name)
        ext=os.path.splitext(self.file.name)#获取文件后缀
        if len(ext)>1:
            ext=ext[1].lstrip(".")#将文件中的点去掉
            if ext in self.exts:
                return  True
        else:
            return  False
    # 判断文件大小
    def _checj_type(self):
        if self.size<0:
            return  False
        return  self.file.size<=self.size
    #文件随机名
    def _ren_time(self):
        fitime=datetime.now().strftime("%Y%m%d%H%M%S" )+"tp"+str(randint(1000,100000))
        ext=os.path.splitext(self.file.name)
        ext=ext[1] if len(ext)>1  else " "
        fitime+=ext
        return fitime

    def _write_file(self ,path):
            '''
            :param path: 文件路径
            :return:
            '''
            with open(path,"wb") as  fp:
                if self.file.multiple_chunks():
                        for chunk in self.file.chunks():
                            fp.write(chunk)
                else:
                    fp.write(self.file.read())