import os
from os.path import isfile
import subprocess

class Dirs_and_files:
    
    def __init__(self,path):
        self.path=path
        
    def get_dir(self):
        f=os.listdir(self.path)
        res=[]
        if self.path [-1]!= os.sep:
            self.path+=os.sep
        for i in f:
            if isfile(self.path+i)==False:
                res.append(self.path+i)
        return res


    def all_dirs(self):
        folders=self.get_dir()
        for i in folders:
            try:
                for n in Dirs_and_files(i).get_dir():
                    folders.append(n)
            except:
                pass
        return folders


    def all_dir_recursive(self):
        f = self.get_dir()
        d=[]
        if len(f)>0:
            for i in f:
                d.append(i)
                try:
                    for n in Dirs_and_files(i).all_dir_recursive():
                        d.append(n)
                except:
                    pass
        return d


    def get_files(self):
        if self.path [-1]!= os.sep:
            self.path+=os.sep
        f = [] 
        for i in os.listdir(self.path):
            if isfile(self.path+i):
                f.append(self.path+i)
        return f


    def get_all_files(self):
        dirs=[self.path]+self.all_dir_recursive()
        res=[]
        for i in dirs:
            res+=Dirs_and_files(i).get_files()
        return res
    
    def get_type(self):
        res=[]
        for i in os.listdir(self.path):
            if isfile(self.path+i):
                res.append(i)
        return res
        
    

class Delet_files():
    
    def __init__(self):
        self.to_send = ''
        self.sec=[]
        

    def delet_one_file(self,file_path):
        file_path=file_path.replace('\\\\','\\')
        p = subprocess.Popen("del "+file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       
    
    def recursive_fles_delete(self,path):
        p = subprocess.Popen('rd /s /q "'+path+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        c = p.stdout.readline()
        if len(c)<2:
            return 'Successfully deleted'
        return c